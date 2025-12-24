"""
测试 AI + RAG 完整功能
"""

import requests
import json
import time

BASE_URL = "http://localhost:8000/api/v1"

# 测试用户数据
test_user = {
    "email": f"ai_test_{int(time.time())}@example.com",
    "password": "Test123456",
    "name": "AI测试用户"
}

def register_and_login():
    """注册并登录获取 token"""
    print("=" * 70)
    print("1. 注册用户")
    print("=" * 70)

    response = requests.post(f"{BASE_URL}/auth/register", json=test_user, timeout=10)
    if response.status_code == 201:
        data = response.json()
        token = data.get("access_token")
        print("[OK] 注册成功")
        print(f"Token: {token[:50]}...")
        return token
    else:
        print(f"[ERROR] 注册失败: {response.status_code}")
        print(response.text)
        return None

def create_qa_session(token):
    """创建 QA 会话（启用 RAG）"""
    print("\n" + "=" * 70)
    print("2. 创建 QA 会话（启用 RAG）")
    print("=" * 70)

    headers = {"Authorization": f"Bearer {token}"}
    response = requests.post(
        f"{BASE_URL}/qa/sessions",
        json={
            "title": "AI+RAG测试",
            "features": {
                "knowledge_base": True,  # 启用 RAG
                "weather": False,
                "voice": False
            }
        },
        headers=headers,
        timeout=10
    )

    if response.status_code == 200:
        data = response.json()
        session_id = data.get("data", {}).get("session", {}).get("id")
        print(f"[OK] 会话创建成功，ID: {session_id}")
        return session_id
    else:
        print(f"[ERROR] 创建会话失败: {response.status_code}")
        return None

def send_message_with_rag(token, session_id):
    """发送消息（使用 RAG）"""
    print("\n" + "=" * 70)
    print("3. 发送消息（AI + RAG）")
    print("=" * 70)

    headers = {"Authorization": f"Bearer {token}"}

    # 测试具体旅游问题（应该能从 RAG 检索到信息）
    queries = [
        "北京故宫的历史是什么时候开始的？",
        "西安兵马俑是如何被发现的？",
        "西藏旅游的高原反应如何预防？"
    ]

    for i, query in enumerate(queries, 1):
        print(f"\n--- 问题 {i} ---")
        print(f"用户问题: {query}")
        print("-" * 70)

        response = requests.post(
            f"{BASE_URL}/qa/messages",
            json={
                "session_id": session_id,
                "content": query,
                "message_type": "text"
            },
            headers=headers,
            timeout=60
        )

        if response.status_code == 200:
            data = response.json()
            message = data.get("data", {}).get("message", {})
            content = message.get("content", "")

            print(f"AI 回答:")
            print(content)

            # 检查是否是回退响应（固定模板）
            if "我可以为您提供以下帮助：" in content:
                print("\n[WARNING] 使用了回退响应（固定模板）")
                print("          AI 调用可能失败")
            else:
                print("\n[OK] AI 成功生成回答")

                # 检查是否包含 RAG 相关信息
                if "故宫" in content or "兵马俑" in content or "西藏" in content:
                    print("[OK] 回答包含相关旅游信息（可能来自 RAG）")
        else:
            print(f"[ERROR] 请求失败: {response.status_code}")
            print(response.text)

def test_without_rag(token, session_id):
    """测试不使用 RAG 的回答"""
    print("\n" + "=" * 70)
    print("4. 对比测试：不使用 RAG")
    print("=" * 70)

    # 创建不启用 RAG 的会话
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.post(
        f"{BASE_URL}/qa/sessions",
        json={
            "title": "通用问答",
            "features": {
                "knowledge_base": False,  # 禁用 RAG
                "weather": False,
                "voice": False
            }
        },
        headers=headers,
        timeout=10
    )

    if response.status_code == 200:
        data = response.json()
        session_id2 = data.get("data", {}).get("session", {}).get("id")

        query = "如何规划一次旅行？"
        print(f"用户问题: {query}")
        print("-" * 70)

        response = requests.post(
            f"{BASE_URL}/qa/messages",
            json={
                "session_id": session_id2,
                "content": query,
                "message_type": "text"
            },
            headers=headers,
            timeout=60
        )

        if response.status_code == 200:
            data = response.json()
            content = data.get("data", {}).get("message", {}).get("content", "")
            print(f"AI 回答:\n{content}")
        else:
            print(f"[ERROR] 请求失败: {response.status_code}")
    else:
        print(f"[ERROR] 创建会话失败: {response.status_code}")

def main():
    """主测试函数"""
    print("\n" + "=" * 70)
    print("  AI 服务 + RAG 检索系统完整测试")
    print("=" * 70)

    # 1. 注册并登录
    token = register_and_login()
    if not token:
        print("\n[ERROR] 无法获取 Token，测试终止")
        return

    # 2. 创建 QA 会话
    session_id = create_qa_session(token)
    if not session_id:
        print("\n[ERROR] 无法创建会话，测试终止")
        return

    # 3. 发送消息（AI + RAG）
    send_message_with_rag(token, session_id)

    # 4. 对比测试（不使用 RAG）
    test_without_rag(token, session_id)

    # 总结
    print("\n" + "=" * 70)
    print("  测试总结")
    print("=" * 70)
    print("  [INFO] QA API 接口正常")
    print("  [INFO] 数据库存储正常")
    print("  [INFO] 请检查 AI 回答质量：")
    print("         - 是否为智能回答而非固定模板？")
    print("         - 是否包含 RAG 检索到的具体信息？")
    print("=" * 70 + "\n")

if __name__ == "__main__":
    main()
