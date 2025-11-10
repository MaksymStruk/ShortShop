"""Pydantic schemas for product data validation and serialization.
"""

from typing import List, Optional
from pydantic import BaseModel, Field
from app.models.product import SizeEnum


# ---------- Product Image Schemas ----------

class ProductImageCreate(BaseModel):
    color: Optional[str] = None
    image_url: str = Field(..., min_length=1, max_length=255)


class ProductImageResponse(BaseModel):
    id: int
    color: Optional[str] = None
    image_url: str
    
    class Config:
        from_attributes = True


# ---------- Product Variant Schemas ----------

class ProductVariantCreate(BaseModel):
    color: str = Field(..., min_length=1, max_length=50)
    size: SizeEnum
    in_stock: bool = False


class ProductVariantResponse(BaseModel):
    id: int
    color: str
    size: SizeEnum
    in_stock: bool
    
    class Config:
        from_attributes = True


# ---------- Product Schemas ----------

class ProductCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=120)
    price: float = Field(..., gt=0)
    description: str = Field(..., min_length=1)
    lifetime_guarantee: bool = True
    variants: List[ProductVariantCreate] = []
    images: List[ProductImageCreate] = []


class ProductUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=120)
    price: Optional[float] = Field(None, gt=0)
    description: Optional[str] = Field(None, min_length=1)
    lifetime_guarantee: Optional[bool] = None


class ProductResponse(BaseModel):
    id: int
    name: str
    price: float
    description: str
    lifetime_guarantee: bool
    variants: List[ProductVariantResponse] = []
    images: List[ProductImageResponse] = []
    
    class Config:
        from_attributes = True


# ---------- Product Recommendation Schemas ----------

class ProductRecommendationResponse(BaseModel):
    id: int
    base_product_id: int
    recommended_product_id: int
    
    class Config:
        from_attributes = True