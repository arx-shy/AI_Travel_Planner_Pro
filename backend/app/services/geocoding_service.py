"""
高德地图地理编码服务
提供地址解析、逆地理编码、路径规划等功能
支持高德地图 API 安全密钥签名认证
"""

import httpx
import hashlib
import logging
from typing import Optional, Dict, Any, List
from urllib.parse import urlencode
from app.core.config.settings import settings

logger = logging.getLogger(__name__)


class AMapGeocodingService:
    """高德地图API服务（支持安全密钥）"""

    BASE_URL = "https://restapi.amap.com"

    def __init__(self, api_key: Optional[str] = None, secret_key: Optional[str] = None):
        """
        初始化高德地图服务

        Args:
            api_key: 高德地图API密钥，如果为None则从配置读取
            secret_key: 高德地图安全密钥，如果为None则从配置读取
        """
        self.api_key = api_key or settings.MAP_API_KEY
        self.secret_key = secret_key or settings.MAP_SECRET_KEY

        if not self.api_key:
            logger.warning("高德地图API密钥未配置，地理编码功能将不可用")

        if not self.secret_key:
            logger.info("未配置安全密钥，将尝试不使用签名调用API")

    def _generate_signature(self, params: Dict[str, str]) -> str:
        """
        生成高德地图 API 签名

        Args:
            params: 请求参数（不包含 key 和 sig）

        Returns:
            MD5 签名值
        """
        if not self.secret_key:
            return ""

        # 1. 对所有参数按字母顺序排序
        sorted_params = sorted(params.items())

        # 2. 拼接参数字符串
        param_str = "&".join([f"{k}={v}" for k, v in sorted_params])

        # 3. 在末尾加上安全密钥
        sign_str = param_str + self.secret_key

        # 4. 计算 MD5 哈希值
        md5 = hashlib.md5()
        md5.update(sign_str.encode('utf-8'))
        signature = md5.hexdigest()

        logger.debug(f"签名原文: {sign_str}")
        logger.debug(f"签名结果: {signature}")

        return signature

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
                "address": address
            }

            if city:
                params["city"] = city

            # 添加签名
            if self.secret_key:
                sig = self._generate_signature(params)
                params["sig"] = sig

            # 添加 key
            params["key"] = self.api_key

            logger.info(f"调用地理编码API: address={address}, city={city}")

            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(url, params=params)
                response.raise_for_status()
                data = response.json()

                logger.debug(f"API响应: status={data.get('status')}, info={data.get('info')}")

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

                logger.warning(f"地址解析失败: {address}, info={data.get('info')}, infocode={data.get('infocode')}")
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
            如果解析失败返回None
        """
        if not self.api_key:
            logger.error("API密钥未配置")
            return None

        try:
            url = f"{self.BASE_URL}/v3/geocode/regeo"
            location = f"{lng},{lat}"
            params = {
                "location": location,
                "extensions": "base"  # 返回基本信息
            }

            # 添加签名
            if self.secret_key:
                sig = self._generate_signature(params)
                params["sig"] = sig

            params["key"] = self.api_key

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
                        "street": address_component.get("streetNumber", {}).get("street", "")
                    }

                logger.warning(f"逆地理编码失败: {location}, info={data.get('info')}")
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
            url = f"{self.BASE_URL}/v5/place/text"
            params = {
                "keywords": keywords,
                "offset": limit
            }

            if city:
                params["city"] = city

            # 添加签名
            if self.secret_key:
                sig = self._generate_signature(params)
                params["sig"] = sig

            params["key"] = self.api_key

            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(url, params=params)
                response.raise_for_status()
                data = response.json()

                if data.get("status") == "1" and data.get("pois"):
                    results = []
                    for poi in data["pois"]:
                        location = poi.get("location", "")
                        lng, lat = 0.0, 0.0
                        if "," in location:
                            lng_str, lat_str = location.split(",")
                            lng, lat = float(lng_str), float(lat_str)

                        results.append({
                            "name": poi.get("name", ""),
                            "location": {"lng": lng, "lat": lat},
                            "address": poi.get("address", ""),
                            "type": poi.get("type", "")
                        })

                    return results

                logger.warning(f"POI搜索失败: {keywords}, info={data.get('info')}")
                return []

        except httpx.HTTPError as e:
            logger.error(f"高德地图API请求失败: {e}")
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
            url = f"{self.BASE_URL}/v5/direction/driving"
            origin_str = f"{origin['lng']},{origin['lat']}"
            dest_str = f"{destination['lng']},{destination['lat']}"

            params = {
                "origin": origin_str,
                "destination": dest_str
            }

            # 添加签名
            if self.secret_key:
                sig = self._generate_signature(params)
                params["sig"] = sig

            params["key"] = self.api_key

            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(url, params=params)
                response.raise_for_status()
                data = response.json()

                if data.get("status") == "1" and data.get("route"):
                    route = data["route"]
                    paths = route.get("paths", [])
                    if paths:
                        return {
                            "distance": paths[0].get("distance", 0),  # 米
                            "duration": paths[0].get("duration", 0),  # 秒
                            "steps": paths[0].get("steps", [])
                        }

                logger.warning(f"路径规划失败: info={data.get('info')}")
                return None

        except httpx.HTTPError as e:
            logger.error(f"高德地图API请求失败: {e}")
            return None
        except Exception as e:
            logger.error(f"路径规划异常: {e}")
            return None
