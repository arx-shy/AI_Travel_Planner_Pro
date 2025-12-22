"""
Plan Service

This module contains business logic for travel planning.
"""

from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.modules.planner.daos.plan_dao import PlanDAO
from app.modules.planner.schemas.plan_schema import PlanCreate, PlanUpdate, PlanResponse
from app.modules.planner.models.itinerary import Itinerary

import logging

logger = logging.getLogger(__name__)


class PlanService:
    """
    Service class for travel plan business logic.
    """

    def __init__(self, db_session: AsyncSession):
        self.plan_dao = PlanDAO(db_session)

    async def generate_itinerary(self, user_id: int, itinerary_data: PlanCreate) -> PlanResponse:
        itinerary = Itinerary(
            user_id=user_id,
            title=itinerary_data.title,
            destination=itinerary_data.destination,
            departure=itinerary_data.departure,
            days=itinerary_data.days,
            budget=itinerary_data.budget,
            travel_style=itinerary_data.travel_style,
            status="draft",
            ai_generated=True,
            metadata_json={},
        )
        itinerary = await self.plan_dao.create_plan(itinerary)
        return PlanResponse.model_validate(itinerary)

    async def get_user_itineraries(
        self,
        user_id: int,
        page: int,
        size: int
    ) -> List[PlanResponse]:
        plans = await self.plan_dao.get_user_plans(user_id, page, size)
        return [PlanResponse.model_validate(plan) for plan in plans]

    async def get_itinerary(self, itinerary_id: int, user_id: int) -> Optional[PlanResponse]:
        plan = await self.plan_dao.get_plan_by_id(itinerary_id, user_id)
        if not plan:
            return None
        return PlanResponse.model_validate(plan)

    async def update_itinerary(
        self,
        itinerary_id: int,
        user_id: int,
        itinerary_data: PlanUpdate
    ) -> Optional[PlanResponse]:
        plan = await self.plan_dao.update_plan(
            itinerary_id,
            user_id,
            itinerary_data.model_dump(exclude_unset=True)
        )
        if not plan:
            return None
        return PlanResponse.model_validate(plan)

    async def delete_itinerary(self, itinerary_id: int, user_id: int) -> bool:
        return await self.plan_dao.delete_plan(itinerary_id, user_id)
