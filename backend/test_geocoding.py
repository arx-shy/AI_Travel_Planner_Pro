"""
测试高德地图地理编码服务
"""
import asyncio
import sys
import os
import io

# 设置 UTF-8 编码输出
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# 添加项目根目录到 Python 路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.services.geocoding_service import AMapGeocodingService
from app.core.config import settings


async def test_geocoding():
    """测试地理编码功能"""
    print("=" * 50)
    print("🧪 测试高德地图地理编码服务")
    print("=" * 50)

    # 检查 API Key
    print(f"\n📋 配置检查:")
    print(f"  MAP_API_KEY: {settings.MAP_API_KEY[:20]}...{settings.MAP_API_KEY[-10:] if settings.MAP_API_KEY else 'None'}")

    # 初始化服务
    service = AMapGeocodingService()
    print(f"  服务初始化: ✅")
    print(f"  API Key: {service.api_key[:20]}...{service.api_key[-10:] if service.api_key else 'None'}")

    # 测试地址列表
    test_addresses = [
        ("故宫博物院", "北京"),
        ("外滩", "上海"),
        ("宽窄巷子", "成都"),
        ("天山天池", "新疆"),
    ]

    print(f"\n🔍 开始地理编码测试:")
    print("-" * 50)

    for address, city in test_addresses:
        print(f"\n📍 查询: {address} ({city})")
        result = await service.geocode(address=address, city=city)

        if result:
            print(f"  ✅ 成功!")
            print(f"     经度: {result['lng']}")
            print(f"     纬度: {result['lat']}")
            print(f"     格式化地址: {result['formatted_address']}")
            print(f"     精度: {result['level']}")
        else:
            print(f"  ❌ 失败: 未找到坐标")

    print("\n" + "=" * 50)
    print("✅ 测试完成!")
    print("=" * 50)


if __name__ == "__main__":
    asyncio.run(test_geocoding())
