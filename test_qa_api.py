"""
QA 接口测试脚本
"""

import requests
import json
import time

BASE_URL = "http://localhost:8000/api/v1"

# 测试用户数据
test_user = {
    "email": f"test_qa_{int(time.time())}@example.com",
    "password": "Test123456",
    "name": "QA测试用户"
}

def print_section(title):
    """打印分隔线"""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70)

def test_register():
    """测试用户注册"""
    print_section("1. 测试用户注册")

    try:
        response = requests.post(
            f"{BASE_URL}/auth/register",
            json=test_user,
            timeout=10
        )
        print(f"状态码: {response.status_code}")
        data = response.json()
        print(f"响应: {json.dumps(data, ensure_ascii=False, indent=2)}")
        return response.status_code == 201
    except Exception as e:
        print(f"注册失败: {e}")
        return False

def test_login():
    """测试用户登录"""
    print_section("2. 测试用户登录")

    try:
        response = requests.post(
            f"{BASE_URL}/auth/login",
            json={
                "email": test_user["email"],
                "password": test_user["password"]
            },
            timeout=10
        )
        print(f"状态码: {response.status_code}")
        data = response.json()
        print(f"响应: {json.dumps(data, ensure_ascii=False, indent=2)}")

        if response.status_code == 200:
            return data.get("access_token")
        return None
    except Exception as e:
        print(f"登录失败: {e}")
        return None

def test_create_session(token):
    """测试创建QA会话"""
    print_section("3. 测试创建QA会话")

    headers = {"Authorization": f"Bearer {token}"}

    try:
        response = requests.post(
            f"{BASE_URL}/qa/sessions",
            json={
                "title": "旅游咨询",
                "features": {
                    "knowledge_base": True,
                    "weather": False,
                    "voice": True
                }
            },
            headers=headers,
            timeout=10
        )
        print(f"状态码: {response.status_code}")
        data = response.json()
        print(f"响应: {json.dumps(data, ensure_ascii=False, indent=2)}")

        if response.status_code == 200:
            return data.get("data", {}).get("session", {}).get("id")
        return None
    except Exception as e:
        print(f"创建会话失败: {e}")
        return None

def test_send_message(token, session_id):
    """测试发送消息"""
    print_section("4. 测试发送消息")

    headers = {"Authorization": f"Bearer {token}"}

    try:
        response = requests.post(
            f"{BASE_URL}/qa/messages",
            json={
                "session_id": session_id,
                "content": "北京有什么好玩的景点？",
                "message_type": "text"
            },
            headers=headers,
            timeout=30
        )
        print(f"状态码: {response.status_code}")
        data = response.json()
        print(f"响应: {json.dumps(data, ensure_ascii=False, indent=2)}")

        return response.status_code == 200
    except Exception as e:
        print(f"发送消息失败: {e}")
        return False

def test_chat_history(token, session_id):
    """测试获取对话历史"""
    print_section("5. 测试获取对话历史")

    headers = {"Authorization": f"Bearer {token}"}

    try:
        response = requests.get(
            f"{BASE_URL}/qa/sessions/{session_id}/messages",
            headers=headers,
            timeout=10
        )
        print(f"状态码: {response.status_code}")
        data = response.json()
        print(f"响应: {json.dumps(data, ensure_ascii=False, indent=2)}")

        return response.status_code == 200
    except Exception as e:
        print(f"获取历史失败: {e}")
        return False

def test_weather_query(token):
    """测试天气查询"""
    print_section("6. 测试天气查询")

    headers = {"Authorization": f"Bearer {token}"}

    try:
        response = requests.get(
            f"{BASE_URL}/qa/weather/北京",
            headers=headers,
            timeout=10
        )
        print(f"状态码: {response.status_code}")
        print(f"响应: {json.dumps(response.json(), ensure_ascii=False, indent=2)}")

        return response.status_code == 200
    except Exception as e:
        print(f"天气查询失败: {e}")
        return False

def main():
    """主测试函数"""
    print("\n" + "=" * 70)
    print("  QA 模块 API 接口测试")
    print("=" * 70)
    print(f"  测试用户: {test_user['email']}")

    token = None
    session_id = None

    # 1. 注册用户
    if not test_register():
        print("\n[ERROR] 用户注册失败，终止测试")
        return

    # 2. 登录获取token
    token = test_login()
    if not token:
        print("\n[ERROR] 用户登录失败，终止测试")
        return
    print(f"\n[OK] 获取到Token: {token[:50]}...")

    # 3. 创建会话
    session_id = test_create_session(token)
    if not session_id:
        print("\n[ERROR] 创建会话失败，终止测试")
        return
    print(f"\n[OK] 创建会话成功，ID: {session_id}")

    # 4. 发送消息
    if not test_send_message(token, session_id):
        print("\n[WARN] 发送消息失败，继续测试其他功能")

    # 5. 获取对话历史
    if not test_chat_history(token, session_id):
        print("\n[WARN] 获取历史失败，继续测试其他功能")

    # 6. 天气查询
    if not test_weather_query(token):
        print("\n[WARN] 天气查询失败")

    print("\n" + "=" * 70)
    print("  测试完成")
    print("=" * 70)
    print(f"\n  测试用户: {test_user['email']}")
    print(f"  Token: {token[:50]}..." if token else "  Token: 未获取")
    print(f"  会话ID: {session_id}" if session_id else "  会话ID: 未创建")
    print("")

if __name__ == "__main__":
    main()
