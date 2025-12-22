"""
Copywriter Content Schemas

Pydantic models for content generation.
"""

from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional, Dict, Any
from datetime import datetime


class ContentCreate(BaseModel):
    platform: Optional[str] = Field(default="xiaohongshu")
    keywords: List[str] = []
    emotion_level: Optional[int] = Field(default=50, ge=0, le=100)
    images: List[str] = []


class ContentResponse(BaseModel):
    id: int
    content_type: str
    platform: Optional[str] = None
    output_content: str
    input_data: Optional[Dict[str, Any]] = None
    rating: Optional[int] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ContentRating(BaseModel):
    rating: int = Field(..., ge=1, le=5)
