"""Cart service layer for business logic.

Provides async CRUD operations for cart management,
including cart creation, item management, and cart operations.
"""

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from fastapi import HTTPException, status

from app.models.product import Cart, CartItem, ProductVariant
from app.schemas.cart import CartCreate, CartItemCreate, CartItemUpdate


class CartService:
    """Service class for cart operations."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_cart(self, session_id: str):
        """Get cart by session_id with items loaded."""
        result = await self.db.execute(
            select(Cart)
            .options(selectinload(Cart.items))
            .filter(Cart.session_id == session_id)
        )
        cart = result.scalar_one_or_none()
        if not cart:
            raise HTTPException(status_code=404, detail="Cart not found")
        return cart

    async def create_cart(self, session_id: str):
        """Create a new cart with session_id or return existing one."""
        # Check if cart already exists
        result = await self.db.execute(
            select(Cart)
            .options(selectinload(Cart.items))
            .filter(Cart.session_id == session_id)
        )
        existing_cart = result.scalar_one_or_none()
        if existing_cart:
            return existing_cart
        
        cart = Cart(session_id=session_id)
        self.db.add(cart)
        await self.db.commit()
        await self.db.refresh(cart)
        
        # Reload with items
        result = await self.db.execute(
            select(Cart)
            .options(selectinload(Cart.items))
            .filter(Cart.id == cart.id)
        )
        return result.scalar_one()

    async def add_item(self, session_id: str, item_create: CartItemCreate):
        """Add item to cart or update quantity if item already exists."""
        # Get or create cart
        result = await self.db.execute(
            select(Cart)
            .options(selectinload(Cart.items))
            .filter(Cart.session_id == session_id)
        )
        cart = result.scalar_one_or_none()
        if not cart:
            # Cart doesn't exist, create it
            cart = await self.create_cart(session_id)
        
        # Check if variant exists
        variant_result = await self.db.execute(
            select(ProductVariant).filter(ProductVariant.id == item_create.variant_id)
        )
        variant = variant_result.scalar_one_or_none()
        if not variant:
            raise HTTPException(status_code=404, detail="Variant not found")
        
        # Check if item already exists in cart
        item_result = await self.db.execute(
            select(CartItem).filter(
                CartItem.cart_id == cart.id,
                CartItem.variant_id == item_create.variant_id
            )
        )
        existing_item = item_result.scalar_one_or_none()
        
        if existing_item:
            # Update quantity
            existing_item.quantity += item_create.quantity
            await self.db.commit()
            await self.db.refresh(existing_item)
            return existing_item
        else:
            # Create new item
            item = CartItem(
                cart_id=cart.id,
                variant_id=item_create.variant_id,
                quantity=item_create.quantity
            )
            self.db.add(item)
            await self.db.commit()
            await self.db.refresh(item)
            return item

    async def update_item(self, session_id: str, item_id: int, item_update: CartItemUpdate):
        """Update item quantity, verifying cart ownership."""
        cart = await self.get_cart(session_id)
        result = await self.db.execute(
            select(CartItem).filter(CartItem.id == item_id, CartItem.cart_id == cart.id)
        )
        item = result.scalar_one_or_none()
        if not item:
            raise HTTPException(status_code=403, detail="Item not found in this cart")

        item.quantity = item_update.quantity
        await self.db.commit()
        await self.db.refresh(item)
        return item

    async def delete_item(self, session_id: str, item_id: int):
        """Delete item from cart safely (ownership checked)."""
        cart = await self.get_cart(session_id)
        result = await self.db.execute(
            select(CartItem).filter(CartItem.id == item_id, CartItem.cart_id == cart.id)
        )
        item = result.scalar_one_or_none()
        if not item:
            raise HTTPException(status_code=403, detail="Item not found in this cart")

        await self.db.delete(item)
        await self.db.commit()
        return {"message": "Cart item deleted"}

    async def clear_cart(self, session_id: str):
        """Clear all items from cart."""
        cart = await self.get_cart(session_id)
        
        # Delete all items in one query
        from sqlalchemy import delete
        await self.db.execute(
            delete(CartItem).where(CartItem.cart_id == cart.id)
        )
        await self.db.commit()
        return {"message": "Cart cleared"}
