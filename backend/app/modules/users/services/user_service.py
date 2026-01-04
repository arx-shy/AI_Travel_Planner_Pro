"""
User Service

This module provides business logic for user operations.
"""

from typing import Optional
from datetime import datetime, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.security.password import hash_password, verify_password
from app.core.security.jwt import create_access_token
from app.modules.users.models.user import User
from app.modules.users.daos.user_dao import UserDAO
from app.modules.users.daos.user_settings_dao import UserSettingsDAO
from app.modules.users.daos.subscription_dao import SubscriptionDAO
from app.modules.users.models.user_settings import UserSettings
from app.modules.users.models.subscription import Subscription


class UserService:
    """
    User business logic service
    """
    
    def __init__(self, db: AsyncSession):
        """
        Initialize UserService
        
        Args:
            db: Database session
        """
        self.db = db
        self.user_dao = UserDAO(db)
        self.user_settings_dao = UserSettingsDAO(db)
        self.subscription_dao = SubscriptionDAO(db)
    
    async def register_user(
        self,
        email: str,
        password: str,
        name: str
    ) -> tuple[User, str]:
        """
        Register a new user
        
        Args:
            email: User email
            password: User password
            name: User name
            
        Returns:
            Tuple of (user, access_token)
            
        Raises:
            ValueError: If email already exists
        """
        # Check if email exists
        if await self.user_dao.email_exists(email):
            raise ValueError("Email already registered")
        
        # Create user
        hashed_pwd = hash_password(password)
        user = User(
            email=email,
            hashed_password=hashed_pwd,
            name=name,
            is_active=True,
            membership_level='free'
        )
        
        user = await self.user_dao.create(user)
        
        # Create access token
        access_token = create_access_token(subject=str(user.id))
        
        return user, access_token
    
    async def authenticate_user(
        self,
        email: str,
        password: str
    ) -> Optional[tuple[User, str]]:
        """
        Authenticate user with email and password
        
        Args:
            email: User email
            password: User password
            
        Returns:
            Tuple of (user, access_token) or None if authentication fails
        """
        # Get user by email
        user = await self.user_dao.get_by_email(email)
        
        if not user:
            return None
        
        # Verify password
        if not verify_password(password, user.hashed_password):
            return None
        
        # Create access token
        access_token = create_access_token(subject=str(user.id))
        
        return user, access_token
    
    async def get_user_by_id(self, user_id: int) -> Optional[User]:
        """
        Get user by ID
        
        Args:
            user_id: User ID
            
        Returns:
            User object or None
        """
        return await self.user_dao.get_by_id(user_id)
    
    async def update_user(
        self,
        user_id: int,
        **kwargs
    ) -> Optional[User]:
        """
        Update user
        
        Args:
            user_id: User ID
            **kwargs: Fields to update
            
        Returns:
            Updated user object or None
        """
        # Remove sensitive fields from kwargs
        sensitive_fields = ['id', 'hashed_password', 'email', 'created_at', 'membership_level']
        for field in sensitive_fields:
            kwargs.pop(field, None)
        
        return await self.user_dao.update(user_id, **kwargs)
    
    async def change_password(
        self,
        user_id: int,
        old_password: str,
        new_password: str
    ) -> bool:
        """
        Change user password
        
        Args:
            user_id: User ID
            old_password: Current password
            new_password: New password
            
        Returns:
            True if password changed, False otherwise
            
        Raises:
            ValueError: If old password is incorrect
        """
        user = await self.user_dao.get_by_id(user_id)
        
        if not user:
            return False
        
        # Verify old password
        if not verify_password(old_password, user.hashed_password):
            raise ValueError("Incorrect password")
        
        # Update password
        hashed_new_pwd = hash_password(new_password)
        await self.user_dao.update(user_id, hashed_password=hashed_new_pwd)

        return True

    async def get_or_create_settings(self, user_id: int) -> UserSettings:
        settings = await self.user_settings_dao.get_by_user_id(user_id)
        if settings:
            return settings
        settings = UserSettings(
            user_id=user_id,
            language="zh-CN",
            theme="auto",
            timezone="Asia/Shanghai",
            currency="CNY",
            preferences={}
        )
        return await self.user_settings_dao.create(settings)

    async def update_settings(self, user_id: int, **kwargs) -> UserSettings:
        settings = await self.get_or_create_settings(user_id)
        return await self.user_settings_dao.update(settings, **kwargs)

    async def get_or_create_subscription(self, user_id: int) -> Subscription:
        subscription = await self.subscription_dao.get_by_user_id(user_id)
        if subscription:
            return subscription
        now = datetime.utcnow()
        subscription = Subscription(
            user_id=user_id,
            plan_type="free",
            status="active",
            start_date=now,
            end_date=now + timedelta(days=365),
            auto_renew=False
        )
        return await self.subscription_dao.create(subscription)
