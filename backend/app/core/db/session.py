"""
Database Session Management

This module manages database connections and session creation.
It uses SQLAlchemy's async capabilities for high performance.
"""

import os
from pathlib import Path
import logging
import sys

# Load .env file if exists
env_file = Path(__file__).parent.parent.parent / '.env'
if env_file.exists():
    with open(env_file, 'r') as f:
        for line in f:
            if '=' in line and not line.strip().startswith('#'):
                key, value = line.strip().split('=', 1)
                os.environ[key] = value

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.pool import StaticPool
from sqlalchemy.engine import Engine
from app.core.config.settings import settings
from app.core.db.base import Base

logger = logging.getLogger(__name__)

# 创建一个自定义的SQLAlchemy日志处理器，使用UTF-8编码
class UTF8Handler(logging.Handler):
    def emit(self, record):
        try:
            msg = self.format(record)
            if isinstance(msg, str):
                msg = msg.encode('utf-8', errors='replace').decode('utf-8', errors='replace')
            print(msg)
        except Exception:
            pass

# 创建自定义engine来避免SQLAlchemy的echo编码问题
def create_engine_with_utf8_logging(database_url, echo=False):
    """创建支持UTF-8的engine"""
    import sqlalchemy

    engine = create_async_engine(
        database_url,
        echo=echo,
        pool_pre_ping=True,
        pool_recycle=3600,
    )

    # 如果启用了echo，配置SQLAlchemy的logger使用UTF-8处理器
    if echo:
        sa_logger = logging.getLogger('sqlalchemy.engine')
        sa_logger.propagate = False
        handler = UTF8Handler()
        handler.setFormatter(logging.Formatter('%(message)s'))
        sa_logger.addHandler(handler)

    return engine

# Create async engine
engine = create_engine_with_utf8_logging(settings.DATABASE_URL, echo=False)  # 禁用echo避免编码问题

# Create async session factory
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)


async def init_db():
    """
    Initialize database connection and create tables.
    This function should be called on application startup.
    """
    logger.info("Initializing database...")
    async with engine.begin() as conn:
        # Create all tables
        await conn.run_sync(Base.metadata.create_all)
    logger.info("Database initialized successfully")


async def get_db() -> AsyncSession:
    """
    Dependency function to get database session.
    Should be used as FastAPI dependency.
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()


async def close_db():
    """
    Close database connections.
    This function should be called on application shutdown.
    """
    await engine.dispose()
    logger.info("Database connections closed")

