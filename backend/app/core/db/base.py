"""
Database Base Model

This module defines the base SQLAlchemy model class with common fields
and functionality used across all database models.
"""

from sqlalchemy import Column, Integer, DateTime, func
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class BaseModel(Base):
    """
    Abstract base model with common fields.
    All models should inherit from this class.
    """
    __abstract__ = True

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(
        DateTime,
        default=func.now(),
        onupdate=func.now(),
        nullable=False
    )


def import_all_models():
    """
    Import all models to register them with SQLAlchemy Base.
    This should be called during application startup.
    """
    # Import models so SQLAlchemy registers them in Base.metadata
    from app.modules.users.models import User, UserSettings, Subscription  # noqa: F401,E402
    from app.modules.planner.models.itinerary import Itinerary, DayDetail  # noqa: F401,E402
    from app.modules.qa.models import Conversation, Message  # noqa: F401,E402
    from app.modules.copywriter.models import Content  # noqa: F401,E402
