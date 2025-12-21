"""
QA Chat Schemas

Pydantic models for QA chat requests/responses.
"""

from pydantic import BaseModel, Field
from typing import Optional, List, Dict
from datetime import datetime


class ChatFeatures(BaseModel):
    knowledge_base: bool = False
    weather: bool = False
    voice: bool = False


class ChatCreate(BaseModel):
    title: Optional[str] = Field(default="新对话", max_length=200)
    features: Optional[ChatFeatures] = None


class ChatResponse(BaseModel):
    id: int
    title: str
    features: Optional[ChatFeatures] = None
    created_at: datetime


class MessageCreate(BaseModel):
    content: str = Field(..., min_length=1)
    session_id: int
    message_type: str = Field(default="text", pattern="^(text|voice)$")


class MessageResponse(BaseModel):
    id: int
    session_id: int
    role: str
    content: str
    message_type: str
    created_at: datetime
