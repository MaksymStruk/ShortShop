# """Product service layer for business logic.

# Provides async CRUD operations for product management,
# including creation, variant management, and recommendations.
# """

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from fastapi import HTTPException, status

from app.models.product import (
    ProductReview
)
from app.schemas.review import (
    ReviewCreate
)


class ReviewService:
    """Service class for product operations."""

    def __init__(self, db: AsyncSession):
        self.db = db

    # ---------------------- PRODUCTS ----------------------

    async def get_all(self, skip: int = 0, limit: int = 100):
        result = await self.db.execute(
            select(ProductReview)
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()

    async def create(self, review_in: ReviewCreate):
        review = ProductReview(
            product_id=review_in.product_id,
            title=review_in.title,
            description=review_in.description,
            author_name=review_in.author_name,
            score=review_in.score
        )
        self.db.add(review)
        
        await self.db.flush()
        await self.db.commit()

        # Reload with relationships
        result = await self.db.execute(
            select(ProductReview).filter(ProductReview.id == review.id)
        )
        return result.scalar_one()