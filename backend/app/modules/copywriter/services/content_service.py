"""
Copywriter Content Service
"""

from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.modules.copywriter.daos.content_dao import ContentDAO
from app.modules.copywriter.models.content import Content
from app.modules.copywriter.schemas.content_schema import ContentCreate


class ContentService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.content_dao = ContentDAO(db)

    async def generate_content(self, user_id: int, payload: ContentCreate) -> Content:
        keywords = ", ".join(payload.keywords or [])
        platform = payload.platform or "xiaohongshu"
        output = f"{platform} 文案示例：围绕 {keywords or '旅行'} 的一段内容。"
        content = Content(
            user_id=user_id,
            content_type="copywriting",
            platform=platform,
            output_content=output,
            input_data=payload.model_dump(),
        )
        return await self.content_dao.create(content)

    async def list_contents(self, user_id: int, page: int, size: int) -> List[Content]:
        return await self.content_dao.list_by_user(user_id, page, size)

    async def rate_content(self, user_id: int, content_id: int, rating: int) -> Optional[Content]:
        content = await self.content_dao.get_by_id(content_id, user_id)
        if not content:
            return None
        return await self.content_dao.update(content, rating=rating)
