"""
Copywriter Content DAO
"""

from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.modules.copywriter.models.content import Content


class ContentDAO:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, content: Content) -> Content:
        self.db.add(content)
        await self.db.commit()
        await self.db.refresh(content)
        return content

    async def list_by_user(self, user_id: int, page: int, size: int) -> List[Content]:
        stmt = (
            select(Content)
            .where(Content.user_id == user_id)
            .order_by(Content.created_at.desc())
            .offset((page - 1) * size)
            .limit(size)
        )
        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def get_by_id(self, content_id: int, user_id: int) -> Optional[Content]:
        result = await self.db.execute(
            select(Content).where(Content.id == content_id, Content.user_id == user_id)
        )
        return result.scalars().first()

    async def update(self, content: Content, **kwargs) -> Content:
        for key, value in kwargs.items():
            setattr(content, key, value)
        await self.db.commit()
        await self.db.refresh(content)
        return content
