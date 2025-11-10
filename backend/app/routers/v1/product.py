"""Product API endpoints for CRUD operations.

Provides REST API endpoints for product management,
including variants, recommendations, and full async support.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db_session
from app.schemas.product import (
    ProductCreate,
    ProductUpdate,
    ProductResponse,
    ProductVariantCreate,
    ProductVariantResponse,
    ProductImageCreate,
    ProductRecommendationResponse,
)
from app.services.product_service import ProductService

router = APIRouter(
    prefix="/product",
    tags=["Product"]
)


def get_product_service(db: AsyncSession = Depends(get_db_session)):
    """Dependency to get ProductService instance."""
    return ProductService(db)


# ---------------------- PRODUCT ROUTES ----------------------

@router.get("/", response_model=List[ProductResponse])
async def get_products(service: ProductService = Depends(get_product_service), skip: int = 0, limit: int = 100):
    """Get all products with pagination."""
    return await service.get_all(skip, limit)


@router.get("/{product_id}", response_model=ProductResponse)
async def get_product(product_id: int, service: ProductService = Depends(get_product_service)):
    """Get a single product by ID."""
    return await service.get_by_id(product_id)


@router.post("/", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
async def create_product(product_in: ProductCreate, service: ProductService = Depends(get_product_service)):
    """Create a new product with variants and images."""
    return await service.create(product_in)


@router.put("/{product_id}", response_model=ProductResponse)
async def update_product(product_id: int, product_in: ProductUpdate, service: ProductService = Depends(get_product_service)):
    """Update product details."""
    return await service.update(product_id, product_in)


@router.delete("/{product_id}")
async def delete_product(product_id: int, service: ProductService = Depends(get_product_service)):
    """Delete a product."""
    return await service.delete(product_id)


# ---------------------- IMAGE ROUTES ----------------------

@router.post("/{product_id}/images", status_code=status.HTTP_201_CREATED)
async def add_images(product_id: int, images_in: List[ProductImageCreate], service: ProductService = Depends(get_product_service)):
    """Add one or more images to an existing product."""
    return await service.add_images(product_id, images_in)


@router.delete("/{product_id}/images/{image_id}")
async def delete_image(product_id: int, image_id: int, service: ProductService = Depends(get_product_service)):
    """Delete a specific image from a product."""
    return await service.delete_image(product_id, image_id)


# ---------------------- VARIANT ROUTES ----------------------

@router.post("/{product_id}/variants", response_model=ProductVariantResponse)
async def add_variant(product_id: int, variant_in: ProductVariantCreate, service: ProductService = Depends(get_product_service)):
    """Add a variant to a product."""
    return await service.add_variant(product_id, variant_in)


@router.put("/variant/{variant_id}", response_model=ProductVariantResponse)
async def update_variant(variant_id: int, variant_in: ProductVariantCreate, service: ProductService = Depends(get_product_service)):
    """Update a specific product variant."""
    return await service.update_variant(variant_id, variant_in)


@router.delete("/variant/{variant_id}")
async def delete_variant(variant_id: int, service: ProductService = Depends(get_product_service)):
    """Delete a specific product variant."""
    return await service.delete_variant(variant_id)


# ---------------------- RECOMMENDATIONS ----------------------

@router.post("/{product_id}/recommendations/{rec_id}")
async def add_recommendation(product_id: int, rec_id: int, service: ProductService = Depends(get_product_service)):
    """Add a recommended product."""
    return await service.add_recommendation(product_id, rec_id)


@router.get("/{product_id}/recommendations", response_model=List[ProductRecommendationResponse])
async def get_recommendations(product_id: int, service: ProductService = Depends(get_product_service)):
    """Get product recommendations."""
    return await service.get_recommendations(product_id)


@router.delete("/recommendations/{rec_id}")
async def delete_recommendation(rec_id: int, service: ProductService = Depends(get_product_service)):
    """Delete a product recommendation."""
    return await service.delete_recommendation(rec_id)
