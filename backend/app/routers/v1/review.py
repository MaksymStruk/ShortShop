"""Product API endpoints for CRUD operations.

Provides REST API endpoints for product management,
including variants, recommendations, and full async support.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db_session
from app.schemas.review import (
    ReviewCreate,
    # ReviewRead
)
from app.services.review_service import ReviewService

router = APIRouter(
    prefix="/review",
    tags=["Review"]
)


def get_product_review_service(db: AsyncSession = Depends(get_db_session)):
    """Dependency to get ProductReviewService instance."""
    return ReviewService(db)


# ---------------------- PRODUCT ROUTES ----------------------

@router.get("/", response_model=List[ReviewCreate])
async def get_reviews(service: ReviewService = Depends(get_product_review_service), skip: int = 0, limit: int = 100):
    """Get all reviws with pagination."""
    return await service.get_all(skip, limit)


# @router.get("/{product_id}", response_model=ProductResponse)
# async def get_product(product_id: int, service: ProductService = Depends(get_product_service)):
#     """Get a single product by ID."""
#     return await service.get_by_id(product_id)


@router.post("/", response_model=ReviewCreate, status_code=status.HTTP_201_CREATED)
async def create_product(review_in: ReviewCreate, service: ReviewService = Depends(get_product_review_service)):
    """Create a new product with variants and images."""
    return await service.create(review_in)


# @router.put("/{product_id}", response_model=ProductResponse)
# async def update_product(product_id: int, product_in: ProductUpdate, service: ProductService = Depends(get_product_service)):
#     """Update product details."""
#     return await service.update(product_id, product_in)


# @router.delete("/{product_id}")
# async def delete_product(product_id: int, service: ProductService = Depends(get_product_service)):
#     """Delete a product."""
#     return await service.delete(product_id)