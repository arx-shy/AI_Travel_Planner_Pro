"""
User Settings Schemas
"""

from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, Dict, Any
from datetime import datetime


class UserSettingsBase(BaseModel):
    language: str = Field(default="zh-CN", max_length=10)
    theme: str = Field(default="auto", pattern="^(light|dark|auto)$")
    timezone: str = Field(default="Asia/Shanghai", max_length=50)
    currency: str = Field(default="CNY", max_length=10)
    preferences: Optional[Dict[str, Any]] = None


class UserSettingsUpdate(BaseModel):
    language: Optional[str] = Field(None, max_length=10)
    theme: Optional[str] = Field(None, pattern="^(light|dark|auto)$")
    timezone: Optional[str] = Field(None, max_length=50)
    currency: Optional[str] = Field(None, max_length=10)
    preferences: Optional[Dict[str, Any]] = None


class UserSettingsResponse(UserSettingsBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
