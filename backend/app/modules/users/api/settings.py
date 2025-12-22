"""
User Settings & Subscription Routes
"""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.db.session import get_db
from app.core.security.deps import get_current_user
from app.modules.users.services.user_service import UserService
from app.modules.users.schemas.user_settings import UserSettingsResponse, UserSettingsUpdate
from app.modules.users.schemas.subscription import SubscriptionResponse
from app.modules.users.models.user import User

router = APIRouter()


@router.get("/settings", response_model=UserSettingsResponse)
async def get_user_settings(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = UserService(db)
    settings = await service.get_or_create_settings(current_user.id)
    return UserSettingsResponse.model_validate(settings)


@router.put("/settings", response_model=UserSettingsResponse)
async def update_user_settings(
    payload: UserSettingsUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = UserService(db)
    settings = await service.update_settings(current_user.id, **payload.model_dump(exclude_unset=True))
    return UserSettingsResponse.model_validate(settings)


@router.get("/subscription", response_model=SubscriptionResponse)
async def get_user_subscription(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = UserService(db)
    subscription = await service.get_or_create_subscription(current_user.id)
    return SubscriptionResponse.model_validate(subscription)
