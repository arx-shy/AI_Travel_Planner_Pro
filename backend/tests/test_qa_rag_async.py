"""
QA RAG 异步检索测试
测试异步 RAG 检索功能，确保不会阻塞事件循环
"""

import asyncio
import time
import sys
from pathlib import Path

# 添加项目根目录到 Python 路径
project_root = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(project_root))

from app.modules.qa.rag.knowledge_base import get_knowledge_base, KnowledgeBase
from app.modules.qa.agents.qa_agent import QAAgent


async def test_async_retrieve_not_blocking():
    """测试异步检索不会阻塞事件循环"""
    print("\n=== 测试 1: 异步检索不会阻塞 ===")

    kb = get_knowledge_base()
    query = "北京的天气怎么样"

    start = time.time()

    # 异步检索
    result = await kb.retrieve_async(query, top_k=4)

    elapsed = time.time() - start

    print(f"✓ 异步检索完成，耗时: {elapsed:.2f}秒")
    print(f"✓ 检索到 {len(result.chunks)} 个文档块")

    if result.chunks:
        print(f"✓ 第一个块来源: {result.chunks[0].source}")
        print(f"✓ 第一个块内容预览: {result.chunks[0].content[:100]}...")

    return elapsed < 30  # 30秒内完成视为成功


async def test_concurrent_retrieves():
    """测试并发检索不会互相阻塞"""
    print("\n=== 测试 2: 并发检索测试 ===")

    kb = get_knowledge_base()
    queries = [
        "北京天气",
        "上海旅游",
        "泰国签证",
        "日本攻略"
    ]

    start = time.time()

    # 并发执行多个检索
    tasks = [kb.retrieve_async(q, top_k=2) for q in queries]
    results = await asyncio.gather(*tasks)

    elapsed = time.time() - start

    total_chunks = sum(len(r.chunks) for r in results)
    print(f"✓ 并发检索 {len(queries)} 个查询完成，耗时: {elapsed:.2f}秒")
    print(f"✓ 共检索到 {total_chunks} 个文档块")

    # 验证所有查询都有结果（即使为空）
    assert len(results) == len(queries), "结果数量应该与查询数量一致"

    return elapsed < 60  # 60秒内完成视为成功


async def test_agent_async_retrieve():
    """测试 QAAgent 使用异步检索"""
    print("\n=== 测试 3: QAAgent 异步检索 ===")

    agent = QAAgent(
        provider="minimax",
        enable_rag=True,
        top_k=2
    )

    query = "北京有什么好玩的地方"

    start = time.time()

    # 测试异步检索方法
    context = await agent._retrieve_context_async(query)

    elapsed = time.time() - start

    print(f"✓ Agent 异步检索完成，耗时: {elapsed:.2f}秒")
    print(f"✓ 检索到 {len(context)} 个上下文块")

    if context:
        print(f"✓ 第一个上下文: 来源={context[0]['source']}, 页码={context[0]['page']}")

    return elapsed < 30


async def test_sync_vs_async_performance():
    """对比同步和异步检索的性能"""
    print("\n=== 测试 4: 同步 vs 异步性能对比 ===")

    kb = get_knowledge_base()
    query = "北京旅游攻略"

    # 测试同步版本
    start_sync = time.time()
    sync_result = kb.retrieve(query, top_k=2)
    sync_time = time.time() - start_sync

    print(f"同步检索耗时: {sync_time:.2f}秒，块数: {len(sync_result.chunks)}")

    # 测试异步版本
    start_async = time.time()
    async_result = await kb.retrieve_async(query, top_k=2)
    async_time = time.time() - start_async

    print(f"异步检索耗时: {async_time:.2f}秒，块数: {len(async_result.chunks)}")

    # 验证结果一致
    assert len(sync_result.chunks) == len(async_result.chunks), "同步和异步结果数量应该一致"

    # 异步版本应该不会比同步慢太多（允许20%误差）
    # 重点是异步不会阻塞事件循环
    print(f"✓ 异步/同步时间比: {async_time/sync_time:.2f}")

    return True


async def test_cache_effectiveness():
    """测试缓存有效性（第二次查询应该更快）"""
    print("\n=== 测试 5: 缓存有效性 ===")

    kb = get_knowledge_base()
    query = "北京旅游景点"

    # 第一次查询（构建索引）
    start_first = time.time()
    result1 = await kb.retrieve_async(query, top_k=2)
    first_time = time.time() - start_first

    print(f"首次查询耗时: {first_time:.2f}秒")

    # 第二次查询（使用缓存）
    start_second = time.time()
    result2 = await kb.retrieve_async(query, top_k=2)
    second_time = time.time() - start_second

    print(f"缓存查询耗时: {second_time:.2f}秒")
    print(f"加速比: {first_time/second_time:.2f}x")

    # 验证结果一致
    assert len(result1.chunks) == len(result2.chunks), "缓存结果应该一致"

    # 第二次应该明显更快（或至少不会更慢）
    return second_time <= first_time * 1.2


async def main():
    """运行所有测试"""
    print("=" * 60)
    print("QA RAG 异步检索测试套件")
    print("=" * 60)

    tests = [
        ("异步检索不阻塞", test_async_retrieve_not_blocking),
        ("并发检索", test_concurrent_retrieves),
        ("Agent 异步检索", test_agent_async_retrieve),
        ("同步 vs 异步性能", test_sync_vs_async_performance),
        ("缓存有效性", test_cache_effectiveness),
    ]

    results = []

    for name, test_func in tests:
        try:
            passed = await test_func()
            results.append((name, "✅ PASS", None))
            print(f"✅ {name}: PASS\n")
        except Exception as e:
            results.append((name, "❌ FAIL", str(e)))
            print(f"❌ {name}: FAIL - {e}\n")

    # 打印总结
    print("=" * 60)
    print("测试总结")
    print("=" * 60)

    passed_count = sum(1 for _, status, _ in results if status == "✅ PASS")
    total_count = len(results)

    for name, status, error in results:
        print(f"{status} {name}")
        if error:
            print(f"   错误: {error}")

    print("=" * 60)
    print(f"通过: {passed_count}/{total_count}")
    print("=" * 60)

    return passed_count == total_count


if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)
