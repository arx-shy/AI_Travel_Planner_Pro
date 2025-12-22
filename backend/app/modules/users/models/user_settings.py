"""
User Settings Model
"""

from sqlalchemy import Column, Integer, String, Enum, ForeignKey, JSON
from app.core.db.base import BaseModel


class UserSettings(BaseModel):
    __tablename__ = "user_settings"

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, unique=True, index=True)
    language = Column(String(10), default="zh-CN", nullable=False)
    theme = Column(
        Enum("light", "dark", "auto", name="user_theme_modes"),
        default="auto",
        nullable=False
    )
    timezone = Column(String(50), default="Asia/Shanghai", nullable=False)
    currency = Column(String(10), default="CNY", nullable=False)
    preferences = Column(JSON, nullable=True)
