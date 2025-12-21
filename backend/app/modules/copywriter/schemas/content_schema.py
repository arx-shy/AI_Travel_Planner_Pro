"""
Copywriter Content Schemas

Pydantic models for content generation.
"""

from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


class ContentCreate(BaseModel):
    platform: Optional[str] = Field(default="xiaohongshu")
    keywords: List[str] = []
    emotion_level: Optional[int] = Field(default=50, ge=0, le=100)
    images: List[str] = []


class ContentResponse(BaseModel):
    id: int
    content_type: str
    output_content: str
    created_at: datetime
