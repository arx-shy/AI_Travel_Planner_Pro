"""
User Settings DAO
"""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.modules.users.models.user_settings import UserSettings


class UserSettingsDAO:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_user_id(self, user_id: int) -> UserSettings | None:
        result = await self.db.execute(
            select(UserSettings).where(UserSettings.user_id == user_id)
        )
        return result.scalars().first()

    async def create(self, settings: UserSettings) -> UserSettings:
        self.db.add(settings)
        await self.db.commit()
        await self.db.refresh(settings)
        return settings

    async def update(self, settings: UserSettings, **kwargs) -> UserSettings:
        for key, value in kwargs.items():
            setattr(settings, key, value)
        await self.db.commit()
        await self.db.refresh(settings)
        return settings
