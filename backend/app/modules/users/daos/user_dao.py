"""
User Data Access Object (DAO)

This module provides database access operations for users.
"""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.modules.users.models.user import User


class UserDAO:
    """
    Data Access Object for User model
    """
    
    def __init__(self, db: AsyncSession):
        """
        Initialize UserDAO
        
        Args:
            db: Database session
        """
        self.db = db
    
    async def get_by_id(self, user_id: int) -> User:
        """
        Get user by ID
        
        Args:
            user_id: User ID
            
        Returns:
            User object or None
        """
        result = await self.db.execute(select(User).where(User.id == user_id))
        return result.scalars().first()
    
    async def get_by_email(self, email: str) -> User:
        """
        Get user by email
        
        Args:
            email: User email
            
        Returns:
            User object or None
        """
        result = await self.db.execute(select(User).where(User.email == email))
        return result.scalars().first()
    
    async def create(self, user: User) -> User:
        """
        Create a new user
        
        Args:
            user: User object
            
        Returns:
            Created user object
        """
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        return user
    
    async def update(self, user_id: int, **kwargs) -> User:
        """
        Update user
        
        Args:
            user_id: User ID
            **kwargs: Fields to update
            
        Returns:
            Updated user object
        """
        user = await self.get_by_id(user_id)
        if user:
            for key, value in kwargs.items():
                setattr(user, key, value)
            await self.db.commit()
            await self.db.refresh(user)
        return user
    
    async def delete(self, user_id: int) -> bool:
        """
        Delete user
        
        Args:
            user_id: User ID
            
        Returns:
            True if deleted, False otherwise
        """
        user = await self.get_by_id(user_id)
        if user:
            await self.db.delete(user)
            await self.db.commit()
            return True
        return False
    
    async def email_exists(self, email: str) -> bool:
        """
        Check if email exists
        
        Args:
            email: Email to check
            
        Returns:
            True if exists, False otherwise
        """
        result = await self.db.execute(select(User).where(User.email == email))
        return result.scalars().first() is not None
