"""
Plan Service

This module contains business logic for travel planning.
"""

from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.modules.planner.daos.plan_dao import PlanDAO
from app.modules.planner.schemas.plan_schema import PlanCreate, PlanUpdate, PlanResponse
from app.modules.planner.models.itinerary import Itinerary, DayDetail
from fastapi import HTTPException

import logging

logger = logging.getLogger(__name__)


class PlanService:
    """
    Service class for travel plan business logic.
    """

    def __init__(self, db_session: AsyncSession):
        self.plan_dao = PlanDAO(db_session)

    async def generate_itinerary(self, user_id: int, itinerary_data: PlanCreate, use_strict_json: bool = True) -> PlanResponse:
        """
        生成行程（仅创建基础行程，不生成详细日程）
        """
        itinerary = Itinerary(
            user_id=user_id,
            title=itinerary_data.title,
            destination=itinerary_data.destination,
            departure=itinerary_data.departure,
            days=itinerary_data.days,
            budget=itinerary_data.budget,
            travel_style=itinerary_data.travel_style,
            status="draft",
            ai_generated=False,
            metadata_json={},
        )
        itinerary = await self.plan_dao.create_plan(itinerary)
        return PlanResponse.model_validate(itinerary)

    async def generate_detailed_itinerary(
        self,
        user_id: int,
        itinerary_id: int,
        use_strict_json: bool = True
    ) -> PlanResponse:
        """
        使用AI生成详细行程

        Args:
            user_id: 用户ID
            itinerary_id: 行程ID
            use_strict_json: 是否使用严格JSON格式

        Returns:
            包含详细日程的行程响应
        """
        from app.modules.planner.agents.planner_agent import TravelPlannerAgent

        # 获取基础行程
        itinerary = await self.plan_dao.get_plan_by_id(itinerary_id, user_id)
        if not itinerary:
            raise HTTPException(status_code=404, detail="Itinerary not found")

        logger.info(f"开始生成详细行程: {itinerary.destination} {itinerary.days}天, use_strict_json={use_strict_json}")

        # 调用AI生成详细行程
        agent = TravelPlannerAgent(use_strict_json=use_strict_json)
        result = await agent.generate_itinerary(
            destination=itinerary.destination,
            days=itinerary.days,
            budget=float(itinerary.budget) if itinerary.budget else 0,
            travel_style=itinerary.travel_style,
            departure=itinerary.departure
        )

        # 清除旧的DayDetail数据
        await self.plan_dao.delete_day_details(itinerary_id)
        logger.info(f"已清除旧的日程数据")

        # 创建新的DayDetail记录
        days_data = result.get('days_data', [])
        logger.info(f"AI返回{len(days_data)}天的数据")

        for day_data in days_data:
            day_detail = DayDetail(
                itinerary_id=itinerary_id,
                day_number=day_data.get('day_number'),
                title=day_data.get('title'),
                activities=day_data.get('activities', []),
                notes=day_data.get('notes')
            )
            await self.plan_dao.create_day_detail(day_detail)
            logger.info(f"已创建第{day_data.get('day_number')}天的日程")

        # 更新行程状态
        updated_itinerary = await self.plan_dao.update_plan(
            itinerary_id,
            user_id,
            {
                "status": "active",
                "ai_generated": True,
                "metadata_json": {
                    "total_cost": result.get('total_cost', 0)
                }
            }
        )

        logger.info(f"详细行程生成完成，行程ID: {itinerary_id}")
        return PlanResponse.model_validate(updated_itinerary)

    async def optimize_itinerary(
        self,
        user_id: int,
        itinerary_id: int,
        feedback: str,
        affected_days: Optional[List[int]] = None,
        use_strict_json: bool = True
    ) -> PlanResponse:
        """
        根据用户反馈优化行程

        Args:
            user_id: 用户ID
            itinerary_id: 行程ID
            feedback: 用户反馈
            affected_days: 需要优化的天数列表
            use_strict_json: 是否使用严格JSON格式

        Returns:
            优化后的行程
        """
        from app.modules.planner.agents.planner_agent import TravelPlannerAgent

        # 获取当前行程
        current_itinerary = await self.plan_dao.get_plan_by_id(itinerary_id, user_id)
        if not current_itinerary:
            raise HTTPException(status_code=404, detail="Itinerary not found")

        # 获取当前的所有日程数据
        current_days = await self.plan_dao.get_day_details_by_itinerary(itinerary_id)
        logger.info(f"当前行程有{len(current_days)}天的数据")

        # 调用AI优化
        agent = TravelPlannerAgent(use_strict_json=use_strict_json)

        # 构建当前行程数据（包含用户反馈）
        optimization_data = {
            "title": current_itinerary.title,
            "destination": current_itinerary.destination,
            "days": current_itinerary.days,
            "budget": float(current_itinerary.budget) if current_itinerary.budget else 0,
            "travel_style": current_itinerary.travel_style,
            "days_data": [
                {
                    "day_number": day.day_number,
                    "title": day.title,
                    "activities": day.activities,
                    "notes": day.notes
                }
                for day in current_days
            ]
        }

        result = await agent.optimize_itinerary(
            current_itinerary=optimization_data,
            feedback=feedback,
            affected_days=affected_days
        )

        # 更新受影响的天数
        optimized_days = result.get('days_data', [])
        for day_data in optimized_days:
            day_number = day_data.get('day_number')

            # 如果指定了受影响的天数，只更新这些天
            if affected_days and day_number not in affected_days:
                continue

            # 更新或创建DayDetail
            existing_day = await self.plan_dao.get_day_detail(itinerary_id, day_number)
            if existing_day:
                await self.plan_dao.update_day_detail(existing_day.id, {
                    "title": day_data.get('title'),
                    "activities": day_data.get('activities', []),
                    "notes": day_data.get('notes')
                })
                logger.info(f"已更新第{day_number}天的数据")
            else:
                day_detail = DayDetail(
                    itinerary_id=itinerary_id,
                    day_number=day_number,
                    title=day_data.get('title'),
                    activities=day_data.get('activities', []),
                    notes=day_data.get('notes')
                )
                await self.plan_dao.create_day_detail(day_detail)
                logger.info(f"已创建第{day_number}天的数据")

        logger.info(f"行程优化完成，行程ID: {itinerary_id}")
        updated_itinerary = await self.plan_dao.get_plan_by_id(itinerary_id, user_id)
        return PlanResponse.model_validate(updated_itinerary)

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
