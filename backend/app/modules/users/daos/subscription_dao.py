"""
Subscription DAO
"""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.modules.users.models.subscription import Subscription


class SubscriptionDAO:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_user_id(self, user_id: int) -> Subscription | None:
        result = await self.db.execute(
            select(Subscription).where(Subscription.user_id == user_id)
        )
        return result.scalars().first()

    async def create(self, subscription: Subscription) -> Subscription:
        self.db.add(subscription)
        await self.db.commit()
        await self.db.refresh(subscription)
        return subscription

    async def update(self, subscription: Subscription, **kwargs) -> Subscription:
        for key, value in kwargs.items():
            setattr(subscription, key, value)
        await self.db.commit()
        await self.db.refresh(subscription)
        return subscription
