"""
Weather tool for QA module.
"""

from __future__ import annotations

from collections import defaultdict
from typing import Optional
import logging

import httpx

logger = logging.getLogger(__name__)


async def query_weather(city: str) -> dict:
    """Query real weather data via Open-Meteo (no API key required)."""
    if not city:
        raise ValueError("City is required")

    geocode_url = "https://geocoding-api.open-meteo.com/v1/search"
    forecast_url = "https://api.open-meteo.com/v1/forecast"
    timeout = httpx.Timeout(15.0, connect=8.0)

    try:
        async with httpx.AsyncClient(timeout=timeout, follow_redirects=True) as client:
            geo_resp = await client.get(geocode_url, params={
                "name": city,
                "count": 1,
                "language": "zh",
                "format": "json"
            })
            geo_resp.raise_for_status()
            geo_data = geo_resp.json()
            results = geo_data.get("results") or []
            if not results:
                raise ValueError("City not found")

            location = results[0]
            latitude = location.get("latitude")
            longitude = location.get("longitude")
            location_name = location.get("name") or city

            if latitude is None or longitude is None:
                raise ValueError("City not found")

            forecast_resp = await client.get(forecast_url, params={
                "latitude": latitude,
                "longitude": longitude,
                "daily": "weathercode,temperature_2m_max,temperature_2m_min,wind_speed_10m_max",
                "hourly": "relativehumidity_2m",
                "timezone": "auto",
                "forecast_days": 3
            })
            forecast_resp.raise_for_status()
            forecast_data = forecast_resp.json()

        daily = forecast_data.get("daily") or {}
        hourly = forecast_data.get("hourly") or {}

        daily_dates = daily.get("time") or []
        daily_codes = daily.get("weathercode") or []
        daily_max = daily.get("temperature_2m_max") or []
        daily_min = daily.get("temperature_2m_min") or []
        daily_wind = daily.get("wind_speed_10m_max") or []

        hourly_times = hourly.get("time") or []
        hourly_humidity = hourly.get("relativehumidity_2m") or []

        humidity_by_date = defaultdict(list)
        for time_str, humidity in zip(hourly_times, hourly_humidity):
            date_key = time_str.split("T")[0]
            if humidity is not None:
                humidity_by_date[date_key].append(humidity)

        forecast = []
        for index, date_str in enumerate(daily_dates):
            code = daily_codes[index] if index < len(daily_codes) else None
            desc = _weather_desc_from_code(code)
            humidity_values = humidity_by_date.get(date_str, [])
            humidity_avg = round(sum(humidity_values) / len(humidity_values)) if humidity_values else 0
            forecast.append({
                "date": date_str,
                "weather": desc,
                "weather_code": code,
                "temp_high": round(daily_max[index]) if index < len(daily_max) else 0,
                "temp_low": round(daily_min[index]) if index < len(daily_min) else 0,
                "humidity": humidity_avg,
                "wind": round(daily_wind[index]) if index < len(daily_wind) else 0
            })

        if not forecast:
            raise RuntimeError("Weather data unavailable")

        return {"city": location_name, "forecast": forecast}
    except Exception as exc:
        logger.error("Weather query failed for city=%s: %s", city, exc, exc_info=True)
        raise RuntimeError("Weather service unavailable") from exc


def _weather_desc_from_code(code: Optional[int]) -> str:
    if code is None:
        return "未知"
    mapping = {
        0: "晴",
        1: "多云",
        2: "多云",
        3: "阴",
        45: "雾",
        48: "雾",
        51: "小雨",
        53: "小雨",
        55: "小雨",
        56: "冻雨",
        57: "冻雨",
        61: "中雨",
        63: "中雨",
        65: "大雨",
        66: "冻雨",
        67: "冻雨",
        71: "小雪",
        73: "中雪",
        75: "大雪",
        77: "雪",
        80: "阵雨",
        81: "阵雨",
        82: "暴雨",
        85: "阵雪",
        86: "阵雪",
        95: "雷阵雨",
        96: "雷阵雨",
        99: "雷阵雨"
    }
    return mapping.get(code, "未知")
