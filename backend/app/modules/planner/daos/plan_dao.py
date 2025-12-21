"""
Plan Data Access Object (DAO)

Async database operations for travel plans.
"""

from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.modules.planner.models.itinerary import Itinerary


class PlanDAO:
    """
    Data Access Object for Itinerary model.
    """

    def __init__(self, db_session: AsyncSession):
        self.db = db_session

    async def get_user_plans(self, user_id: int, page: int, size: int) -> List[Itinerary]:
        stmt = (
            select(Itinerary)
            .where(Itinerary.user_id == user_id)
            .order_by(Itinerary.created_at.desc())
            .offset((page - 1) * size)
            .limit(size)
        )
        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def get_plan_by_id(self, plan_id: int, user_id: int) -> Optional[Itinerary]:
        stmt = select(Itinerary).where(
            Itinerary.id == plan_id,
            Itinerary.user_id == user_id
        )
        result = await self.db.execute(stmt)
        return result.scalars().first()

    async def update_plan(self, plan_id: int, user_id: int, data: dict) -> Optional[Itinerary]:
        plan = await self.get_plan_by_id(plan_id, user_id)
        if not plan:
            return None

        for key, value in data.items():
            setattr(plan, key, value)

        await self.db.commit()
        await self.db.refresh(plan)
        return plan

    async def delete_plan(self, plan_id: int, user_id: int) -> bool:
        plan = await self.get_plan_by_id(plan_id, user_id)
        if not plan:
            return False

        await self.db.delete(plan)
        await self.db.commit()
        return True
