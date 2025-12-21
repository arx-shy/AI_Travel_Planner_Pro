"""
Message Model
"""

from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.core.db.base import BaseModel


class Message(BaseModel):
    __tablename__ = "qa_messages"

    conversation_id = Column(Integer, ForeignKey("qa_conversations.id"), nullable=False, index=True)
    role = Column(String(20), nullable=False)
    content = Column(Text, nullable=False)
    message_type = Column(String(20), default="text", nullable=False)
    metadata_json = Column("metadata", Text, nullable=True)

    conversation = relationship("Conversation", back_populates="messages")
