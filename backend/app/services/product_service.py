"""Product service layer for business logic.

Provides async CRUD operations for product management,
including creation, variant management, and recommendations.
"""

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from fastapi import HTTPException, status

from app.models.product import (
    Product,
    ProductVariant,
    ProductImage,
    ProductRecommendation,
)
from app.schemas.product import (
    ProductCreate,
    ProductUpdate,
    ProductVariantCreate,
    ProductImageCreate,
)


class ProductService:
    """Service class for product operations."""

    def __init__(self, db: AsyncSession):
        self.db = db

    # ---------------------- PRODUCTS ----------------------

    async def get_all(self, skip: int = 0, limit: int = 100):
        result = await self.db.execute(
            select(Product)
            .options(
                selectinload(Product.variants),
                selectinload(Product.images)
            )
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()

    async def get_by_id(self, product_id: int):
        result = await self.db.execute(
            select(Product)
            .options(
                selectinload(Product.variants),
                selectinload(Product.images)
            )
            .filter(Product.id == product_id)
        )
        product = result.scalar_one_or_none()
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        return product

    async def create(self, product_in: ProductCreate):
        product = Product(
            name=product_in.name,
            price=product_in.price,
            description=product_in.description,
            lifetime_guarantee=product_in.lifetime_guarantee,
        )
        self.db.add(product)
        await self.db.flush()

        # Images
        for img in product_in.images:
            self.db.add(ProductImage(product_id=product.id, color=img.color, image_url=img.image_url))

        # Variants
        for var in product_in.variants:
            self.db.add(ProductVariant(product_id=product.id, color=var.color, size=var.size, in_stock=var.in_stock))

        await self.db.commit()
        await self.db.refresh(product)
        
        # Reload with relationships
        result = await self.db.execute(
            select(Product)
            .options(
                selectinload(Product.variants),
                selectinload(Product.images)
            )
            .filter(Product.id == product.id)
        )
        return result.scalar_one()

    async def update(self, product_id: int, product_in: ProductUpdate):
        product = await self.get_by_id(product_id)
        update_data = product_in.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(product, field, value)
        await self.db.commit()
        await self.db.refresh(product)
        return product

    async def delete(self, product_id: int):
        product = await self.get_by_id(product_id)
        await self.db.delete(product)
        await self.db.commit()
        return {"message": "Product deleted"}

    # ---------------------- IMAGES ----------------------

    async def add_images(self, product_id: int, images_in: list[ProductImageCreate]):
        """Add one or more images to an existing product."""
        product = await self.get_by_id(product_id)

        if not images_in:
            raise HTTPException(status_code=400, detail="No images provided")

        for img in images_in:
            new_image = ProductImage(
                product_id=product.id,
                color=img.color,
                image_url=img.image_url
            )
            self.db.add(new_image)

        await self.db.commit()
        await self.db.refresh(product)
        return {"message": f"{len(images_in)} image(s) added successfully"}

    async def delete_image(self, product_id: int, image_id: int):
        """Delete a specific image from a specific product."""
        result = await self.db.execute(
            select(ProductImage)
            .filter(ProductImage.id == image_id, ProductImage.product_id == product_id)
        )
        image = result.scalar_one_or_none()
        if not image:
            raise HTTPException(
                status_code=404,
                detail="Image not found for this product"
            )

        await self.db.delete(image)
        await self.db.commit()
        return {"message": "Image deleted"}

    # ---------------------- VARIANTS ----------------------

    async def add_variant(self, product_id: int, variant_in: ProductVariantCreate):
        product = await self.get_by_id(product_id)
        variant = ProductVariant(
            product_id=product.id,
            color=variant_in.color,
            size=variant_in.size,
            in_stock=variant_in.in_stock,
        )
        self.db.add(variant)
        await self.db.commit()
        await self.db.refresh(variant)
        return variant

    async def update_variant(self, variant_id: int, variant_in: ProductVariantCreate):
        result = await self.db.execute(select(ProductVariant).filter(ProductVariant.id == variant_id))
        variant = result.scalar_one_or_none()
        if not variant:
            raise HTTPException(status_code=404, detail="Variant not found")
        variant.color = variant_in.color
        variant.size = variant_in.size
        variant.in_stock = variant_in.in_stock
        await self.db.commit()
        await self.db.refresh(variant)
        return variant

    async def delete_variant(self, variant_id: int):
        result = await self.db.execute(select(ProductVariant).filter(ProductVariant.id == variant_id))
        variant = result.scalar_one_or_none()
        if not variant:
            raise HTTPException(status_code=404, detail="Variant not found")
        await self.db.delete(variant)
        await self.db.commit()
        return {"message": "Variant deleted"}

    # ---------------------- RECOMMENDATIONS ----------------------

    async def add_recommendation(self, base_id: int, rec_id: int):
        if base_id == rec_id:
            raise HTTPException(status_code=400, detail="Cannot recommend the same product")
        
        # Check if both products exist
        base_product = await self.get_by_id(base_id)
        rec_product = await self.get_by_id(rec_id)
        
        # Check if recommendation already exists
        existing = await self.db.execute(
            select(ProductRecommendation).filter(
                ProductRecommendation.base_product_id == base_id,
                ProductRecommendation.recommended_product_id == rec_id
            )
        )
        if existing.scalar_one_or_none():
            raise HTTPException(status_code=400, detail="Recommendation already exists")
        
        rec = ProductRecommendation(base_product_id=base_id, recommended_product_id=rec_id)
        self.db.add(rec)
        await self.db.commit()
        await self.db.refresh(rec)
        return {"message": "Recommendation added"}

    async def get_recommendations(self, base_id: int):
        # Verify product exists
        await self.get_by_id(base_id)
        
        result = await self.db.execute(
            select(ProductRecommendation)
            .filter(ProductRecommendation.base_product_id == base_id)
        )
        return result.scalars().all()

    async def delete_recommendation(self, rec_id: int):
        result = await self.db.execute(select(ProductRecommendation).filter(ProductRecommendation.id == rec_id))
        rec = result.scalar_one_or_none()
        if not rec:
            raise HTTPException(status_code=404, detail="Recommendation not found")
        await self.db.delete(rec)
        await self.db.commit()
        return {"message": "Recommendation deleted"}
