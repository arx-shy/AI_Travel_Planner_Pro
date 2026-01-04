"""
User Schemas

This module defines Pydantic models for user API requests and responses.
"""

from pydantic import BaseModel, EmailStr, Field
from typing import Optional, Dict
from datetime import datetime
from datetime import date as date_type


# Base user schema
class UserBase(BaseModel):
    """Base user schema"""
    email: EmailStr
    name: str = Field(..., min_length=1, max_length=100)
    membership_level: str = Field(default='free')


# User creation schema
class UserCreate(UserBase):
    """Schema for user registration"""
    password: str = Field(..., min_length=6, max_length=128)


# User login schema
class UserLogin(BaseModel):
    """Schema for user login"""
    email: EmailStr
    password: str


# User update schema
class UserUpdate(BaseModel):
    """Schema for user update"""
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    avatar_url: Optional[str] = Field(None, max_length=500)
    phone: Optional[str] = Field(None, max_length=30)
    gender: Optional[str] = Field(None, pattern="^(male|female|other|unspecified)$")
    birth_date: Optional[date_type] = None
    city: Optional[str] = Field(None, max_length=100)
    country: Optional[str] = Field(None, max_length=100)
    bio: Optional[str] = Field(None, max_length=500)
    preferred_language: Optional[str] = Field(None, max_length=50)
    preferred_currency: Optional[str] = Field(None, max_length=20)
    social_accounts: Optional[Dict[str, str]] = None


# User response schema
class UserResponse(UserBase):
    """Schema for user response"""
    id: int
    is_active: bool
    avatar_url: Optional[str] = None
    phone: Optional[str] = None
    gender: Optional[str] = None
    birth_date: Optional[date_type] = None
    city: Optional[str] = None
    country: Optional[str] = None
    bio: Optional[str] = None
    preferred_language: Optional[str] = None
    preferred_currency: Optional[str] = None
    social_accounts: Optional[Dict[str, str]] = None
    plan_usage_count: int = 0
    copywriter_usage_count: int = 0
    last_quota_reset: Optional[date_type] = None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


# User quota info schema
class UserQuotaInfo(BaseModel):
    """Schema for user quota information"""
    membership_level: str
    plan_usage_count: int
    plan_limit: int  # Free用户: 100, Pro用户: 无限制
    copywriter_usage_count: int
    copywriter_limit: int  # 可以后续配置
    remaining_plans: int
    last_reset: Optional[date_type] = None
    is_pro: bool


# Token response schema
class Token(BaseModel):
    """Schema for token response"""
    access_token: str
    token_type: str = "bearer"
    expires_in: int


# Login response schema
class LoginResponse(BaseModel):
    """Schema for login response"""
    access_token: str
    token_type: str = "bearer"
    expires_in: int
    user: UserResponse


# Register response schema
class RegisterResponse(BaseModel):
    """Schema for register response"""
    access_token: str
    token_type: str = "bearer"
    expires_in: int
    user: UserResponse


# Password change schema
class PasswordChange(BaseModel):
    """Schema for password change"""
    old_password: str
    new_password: str = Field(..., min_length=6, max_length=128)
