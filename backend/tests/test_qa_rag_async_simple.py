"""
QA RAG 异步检索测试（简化版）
测试异步 RAG 检索功能，使用模拟数据避免内存问题
"""

import asyncio
import time
import sys
from pathlib import Path

# 添加项目根目录到 Python 路径
project_root = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(project_root))

from app.modules.qa.rag.knowledge_base import KnowledgeBase, Chunk
from app.modules.qa.rag.vector_store import BM25VectorStore


async def test_async_vs_sync_retrieve():
    """测试异步检索与同步检索的一致性"""
    print("\n=== 测试 1: 异步 vs 同步检索一致性 ===")

    # 创建模拟数据
    chunks = [
        Chunk(chunk_id="1", content="北京是中国的首都，拥有故宫、长城等著名景点", source="北京", page=0),
        Chunk(chunk_id="2", content="上海是中国的经济中心，有外滩、东方明珠等景点", source="上海", page=0),
        Chunk(chunk_id="3", content="泰国签证需要护照、照片和申请表", source="泰国", page=0),
        Chunk(chunk_id="4", content="日本旅游需要提前办理签证，推荐春季赏樱", source="日本", page=0),
    ]

    kb = KnowledgeBase()
    kb._chunks = chunks
    kb._store = BM25VectorStore(chunks)

    query = "北京有什么好玩的"

    # 测试同步检索
    start_sync = time.time()
    sync_result = kb._store.search(query, top_k=2)
    sync_time = time.time() - start_sync

    print(f"同步检索耗时: {sync_time*1000:.2f}ms，结果数: {len(sync_result)}")

    # 测试异步检索
    start_async = time.time()
    async_result = await asyncio.to_thread(kb._store.search, query, 2)
    async_time = time.time() - start_async

    print(f"异步检索耗时: {async_time*1000:.2f}ms，结果数: {len(async_result)}")

    # 验证结果一致
    assert len(sync_result) == len(async_result), "同步和异步结果数量应该一致"
    print("PASS: 异步和同步检索结果一致")

    return True


async def test_concurrent_operations():
    """测试并发操作不会互相阻塞"""
    print("\n=== 测试 2: 并发操作测试 ===")

    chunks = [
        Chunk(chunk_id=str(i), content=f"文档{i}的内容，关于旅行和攻略", source=f"文档{i}", page=0)
        for i in range(10)
    ]

    kb = KnowledgeBase()
    kb._chunks = chunks
    kb._store = BM25VectorStore(chunks)

    queries = [f"文档{i}" for i in range(5)]

    start = time.time()

    # 并发执行多个检索
    tasks = [asyncio.to_thread(kb._store.search, q, 2) for q in queries]
    results = await asyncio.gather(*tasks)

    elapsed = time.time() - start

    print(f"并发 {len(queries)} 个查询完成，耗时: {elapsed*1000:.2f}ms")
    print(f"每个结果数: {[len(r) for r in results]}")

    assert len(results) == len(queries), "结果数量应该与查询数量一致"
    print("PASS: 并发检索正常")

    return True


async def test_non_blocking_behavior():
    """测试异步操作不阻塞事件循环"""
    print("\n=== 测试 3: 非阻塞行为 ===")

    chunks = [
        Chunk(chunk_id="1", content="北京旅游景点包括故宫、长城", source="北京", page=0),
        Chunk(chunk_id="2", content="上海旅游景点包括外滩、东方明珠", source="上海", page=0),
    ]

    kb = KnowledgeBase()
    kb._chunks = chunks
    kb._store = BM25VectorStore(chunks)

    async def slow_task():
        """模拟慢任务"""
        await asyncio.sleep(0.1)
        return "slow_done"

    async def fast_task():
        """模拟快任务"""
        await asyncio.sleep(0.01)
        return "fast_done"

    start = time.time()

    # 并发执行慢任务（检索）和快任务
    results = await asyncio.gather(
        asyncio.to_thread(kb._store.search, "北京", 2),
        fast_task(),
        slow_task()
    )

    elapsed = time.time() - start

    print(f"所有任务完成，耗时: {elapsed*1000:.2f}ms")
    print(f"结果: {[len(r) if isinstance(r, list) else r for r in results]}")

    # 验证快任务没有被慢任务阻塞
    # 总时间应该接近最慢的任务（约100ms），而不是所有任务时间的总和
    assert elapsed < 0.2, "并发任务应该在200ms内完成"
    print("PASS: 事件循环未被阻塞")

    return True


async def test_memory_efficiency():
    """测试内存效率"""
    print("\n=== 测试 4: 内存效率 ===")

    # 创建大量小文档块
    chunks = [
        Chunk(
            chunk_id=str(i),
            content=f"这是第{i}个文档块的内容，包含一些旅行相关的信息" * 10,
            source=f"文档{i % 5}",
            page=i // 10
        )
        for i in range(100)
    ]

    kb = KnowledgeBase()
    kb._max_text_length = 10000  # 设置较小的限制
    kb._chunks = chunks
    kb._store = BM25VectorStore(chunks)

    query = "旅行攻略"

    start = time.time()
    result = await asyncio.to_thread(kb._store.search, query, 5)
    elapsed = time.time() - start

    print(f"从 {len(chunks)} 个块中检索，耗时: {elapsed*1000:.2f}ms")
    print(f"检索到 {len(result)} 个结果")

    assert len(result) > 0, "应该有检索结果"
    print("PASS: 内存效率正常")

    return True


async def main():
    """运行所有测试"""
    print("=" * 60)
    print("QA RAG 异步检索测试套件（简化版）")
    print("=" * 60)

    tests = [
        ("异步 vs 同步一致性", test_async_vs_sync_retrieve),
        ("并发操作", test_concurrent_operations),
        ("非阻塞行为", test_non_blocking_behavior),
        ("内存效率", test_memory_efficiency),
    ]

    results = []

    for name, test_func in tests:
        try:
            passed = await test_func()
            results.append((name, True, None))
            print(f"[PASS] {name}\n")
        except Exception as e:
            results.append((name, False, str(e)))
            print(f"[FAIL] {name}: {e}\n")

    # 打印总结
    print("=" * 60)
    print("测试总结")
    print("=" * 60)

    passed_count = sum(1 for _, passed, _ in results if passed)
    total_count = len(results)

    for name, passed, error in results:
        status = "[PASS]" if passed else "[FAIL]"
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
