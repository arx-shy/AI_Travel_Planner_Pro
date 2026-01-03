"""
高德地图地理编码服务
提供地址解析、逆地理编码、路径规划等功能
"""

import httpx
from typing import Optional, Dict, Any, List
from app.core.config import settings
from app.core.logging import logger


class AMapGeocodingService:
    """高德地图API服务"""

    BASE_URL = "https://restapi.amap.com"

    def __init__(self, api_key: Optional[str] = None):
        """
        初始化高德地图服务

        Args:
            api_key: 高德地图API密钥，如果为None则从配置读取
        """
        self.api_key = api_key or settings.AMAP_API_KEY
        if not self.api_key:
            logger.warning("高德地图API密钥未配置，地理编码功能将不可用")

    async def geocode(self, address: str, city: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """
        地址解析：将结构化地址转换为经纬度坐标

        Args:
            address: 待解析的结构化地址描述
            city: 指定查询的城市（可选）

        Returns:
            包含经纬度信息的字典，格式：
            {
                "lng": 经度,
                "lat": 纬度,
                "formatted_address": 格式化地址,
                "level": 地址精度
            }
            如果解析失败返回None
        """
        if not self.api_key:
            logger.error("API密钥未配置")
            return None

        try:
            url = f"{self.BASE_URL}/v3/geocode/geo"
            params = {
                "key": self.api_key,
                "address": address
            }

            if city:
                params["city"] = city

            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(url, params=params)
                response.raise_for_status()
                data = response.json()

                if data.get("status") == "1" and data.get("geocodes"):
                    geocode = data["geocodes"][0]
                    location = geocode.get("location", "")
                    if "," in location:
                        lng, lat = location.split(",")
                        return {
                            "lng": float(lng),
                            "lat": float(lat),
                            "formatted_address": geocode.get("formatted_address", ""),
                            "level": geocode.get("level", "")
                        }

                logger.warning(f"地址解析失败: {address}")
                return None

        except httpx.HTTPError as e:
            logger.error(f"高德地图API请求失败: {e}")
            return None
        except Exception as e:
            logger.error(f"地理编码异常: {e}")
            return None

    async def regeocode(self, lng: float, lat: float) -> Optional[Dict[str, Any]]:
        """
        逆地理编码：将经纬度坐标转换为结构化地址

        Args:
            lng: 经度
            lat: 纬度

        Returns:
            包含地址信息的字典，格式：
            {
                "formatted_address": 格式化地址,
                "province": 省份,
                "city": 城市,
                "district": 区县,
                "street": 街道
            }
        """
        if not self.api_key:
            logger.error("API密钥未配置")
            return None

        try:
            url = f"{self.BASE_URL}/v3/geocode/regeo"
            params = {
                "key": self.api_key,
                "location": f"{lng},{lat}",
                "extensions": "base"  # base: 基本信息; all: 详细信息
            }

            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(url, params=params)
                response.raise_for_status()
                data = response.json()

                if data.get("status") == "1" and data.get("regeocode"):
                    regeocode = data["regeocode"]
                    address_component = regeocode.get("addressComponent", {})

                    return {
                        "formatted_address": regeocode.get("formatted_address", ""),
                        "province": address_component.get("province", ""),
                        "city": address_component.get("city", ""),
                        "district": address_component.get("district", ""),
                        "street": address_component.get("township", ""),
                        "street_number": address_component.get("streetNumber", "")
                    }

                logger.warning(f"逆地理编码失败: {lng}, {lat}")
                return None

        except httpx.HTTPError as e:
            logger.error(f"高德地图API请求失败: {e}")
            return None
        except Exception as e:
            logger.error(f"逆地理编码异常: {e}")
            return None

    async def text_search(
        self,
        keywords: str,
        city: Optional[str] = None,
        city_limit: bool = False
    ) -> List[Dict[str, Any]]:
        """
        关键字搜索：搜索POI（兴趣点）

        Args:
            keywords: 搜索关键字
            city: 指定搜索城市（可选）
            city_limit: 是否限制在指定城市内搜索

        Returns:
            POI列表，每个元素包含：
            {
                "name": 名称,
                "lng": 经度,
                "lat": 纬度,
                "address": 地址,
                "type": 类型
            }
        """
        if not self.api_key:
            logger.error("API密钥未配置")
            return []

        try:
            url = f"{self.BASE_URL}/v5/place/text"
            params = {
                "key": self.api_key,
                "keywords": keywords,
                "show_fields": "business,photos"
            }

            if city:
                params["city"] = city
            if city_limit:
                params["citylimit"] = "true"

            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(url, params=params)
                response.raise_for_status()
                data = response.json()

                if data.get("status") == "1" and data.get("pois"):
                    results = []
                    for poi in data["pois"]:
                        location = poi.get("location", "")
                        if "," in location:
                            lng, lat = location.split(",")
                            results.append({
                                "name": poi.get("name", ""),
                                "lng": float(lng),
                                "lat": float(lat),
                                "address": poi.get("address", ""),
                                "type": poi.get("type", ""),
                                "biz_type": poi.get("biz_type", ""),
                                "photos": poi.get("photos", [])
                            })
                    return results

                logger.warning(f"POI搜索失败: {keywords}")
                return []

        except httpx.HTTPError as e:
            logger.error(f"高德地图API请求失败: {e}")
            return []
        except Exception as e:
            logger.error(f"POI搜索异常: {e}")
            return []

    async def get_driving_route(
        self,
        origin: str,  # "经度,纬度"
        destination: str,  # "经度,纬度"
        strategy: int = 0
    ) -> Optional[Dict[str, Any]]:
        """
        驾车路径规划

        Args:
            origin: 起点坐标 "经度,纬度"
            destination: 终点坐标 "经度,纬度"
            strategy: 路径规划策略
                0: 速度优先
                1: 费用优先
                2: 距离优先

        Returns:
            路径信息，格式：
            {
                "distance": 总距离(米),
                "duration": 预计时间(秒),
                "steps": 路段列表,
                "polyline": 路径编码
            }
        """
        if not self.api_key:
            logger.error("API密钥未配置")
            return None

        try:
            url = f"{self.BASE_URL}/v5/direction/driving"
            params = {
                "key": self.api_key,
                "origin": origin,
                "destination": destination,
                "strategy": strategy
            }

            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(url, params=params)
                response.raise_for_status()
                data = response.json()

                if data.get("status") == "1" and data.get("route"):
                    route = data["route"]
                    paths = route.get("paths", [])
                    if paths:
                        path = paths[0]
                        return {
                            "distance": path.get("distance", 0),  # 米
                            "duration": path.get("duration", 0),  # 秒
                            "strategy": path.get("strategy", ""),
                            "tolls": path.get("tolls", 0),  # 过路费
                            "toll_distance": path.get("toll_distance", 0),  # 收费里程
                            "steps": path.get("steps", [])
                        }

                logger.warning(f"路径规划失败: {origin} -> {destination}")
                return None

        except httpx.HTTPError as e:
            logger.error(f"高德地图API请求失败: {e}")
            return None
        except Exception as e:
            logger.error(f"路径规划异常: {e}")
            return None

    async def get_walking_route(
        self,
        origin: str,
        destination: str
    ) -> Optional[Dict[str, Any]]:
        """
        步行路径规划

        Args:
            origin: 起点坐标 "经度,纬度"
            destination: 终点坐标 "经度,纬度"

        Returns:
            路径信息
        """
        if not self.api_key:
            logger.error("API密钥未配置")
            return None

        try:
            url = f"{self.BASE_URL}/v5/direction/walking"
            params = {
                "key": self.api_key,
                "origin": origin,
                "destination": destination
            }

            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(url, params=params)
                response.raise_for_status()
                data = response.json()

                if data.get("status") == "1" and data.get("route"):
                    route = data["route"]
                    paths = route.get("paths", [])
                    if paths:
                        path = paths[0]
                        return {
                            "distance": path.get("distance", 0),
                            "duration": path.get("duration", 0),
                            "steps": path.get("steps", [])
                        }

                logger.warning(f"步行路径规划失败: {origin} -> {destination}")
                return None

        except httpx.HTTPError as e:
            logger.error(f"高德地图API请求失败: {e}")
            return None
        except Exception as e:
            logger.error(f"步行路径规划异常: {e}")
            return None

    async def batch_geocode(self, addresses: List[str], city: Optional[str] = None) -> List[Optional[Dict[str, Any]]]:
        """
        批量地址解析

        Args:
            addresses: 地址列表
            city: 指定查询的城市（可选）

        Returns:
            经纬度信息列表，顺序与输入一致
        """
        results = []
        for address in addresses:
            result = await self.geocode(address, city)
            results.append(result)
        return results

    async def enrich_itinerary_with_coordinates(
        self,
        itinerary_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        为行程数据添加地理坐标信息

        Args:
            itinerary_data: 行程数据，格式：
                {
                    "destination": 目的地,
                    "days": [
                        {
                            "day_number": 1,
                            "activities": [
                                {
                                    "title": "活动名称",
                                    "location": "地址",
                                    ...
                                }
                            ]
                        }
                    ]
                }

        Returns:
            添加了coordinates字段的行程数据
        """
        destination = itinerary_data.get("destination", "")
        days = itinerary_data.get("days", [])

        enriched_days = []

        for day_plan in days:
            activities = day_plan.get("activities", [])
            enriched_activities = []

            for activity in activities:
                location = activity.get("location", "")

                # 尝试获取经纬度
                coordinates = None
                if location:
                    # 先尝试在该城市下搜索
                    geo_result = await self.geocode(location, city=destination)
                    if not geo_result:
                        # 如果失败，尝试不指定城市
                        geo_result = await self.geocode(location)

                    if geo_result:
                        coordinates = {
                            "lng": geo_result["lng"],
                            "lat": geo_result["lat"]
                        }

                enriched_activity = {
                    **activity,
                    "coordinates": coordinates
                }
                enriched_activities.append(enriched_activity)

            enriched_days.append({
                **day_plan,
                "activities": enriched_activities
            })

        return {
            **itinerary_data,
            "days": enriched_days
        }


# 创建全局实例
geocoding_service = AMapGeocodingService()
