"""
Subscription Schemas
"""

from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime


class SubscriptionResponse(BaseModel):
    id: int
    user_id: int
    plan_type: str = Field(pattern="^(free|pro|enterprise)$")
    status: str = Field(pattern="^(active|cancelled|expired)$")
    start_date: datetime
    end_date: datetime
    auto_renew: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
