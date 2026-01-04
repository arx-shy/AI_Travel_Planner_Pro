"""
User API Routes

This module defines FastAPI routes for user operations.
"""

from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from fastapi.security import HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.db.session import get_db
from app.core.security.deps import get_current_user
from app.modules.users.services.user_service import UserService
from app.modules.users.services.quota_service import QuotaService
from app.modules.users.schemas.user import (
    UserCreate,
    UserLogin,
    UserUpdate,
    UserResponse,
    LoginResponse,
    RegisterResponse,
    PasswordChange,
    UserQuotaInfo
)
from app.modules.users.models.user import User
from app.core.config.settings import settings
import os
import uuid
import logging

logger = logging.getLogger(__name__)
router = APIRouter()
security = HTTPBearer()


@router.post("/register", response_model=RegisterResponse, status_code=status.HTTP_201_CREATED)
async def register(
    user_data: UserCreate,
    db: AsyncSession = Depends(get_db)
):
    """
    Register a new user
    """
    try:
        user_service = UserService(db)
        user, access_token = await user_service.register_user(
            email=user_data.email,
            password=user_data.password,
            name=user_data.name
        )
        
        return RegisterResponse(
            access_token=access_token,
            token_type="bearer",
            expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
            user=UserResponse.model_validate(user)
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.post("/login", response_model=LoginResponse)
async def login(
    login_data: UserLogin,
    db: AsyncSession = Depends(get_db)
):
    """
    Authenticate user and return access token
    """
    user_service = UserService(db)
    result = await user_service.authenticate_user(
        email=login_data.email,
        password=login_data.password
    )
    
    if not result:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    user, access_token = result
    
    return LoginResponse(
        access_token=access_token,
        token_type="bearer",
        expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        user=UserResponse.model_validate(user)
    )


@router.post("/logout")
async def logout(
    current_user: User = Depends(get_current_user)
):
    """
    Logout current user (stateless).
    """
    return {"message": "Logged out successfully"}


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(
    current_user: User = Depends(get_current_user)
):
    """
    Get current user information
    """
    return UserResponse.model_validate(current_user)


@router.put("/me", response_model=UserResponse)
async def update_current_user(
    user_data: UserUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Update current user information
    """
    user_service = UserService(db)
    updated_user = await user_service.update_user(
        user_id=current_user.id,
        name=user_data.name,
        avatar_url=user_data.avatar_url,
        phone=user_data.phone,
        gender=user_data.gender,
        birth_date=user_data.birth_date,
        city=user_data.city,
        country=user_data.country,
        bio=user_data.bio,
        preferred_language=user_data.preferred_language,
        preferred_currency=user_data.preferred_currency,
        social_accounts=user_data.social_accounts
    )
    
    if not updated_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return UserResponse.model_validate(updated_user)


@router.post("/change-password")
async def change_password(
    password_data: PasswordChange,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Change user password
    """
    user_service = UserService(db)
    
    try:
        await user_service.change_password(
            user_id=current_user.id,
            old_password=password_data.old_password,
            new_password=password_data.new_password
        )
        
        return {"message": "Password changed successfully"}
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/quota", response_model=UserQuotaInfo)
async def get_user_quota(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    获取当前用户配额信息
    """
    quota_service = QuotaService(db)
    quota_info = await quota_service.get_user_quota_info(current_user.id)
    return UserQuotaInfo(**quota_info)


@router.post("/upload-avatar", response_model=UserResponse)
async def upload_avatar(
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    上传用户头像
    """
    # 验证文件类型
    if not file.content_type or not file.content_type.startswith('image/'):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="只支持图片文件"
        )
    
    # 验证文件大小（最大 5MB）
    MAX_FILE_SIZE = 5 * 1024 * 1024
    contents = await file.read()
    if len(contents) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="图片大小不能超过 5MB"
        )
    
    # 生成文件名
    file_extension = file.filename.split('.')[-1] if '.' in file.filename else 'jpg'
    filename = f"avatar_{current_user.id}_{uuid.uuid4().hex[:8]}.{file_extension}"
    
    # 保存到 static/uploads/avatars
    upload_dir = "static/uploads/avatars"
    os.makedirs(upload_dir, exist_ok=True)
    file_path = os.path.join(upload_dir, filename)
    
    with open(file_path, "wb") as f:
        f.write(contents)
    
    avatar_url = f"/static/uploads/avatars/{filename}"
    
    # 更新用户头像 URL
    user_service = UserService(db)
    updated_user = await user_service.update_user(
        user_id=current_user.id,
        avatar_url=avatar_url
    )
    
    logger.info(f"Avatar uploaded for user {current_user.id}: {filename}")
    
    return UserResponse.model_validate(updated_user)
