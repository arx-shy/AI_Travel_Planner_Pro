"""
Plan Data Access Object (DAO)

Async database operations for travel plans.
"""

from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from app.modules.planner.models.itinerary import Itinerary, DayDetail


class PlanDAO:
    """
    Data Access Object for Itinerary and DayDetail models.
    """

    def __init__(self, db_session: AsyncSession):
        self.db = db_session

    async def get_user_plans(self, user_id: int, page: int, size: int) -> List[Itinerary]:
        stmt = (
            select(Itinerary)
            .options(selectinload(Itinerary.days_detail))
            .where(Itinerary.user_id == user_id)
            .order_by(Itinerary.created_at.desc())
            .offset((page - 1) * size)
            .limit(size)
        )
        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def create_plan(self, plan: Itinerary) -> Itinerary:
        self.db.add(plan)
        await self.db.commit()
        await self.db.refresh(plan)
        return plan

    async def get_plan_by_id(self, plan_id: int, user_id: int) -> Optional[Itinerary]:
        stmt = (
            select(Itinerary)
            .options(selectinload(Itinerary.days_detail))
            .where(Itinerary.id == plan_id, Itinerary.user_id == user_id)
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

    async def get_day_details_by_itinerary(self, itinerary_id: int) -> List[DayDetail]:
        """获取指定行程的所有每日详情"""
        stmt = (
            select(DayDetail)
            .where(DayDetail.itinerary_id == itinerary_id)
            .order_by(DayDetail.day_number.asc())
        )
        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def get_day_detail(self, itinerary_id: int, day_number: int) -> Optional[DayDetail]:
        """获取指定行程的指定天的详情"""
        stmt = (
            select(DayDetail)
            .where(
                DayDetail.itinerary_id == itinerary_id,
                DayDetail.day_number == day_number
            )
        )
        result = await self.db.execute(stmt)
        return result.scalars().first()

    async def create_day_detail(self, day_detail: DayDetail) -> DayDetail:
        """创建每日详情"""
        self.db.add(day_detail)
        await self.db.commit()
        await self.db.refresh(day_detail)
        return day_detail

    async def update_day_detail(self, day_detail_id: int, data: dict) -> Optional[DayDetail]:
        """更新每日详情"""
        stmt = select(DayDetail).where(DayDetail.id == day_detail_id)
        result = await self.db.execute(stmt)
        day_detail = result.scalars().first()
        if not day_detail:
            return None

        for key, value in data.items():
            setattr(day_detail, key, value)

        await self.db.commit()
        await self.db.refresh(day_detail)
        return day_detail

    async def delete_day_details(self, itinerary_id: int):
        """删除指定行程的所有每日详情"""
        stmt = select(DayDetail).where(DayDetail.itinerary_id == itinerary_id)
        result = await self.db.execute(stmt)
        for day in result.scalars().all():
            await self.db.delete(day)
        await self.db.commit()

