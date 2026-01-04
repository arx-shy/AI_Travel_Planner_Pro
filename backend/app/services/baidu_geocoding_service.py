"""
百度地图地理编码服务
提供地址解析、逆地理编码、POI搜索等功能
"""

import httpx
import logging
from typing import Optional, Dict, Any, List
from app.core.config.settings import settings

logger = logging.getLogger(__name__)


class BaiduGeocodingService:
    """百度地图API服务"""

    BASE_URL = "http://api.map.baidu.com"

    def __init__(self, api_key: Optional[str] = None):
        """
        初始化百度地图服务

        Args:
            api_key: 百度地图API密钥（AK），如果为None则从配置读取
        """
        self.api_key = api_key or settings.MAP_API_KEY

        if not self.api_key:
            logger.warning("百度地图API密钥未配置，地理编码功能将不可用")

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
            url = f"{self.BASE_URL}/geocoding/v3/"
            params = {
                "address": address,
                "output": "json",
                "ak": self.api_key
            }

            if city:
                params["city"] = city

            logger.info(f"调用百度地图地理编码API: address={address}, city={city}")

            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(url, params=params)
                response.raise_for_status()
                data = response.json()

                logger.debug(f"API响应: status={data.get('status')}")

                if data.get("status") == 0:
                    result = data.get("result", {})
                    location = result.get("location", {})

                    return {
                        "lng": location.get("lng"),
                        "lat": location.get("lat"),
                        "formatted_address": result.get("level", ""),
                        "level": result.get("level", "")
                    }

                logger.warning(f"地址解析失败: {address}, message={data.get('message')}")
                return None

        except httpx.HTTPError as e:
            logger.error(f"百度地图API请求失败: {e}")
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
            如果解析失败返回None
        """
        if not self.api_key:
            logger.error("API密钥未配置")
            return None

        try:
            url = f"{self.BASE_URL}/reverse_geocoding/v3/"
            coords = f"{lng},{lat}"

            params = {
                "location": coords,
                "output": "json",
                "ak": self.api_key
            }

            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(url, params=params)
                response.raise_for_status()
                data = response.json()

                if data.get("status") == 0:
                    result = data.get("result", {})
                    address_component = result.get("addressComponent", {})

                    return {
                        "formatted_address": result.get("formatted_address", ""),
                        "province": address_component.get("province", ""),
                        "city": address_component.get("city", ""),
                        "district": address_component.get("district", ""),
                        "street": address_component.get("street", "")
                    }

                logger.warning(f"逆地理编码失败: {coords}, message={data.get('message')}")
                return None

        except httpx.HTTPError as e:
            logger.error(f"百度地图API请求失败: {e}")
            return None
        except Exception as e:
            logger.error(f"逆地理编码异常: {e}")
            return None

    async def text_search(
        self,
        keywords: str,
        city: Optional[str] = None,
        limit: int = 20
    ) -> List[Dict[str, Any]]:
        """
        POI 搜索：关键字搜索兴趣点

        Args:
            keywords: 搜索关键字
            city: 指定查询的城市（可选）
            limit: 返回结果数量限制

        Returns:
            POI 列表，每个 POI 包含：
            {
                "name": 名称,
                "location": 经纬度,
                "address": 地址,
                "type": 类型
            }
        """
        if not self.api_key:
            logger.error("API密钥未配置")
            return []

        try:
            url = f"{self.BASE_URL}/place/v2/search"
            params = {
                "query": keywords,
                "output": "json",
                "ak": self.api_key,
                "page_size": min(limit, 20)
            }

            if city:
                params["region"] = city

            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(url, params=params)
                response.raise_for_status()
                data = response.json()

                if data.get("status") == 0:
                    results = []
                    for poi in data.get("results", []):
                        location = poi.get("location", {})
                        results.append({
                            "name": poi.get("name", ""),
                            "location": {
                                "lng": float(location.get("lng", 0)),
                                "lat": float(location.get("lat", 0))
                            },
                            "address": poi.get("address", ""),
                            "type": poi.get("detail_info", {}).get("tag", "")
                        })

                    return results

                logger.warning(f"POI搜索失败: {keywords}, message={data.get('message')}")
                return []

        except httpx.HTTPError as e:
            logger.error(f"百度地图API请求失败: {e}")
            return []
        except Exception as e:
            logger.error(f"POI搜索异常: {e}")
            return []

    async def driving_route(
        self,
        origin: Dict[str, float],
        destination: Dict[str, float]
    ) -> Optional[Dict[str, Any]]:
        """
        驾车路径规划

        Args:
            origin: 起点坐标 {"lng": 经度, "lat": 纬度}
            destination: 终点坐标 {"lng": 经度, "lat": 纬度}

        Returns:
            路径信息，包含距离、时间等
        """
        if not self.api_key:
            logger.error("API密钥未配置")
            return None

        try:
            url = f"{self.BASE_URL}/direction/v2/driving"
            origin_str = f"{origin['lng']},{origin['lat']}"
            dest_str = f"{destination['lng']},{destination['lat']}"

            params = {
                "origin": origin_str,
                "destination": dest_str,
                "ak": self.api_key
            }

            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(url, params=params)
                response.raise_for_status()
                data = response.json()

                if data.get("status") == 0:
                    result = data.get("result", {})
                    routes = result.get("routes", [])
                    if routes:
                        return {
                            "distance": routes[0].get("distance", 0),  # 米
                            "duration": routes[0].get("duration", 0),  # 秒
                            "steps": routes[0].get("steps", [])
                        }

                logger.warning(f"路径规划失败: message={data.get('message')}")
                return None

        except httpx.HTTPError as e:
            logger.error(f"百度地图API请求失败: {e}")
            return None
        except Exception as e:
            logger.error(f"路径规划异常: {e}")
            return None
