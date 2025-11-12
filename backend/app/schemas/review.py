"""Pydantic schemas for product data validation and serialization.
"""

from typing import List, Optional
from pydantic import BaseModel, Field
from app.models.product import SizeEnum

class ReviewCreate(BaseModel):
    product_id: int
    title: str = Field(..., min_length=10, max_length=120)
    description: str = Field(..., min_length=20, max_length=300)
    author_name: str = Field()
    score: int = Field(..., ge=1, le=5)