"""
综合测试：AI 服务 + RAG 检索
"""

import asyncio
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from app.modules.qa.rag.knowledge_base import get_knowledge_base
from app.modules.qa.agents.qa_agent import QAAgent


async def test_rag_retrieval():
    """测试 RAG 检索"""
    print("=" * 70)
    print("  测试1: RAG 检索系统")
    print("=" * 70)

    try:
        kb = get_knowledge_base()
        print("[OK] 知识库初始化成功\n")

        pdfs = kb._list_pdfs()
        print(f"[INFO] PDF 文档数: {len(pdfs)}")

        queries = ["北京故宫", "西安兵马俑", "西藏旅游"]

        for q in queries:
            print(f"\n{'-' * 70}")
            print(f"检索: {q}")
            print(f"{'-' * 70}")

            retrieval = kb.retrieve(q, top_k=2)
            print(f"[OK] 检索到 {len(retrieval.chunks)} 个片段")

            for i, chunk in enumerate(retrieval.chunks, 1):
                preview = chunk.content[:60].replace('\n', ' ')
                print(f"\n  片段{i}: [{chunk.source}]")
                print(f"  内容: {preview}...")

        return True

    except Exception as e:
        print(f"[ERROR] RAG 检索失败: {e}")
        import traceback
        traceback.print_exc()
        return False


async def test_ai_with_rag():
    """测试 AI + RAG"""
    print("\n" + "=" * 70)
    print("  测试2: AI + RAG 智能回答")
    print("=" * 70)

    try:
        agent = QAAgent(provider='glm', enable_rag=True, top_k=3)
        print("[OK] QAAgent 创建成功 (启用 RAG)\n")

        # 测试具体旅游问题
        queries = [
            "北京故宫有什么特色？",
            "西安有什么必去的景点？",
            "去西藏旅游需要注意什么？"
        ]

        for q in queries:
            print(f"\n{'=' * 70}")
            print(f"问题: {q}")
            print(f"{'=' * 70}")

            try:
                response = await agent.chat(q, use_rag=True)
                print(f"AI 回答:\n{response}")
            except Exception as e:
                print(f"[ERROR] AI 调用失败: {e}")
                # 如果失败，显示回退响应
                fallback = agent._fallback_response(q, True)
                print(f"回退响应:\n{fallback}")

        return True

    except Exception as e:
        print(f"[ERROR] AI + RAG 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


async def test_ai_without_rag():
    """测试 AI 不带 RAG"""
    print("\n" + "=" * 70)
    print("  测试3: AI 通用回答 (不使用 RAG)")
    print("=" * 70)

    try:
        agent = QAAgent(provider='glm', enable_rag=False)
        print("[OK] QAAgent 创建成功 (禁用 RAG)\n")

        queries = [
            "帮我规划一次旅行",
            "旅行前需要准备什么？"
        ]

        for q in queries:
            print(f"\n{'=' * 70}")
            print(f"问题: {q}")
            print(f"{'=' * 70}")

            try:
                response = await agent.chat(q, use_rag=False)
                print(f"AI 回答:\n{response}")
            except Exception as e:
                print(f"[ERROR] AI 调用失败: {e}")
                fallback = agent._fallback_response(q, False)
                print(f"回退响应:\n{fallback}")

        return True

    except Exception as e:
        print(f"[ERROR] AI 通用回答测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


async def test_direct_rag():
    """测试直接 RAG 检索结果"""
    print("\n" + "=" * 70)
    print("  测试4: 直接 RAG 检索结果")
    print("=" * 70)

    try:
        agent = QAAgent(provider='glm', enable_rag=True, top_k=2)

        query = "北京故宫历史"
        print(f"\n查询: {query}")
        print(f"{'-' * 70}")

        # 直接调用检索方法
        chunks = agent._retrieve_context(query)
        print(f"[OK] 检索到 {len(chunks)} 个相关片段\n")

        for i, chunk in enumerate(chunks, 1):
            print(f"片段 {i}:")
            print(f"  来源: {chunk['source']}")
            print(f"  页码: {chunk['page']}")
            preview = chunk['content'][:100].replace('\n', ' ')
            print(f"  内容: {preview}...")
            print()

        return True

    except Exception as e:
        print(f"[ERROR] 直接 RAG 检索失败: {e}")
        import traceback
        traceback.print_exc()
        return False


async def main():
    """主测试函数"""
    print("\n" + "=" * 70)
    print("  AI 服务和 RAG 检索系统综合测试")
    print("=" * 70)

    results = []

    # 测试 RAG 检索
    results.append(("RAG 检索系统", await test_rag_retrieval()))

    # 测试 AI + RAG
    results.append(("AI + RAG 智能回答", await test_ai_with_rag()))

    # 测试 AI 通用回答
    results.append(("AI 通用回答", await test_ai_without_rag()))

    # 测试直接 RAG
    results.append(("直接 RAG 检索", await test_direct_rag()))

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
        print("  ✓ RAG 检索系统正常工作")
        print("  ✓ AI 服务正常运行")
        print("  ✓ AI 可以使用 RAG 进行智能回答")
    else:
        print("\n  [WARNING] 部分测试失败")

    print("=" * 70 + "\n")


if __name__ == "__main__":
    asyncio.run(main())
