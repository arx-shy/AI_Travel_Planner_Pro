"""
Subscription Model
"""

from datetime import datetime
from sqlalchemy import Column, Integer, Enum, Boolean, DateTime, ForeignKey, func
from app.core.db.base import BaseModel


class Subscription(BaseModel):
    __tablename__ = "subscriptions"

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    plan_type = Column(
        Enum("free", "pro", "enterprise", name="subscription_plan_types"),
        default="free",
        nullable=False
    )
    status = Column(
        Enum("active", "cancelled", "expired", name="subscription_statuses"),
        default="active",
        nullable=False
    )
    start_date = Column(DateTime, default=func.now(), nullable=False)
    end_date = Column(DateTime, nullable=False)
    auto_renew = Column(Boolean, default=False, nullable=False)
