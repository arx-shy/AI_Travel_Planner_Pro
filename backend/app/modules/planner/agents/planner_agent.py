"""
Travel Planner Agent

This module contains AI agent responsible for generating travel itineraries.
It uses LLM to create intelligent, personalized travel plans.
"""

from typing import List, Dict, Any, Optional
from app.core.ai.factory import LLMFactory
from app.core.config.settings import settings
from langchain.schema import HumanMessage, SystemMessage
from app.modules.planner.prompts.planning_prompts import (
    PLANNING_SYSTEM_PROMPT,
    STRICT_JSON_OUTPUT,
    FLEXIBLE_JSON_OUTPUT,
    CULTURAL_PROMPT,
    ADVENTURE_PROMPT,
    FOODIE_PROMPT,
    LEISURE_PROMPT
)
import logging
import json

logger = logging.getLogger(__name__)


class TravelPlannerAgent:
    """
    AI agent for travel planning.
    Generates intelligent travel itineraries based on user preferences.
    """

    def __init__(self, use_strict_json: bool = True):
        """
        Initialize planner agent.

        Args:
            use_strict_json: Whether to use strict JSON output format
        """
        self.use_strict_json = use_strict_json
        self.llm = LLMFactory.create_client(
            provider="minimax",
            model_name="MiniMax-M2.1",
            temperature=0.7
        )

    def _get_style_prompt(self, travel_style: str) -> str:
        """Get style-specific prompt"""
        style_prompts = {
            "leisure": LEISURE_PROMPT,
            "adventure": ADVENTURE_PROMPT,
            "foodie": FOODIE_PROMPT,
            "cultural": CULTURAL_PROMPT
        }
        return style_prompts.get(travel_style, "")

    def _parse_ai_response(self, response: str) -> List[Dict[str, Any]]:
        """
        Parse AI response into structured data.

        Args:
            response: Raw AI response

        Returns:
            List of daily itinerary data
        """
        if self.use_strict_json:
            try:
                data = json.loads(response)
                if isinstance(data, dict) and "days" in data:
                    return data["days"]
                elif isinstance(data, list):
                    return data
                else:
                    logger.warning("Invalid JSON structure, trying flexible parse")
                    return self._flexible_parse(response)
            except json.JSONDecodeError:
                logger.warning("JSON decode error, using flexible parse")
                return self._flexible_parse(response)
        else:
            return self._flexible_parse(response)

    def _flexible_parse(self, response: str) -> List[Dict[str, Any]]:
        """
        Flexible parsing for non-JSON responses.
        Extracts day structure from text.
        """
        days = []
        current_day = None
        lines = response.split('\n')

        for line in lines:
            line = line.strip()
            if not line:
                continue

            # 识别"第X天"模式
            if '第' in line and ('天' in line or 'Day' in line):
                if current_day:
                    days.append(current_day)
                day_num = len(days) + 1
                current_day = {
                    "day_number": day_num,
                    "title": line.strip(),
                    "activities": [],
                    "notes": ""
                }
            # 识别时间模式 (09:00, 09:30等)
            elif ':' in line and current_day:
                current_day["activities"].append({
                    "time": line[:5],
                    "title": line[5:].strip(),
                    "description": "",
                    "location": "",
                    "duration": "1小时",
                    "cost": 0,
                    "tips": []
                })

        if current_day:
            days.append(current_day)

        return days

    async def generate_itinerary(
        self,
        destination: str,
        days: int,
        budget: float,
        travel_style: str,
        departure: str = None,
        preferences: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """
        Generate a travel itinerary using AI.

        Args:
            destination: Travel destination
            days: Number of days
            budget: Budget in CNY
            travel_style: Travel style (leisure, adventure, foodie)
            departure: Departure location
            preferences: Additional preferences

        Returns:
            Generated itinerary data with daily details
        """
        # Prepare user input
        user_input = f"""
请为{destination}制定一个{days}天的旅行计划。

目的地：{destination}
出发地：{departure or '未指定'}
天数：{days}
预算：¥{budget if budget else '不限'}
旅行风格：{travel_style}
偏好：{preferences or '无特殊要求'}

要求：
1. 每天安排合理，避免过于紧凑
2. 推荐当地特色景点和美食
3. 考虑交通便利性
4. 控制在预算范围内
5. 提供实用提示（开放时间、票价等）
"""

        # Get style-specific prompt
        style_prompt = self._get_style_prompt(travel_style)

        # Add JSON output requirement if strict mode
        if self.use_strict_json:
            user_input += "\n\n" + STRICT_JSON_OUTPUT
        else:
            user_input += "\n\n" + FLEXIBLE_JSON_OUTPUT

        # Build system message with style
        system_content = PLANNING_SYSTEM_PROMPT
        if style_prompt:
            system_content += "\n\n" + style_prompt

        # Generate itinerary
        messages = [
            SystemMessage(content=system_content),
            HumanMessage(content=user_input)
        ]

        try:
            response = await LLMFactory.agenerate(self.llm, messages)
            logger.info(f"AI response received, length: {len(response)}")

            # Parse response into daily itinerary
            days_data = self._parse_ai_response(response)

            # Calculate total cost estimate
            total_cost = 0
            for day in days_data:
                for activity in day.get("activities", []):
                    total_cost += activity.get("cost", 0)

            return {
                "title": f"{destination} {days}日游",
                "destination": destination,
                "days": days,
                "budget": budget,
                "travel_style": travel_style,
                "days_data": days_data,
                "total_cost": total_cost,
                "generated_content": response,
                "ai_generated": True
            }
        except Exception as e:
            logger.error(f"Error generating itinerary: {str(e)}")
            raise

    async def optimize_itinerary(
        self,
        current_itinerary: Dict[str, Any],
        feedback: str,
        affected_days: List[int] = None,
        use_strict_json: bool = None
    ) -> Dict[str, Any]:
        """
        Optimize an existing itinerary based on user feedback.

        Args:
            current_itinerary: Current itinerary data
            feedback: User feedback for optimization
            affected_days: List of day numbers to optimize
            use_strict_json: Override strict_json setting

        Returns:
            Optimized itinerary
        """
        strict_mode = use_strict_json if use_strict_json is not None else self.use_strict_json

        # Build optimization prompt
        prompt = f"""
用户对以下行程不满意，需要根据反馈进行优化：

当前行程：
{json.dumps(current_itinerary, ensure_ascii=False, indent=2)}

用户反馈：
{feedback}

需要优化的天数：{', '.join(map(str, affected_days)) if affected_days else '全部'}

请根据用户反馈重新生成或修改这些天的行程，保持其他天数不变。
"""

        if strict_mode:
            prompt += "\n\n" + STRICT_JSON_OUTPUT

        messages = [
            SystemMessage(content=PLANNING_SYSTEM_PROMPT),
            HumanMessage(content=prompt)
        ]

        try:
            response = await LLMFactory.agenerate(self.llm, messages)
            logger.info(f"Optimization response received")

            # Parse optimization result
            days_data = self._parse_ai_response(response)

            return {
                "days_data": days_data,
                "generated_content": response,
                "ai_generated": True
            }
        except Exception as e:
            logger.error(f"Error optimizing itinerary: {str(e)}")
            raise
