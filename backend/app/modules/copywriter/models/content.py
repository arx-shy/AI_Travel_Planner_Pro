"""
Copywriter Content Model
"""

from sqlalchemy import Column, Integer, String, Text, ForeignKey, JSON
from app.core.db.base import BaseModel


class Content(BaseModel):
    __tablename__ = "copywriter_contents"

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    content_type = Column(String(50), default="copywriting", nullable=False)
    platform = Column(String(50), nullable=True)
    output_content = Column(Text, nullable=False)
    input_data = Column(JSON, nullable=True)
    rating = Column(Integer, nullable=True)
