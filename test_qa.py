"""
QA 对话功能测试脚本
"""

import asyncio
import sys
import os

# 添加项目路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from app.modules.qa.agents.qa_agent import QAAgent
from app.modules.qa.rag.knowledge_base import get_knowledge_base


async def test_qa_agent():
    """测试 QAAgent 对话功能"""
    print("=" * 60)
    print("测试 QAAgent 对话功能")
    print("=" * 60)

    try:
        agent = QAAgent(
            provider="openai",
            temperature=0.7,
            enable_rag=True,
            top_k=4
        )
        print("[OK] QAAgent 初始化成功")
    except Exception as e:
        print(f"[ERROR] QAAgent 初始化失败: {e}")
        return

    test_queries = [
        "北京有什么好玩的景点？",
        "去西藏旅游需要注意什么？",
        "如何规划一次西安旅行？"
    ]

    for query in test_queries:
        print(f"\n{'=' * 60}")
        print(f"用户问题: {query}")
        print(f"{'=' * 60}")

        try:
            response = await agent.chat(query, use_rag=True)
            print(f"AI 回答:\n{response}")
        except Exception as e:
            print(f"[ERROR] 对话失败: {e}")

    print("\n" + "=" * 60)
    print("测试完成")
    print("=" * 60)


async def test_knowledge_base():
    """测试知识库检索功能"""
    print("\n" + "=" * 60)
    print("测试知识库检索功能")
    print("=" * 60)

    try:
        kb = get_knowledge_base()
        print("[OK] 知识库初始化成功")

        # 检查可用的 PDF 文档
        pdfs = kb._list_pdfs()
        print(f"[INFO] 可用的 PDF 文档数: {len(pdfs)}")
        for pdf in pdfs[:5]:
            print(f"   - {pdf.name}")

        # 测试检索
        test_query = "北京"
        print(f"\n[TEST] 测试检索: '{test_query}'")
        retrieval = kb.retrieve(test_query, top_k=3)
        print(f"[OK] 检索到 {len(retrieval.chunks)} 个片段")
        for i, chunk in enumerate(retrieval.chunks[:2], 1):
            preview = chunk.content[:100].replace('\n', ' ')
            print(f"   片段{i}: [{chunk.source}] {preview}...")

    except Exception as e:
        print(f"[ERROR] 知识库测试失败: {e}")
        import traceback
        traceback.print_exc()


async def test_without_llm():
    """测试不依赖 LLM 的回退响应"""
    print("\n" + "=" * 60)
    print("测试回退响应功能 (不使用 LLM)")
    print("=" * 60)

    try:
        agent = QAAgent(
            provider="openai",
            temperature=0.7,
            enable_rag=False
        )

        # 设置 llm_client 为 None 触发回退
        agent.llm_client = None

        query = "帮我规划一次旅行"
        print(f"用户问题: {query}")
        response = await agent.chat(query, use_rag=False)
        print(f"回退响应:\n{response}")

    except Exception as e:
        print(f"[ERROR] 回退测试失败: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("QA 模块功能测试")
    print("=" * 60)

    # 运行测试
    asyncio.run(test_knowledge_base())
    asyncio.run(test_qa_agent())
    asyncio.run(test_without_llm())
