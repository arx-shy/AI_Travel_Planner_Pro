"""
Conversation Model
"""

from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.core.db.base import BaseModel


class Conversation(BaseModel):
    __tablename__ = "qa_conversations"

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    title = Column(String(200), nullable=False)
    features_json = Column("features", Text, nullable=True)

    messages = relationship("Message", back_populates="conversation", cascade="all, delete-orphan")
