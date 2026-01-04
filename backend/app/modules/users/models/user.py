"""
User Model

This module defines the User database model using SQLAlchemy.
"""

from sqlalchemy import Column, Integer, String, Boolean, Enum, DateTime, Date, JSON, func
from sqlalchemy.orm import relationship
from app.core.db.base import Base


class User(Base):
    """
    User model
    
    Attributes:
        id: Primary key
        email: User email (unique)
        hashed_password: Hashed password
        name: User full name
        is_active: Whether the user account is active
        membership_level: User membership level (free/pro)
        avatar_url: User avatar URL
        plan_usage_count: Number of plans generated this month
        copywriter_usage_count: Number of copywriting generated this month
        last_quota_reset: Last date when usage quota was reset
        created_at: Account creation timestamp
        updated_at: Last update timestamp
    """
    __tablename__ = "users"

    # Primary key
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    
    # Required fields
    email = Column(String(255), unique=True, index=True, nullable=False, comment="User email")
    hashed_password = Column(String(255), nullable=False, comment="Hashed password")
    name = Column(String(100), nullable=False, comment="User full name")
    
    # Optional fields
    is_active = Column(Boolean, default=True, nullable=False, comment="Account status")
    membership_level = Column(
        Enum('free', 'pro', name='membership_levels'),
        default='free',
        nullable=False,
        comment="Membership level"
    )
    
    # Usage tracking fields
    avatar_url = Column(String(500), nullable=True, comment="User avatar URL")
    phone = Column(String(30), nullable=True, comment="User phone number")
    gender = Column(String(20), nullable=True, comment="User gender")
    birth_date = Column(Date, nullable=True, comment="User birth date")
    city = Column(String(100), nullable=True, comment="User city")
    country = Column(String(100), nullable=True, comment="User country")
    bio = Column(String(500), nullable=True, comment="User bio")
    preferred_language = Column(String(50), nullable=True, comment="Preferred language")
    preferred_currency = Column(String(20), nullable=True, comment="Preferred currency")
    social_accounts = Column(JSON, nullable=True, comment="Social accounts")
    plan_usage_count = Column(Integer, default=0, nullable=False, comment="Number of plans generated this month")
    copywriter_usage_count = Column(Integer, default=0, nullable=False, comment="Number of copywriting generated this month")
    last_quota_reset = Column(Date, nullable=True, comment="Last date when usage quota was reset")
    
    # Timestamps
    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
        comment="Account creation time"
    )
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
        comment="Last update time"
    )
    
    # Relationships
    # Example: itineraries = relationship("Itinerary", back_populates="user")
