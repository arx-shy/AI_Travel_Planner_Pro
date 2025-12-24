"""
测试 AI 服务和 RAG 检索系统
"""

import asyncio
import sys
import os

# 添加项目路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from app.modules.qa.rag.knowledge_base import get_knowledge_base
from app.modules.qa.agents.qa_agent import QAAgent


async def test_rag_retrieval():
    """测试 RAG 检索功能"""
    print("=" * 70)
    print("  测试1: RAG 检索系统")
    print("=" * 70)

    try:
        kb = get_knowledge_base()
        print("[OK] 知识库初始化成功\n")

        # 检查可用的 PDF 文档
        pdfs = kb._list_pdfs()
        print(f"[INFO] 可用的 PDF 文档数: {len(pdfs)}")

        test_queries = [
            "北京",
            "西安有什么好玩的",
            "西藏旅游注意事项"
        ]

        for query in test_queries:
            print(f"\n{'-' * 70}")
            print(f"检索查询: {query}")
            print(f"{'-' * 70}")

            retrieval = kb.retrieve(query, top_k=3)
            print(f"[OK] 检索到 {len(retrieval.chunks)} 个片段")

            for i, chunk in enumerate(retrieval.chunks, 1):
                preview = chunk.content[:80].replace('\n', ' ')
                print(f"\n  片段{i}: [{chunk.source} 第{chunk.page}页]")
                print(f"  内容预览: {preview}...")

        return True

    except Exception as e:
        print(f"[ERROR] RAG 检索测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


async def test_ai_with_rag():
    """测试 AI 带 RAG 的回答"""
    print("\n" + "=" * 70)
    print("  测试2: AI + RAG 智能回答")
    print("=" * 70)

    try:
        # 创建启用 RAG 的 agent
        agent = QAAgent(
            provider="openai",
            temperature=0.7,
            enable_rag=True,
            top_k=4
        )
        print("[OK] QAAgent 创建成功 (启用 RAG)\n")

        test_queries = [
            "北京故宫有什么特色？",
            "西安兵马俑是什么时候发现的？",
            "去西藏需要准备什么？"
        ]

        for query in test_queries:
            print(f"\n{'-' * 70}")
            print(f"用户问题: {query}")
            print(f"{'-' * 70}")

            response = await agent.chat(query, use_rag=True)
            print(f"AI 回答:\n{response}\n")

        return True

    except Exception as e:
        print(f"[ERROR] AI + RAG 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


async def test_ai_without_rag():
    """测试 AI 不带 RAG 的回答（对比）"""
    print("\n" + "=" * 70)
    print("  测试3: AI 通用回答 (不使用 RAG)")
    print("=" * 70)

    try:
        # 创建禁用 RAG 的 agent
        agent = QAAgent(
            provider="openai",
            temperature=0.7,
            enable_rag=False
        )
        print("[OK] QAAgent 创建成功 (禁用 RAG)\n")

        test_queries = [
            "北京故宫有什么特色？",
            "如何规划一次旅行？"
        ]

        for query in test_queries:
            print(f"\n{'-' * 70}")
            print(f"用户问题: {query}")
            print(f"{'-' * 70}")

            response = await agent.chat(query, use_rag=False)
            print(f"AI 回答:\n{response}\n")

        return True

    except Exception as e:
        print(f"[ERROR] AI 不带 RAG 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


async def test_rag_vs_no_rag_comparison():
    """对比测试：带 RAG vs 不带 RAG"""
    print("\n" + "=" * 70)
    print("  测试4: RAG vs 非RAG 对比")
    print("=" * 70)

    try:
        # 两个 agent
        agent_with_rag = QAAgent(
            provider="openai",
            temperature=0.7,
            enable_rag=True,
            top_k=3
        )
        agent_without_rag = QAAgent(
            provider="openai",
            temperature=0.7,
            enable_rag=False
        )

        query = "北京有什么必去的景点？"

        print(f"\n{'=' * 70}")
        print(f"统一问题: {query}")
        print(f"{'=' * 70}\n")

        print("[使用 RAG 检索]")
        print(f"{'-' * 70}")
        response_with_rag = await agent_with_rag.chat(query, use_rag=True)
        print(response_with_rag)

        print("\n\n[不使用 RAG 检索]")
        print(f"{'-' * 70}")
        response_without_rag = await agent_without_rag.chat(query, use_rag=False)
        print(response_without_rag)

        print("\n" + "=" * 70)
        print("  对比分析")
        print("=" * 70)
        print("使用 RAG 的回答应该包含更多具体的、")
        print("来自知识库的详细信息，而通用回答则更加泛化。")

        return True

    except Exception as e:
        print(f"[ERROR] 对比测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


async def main():
    """主测试函数"""
    print("\n" + "=" * 70)
    print("  AI 服务和 RAG 检索系统综合测试")
    print("=" * 70)

    results = []

    # 测试1: RAG 检索
    results.append(("RAG 检索", await test_rag_retrieval()))

    # 测试2: AI + RAG
    results.append(("AI + RAG", await test_ai_with_rag()))

    # 测试3: AI 通用回答
    results.append(("AI 通用回答", await test_ai_without_rag()))

    # 测试4: 对比
    results.append(("RAG 对比", await test_rag_vs_no_rag_comparison()))

    # 总结
    print("\n" + "=" * 70)
    print("  测试总结")
    print("=" * 70)

    for name, result in results:
        status = "[OK]" if result else "[FAIL]"
        print(f"  {status} {name}")

    all_passed = all(result for _, result in results)

    if all_passed:
        print("\n  [SUCCESS] 所有测试通过！")
        print("  AI 服务正常运行")
        print("  RAG 检索系统正常工作")
        print("  AI 可以使用 RAG 进行智能回答")
    else:
        print("\n  [WARNING] 部分测试失败")

    print("=" * 70 + "\n")


if __name__ == "__main__":
    asyncio.run(main())
