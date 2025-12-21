"""
QA Chat Schemas

Pydantic models for QA chat requests/responses.
"""

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class ChatCreate(BaseModel):
    title: Optional[str] = Field(default="新对话", max_length=200)


class ChatResponse(BaseModel):
    id: int
    title: str
    created_at: datetime


class MessageCreate(BaseModel):
    content: str = Field(..., min_length=1)
    session_id: Optional[int] = None


class MessageResponse(BaseModel):
    id: int
    role: str
    content: str
    created_at: datetime
