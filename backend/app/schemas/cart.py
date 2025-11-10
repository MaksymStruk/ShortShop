"""Pydantic schemas for cart data validation and serialization.
"""

from typing import List
from pydantic import BaseModel, Field


# ---------- Cart Schemas ----------

class CartCreate(BaseModel):
    session_id: str = Field(..., min_length=1, max_length=128)


class CartResponse(BaseModel):
    id: int
    session_id: str
    items: List["CartItemResponse"] = []
    
    class Config:
        from_attributes = True


# ---------- Cart Item Schemas ----------

class CartItemCreate(BaseModel):
    variant_id: int = Field(..., gt=0)
    quantity: int = Field(..., gt=0)


class CartItemUpdate(BaseModel):
    quantity: int = Field(..., gt=0)


class CartItemResponse(BaseModel):
    id: int
    variant_id: int
    quantity: int
    
    class Config:
        from_attributes = True


# Update forward references
CartResponse.model_rebuild()
