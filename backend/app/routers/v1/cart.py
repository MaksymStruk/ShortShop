"""Cart API endpoints for CRUD operations.

Provides REST API endpoints for cart management,
including cart creation, item management, and cart operations.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db_session
from app.schemas.cart import (
    CartCreate,
    CartResponse,
    CartItemCreate,
    CartItemUpdate,
    CartItemResponse,
)
from app.services.cart_service import CartService

router = APIRouter(
    prefix="/cart",
    tags=["Cart"]
)


def get_cart_service(db: AsyncSession = Depends(get_db_session)):
    """Dependency to get CartService instance."""
    return CartService(db)


# ---------------------- CART ROUTES ----------------------

@router.post("/", response_model=CartResponse, status_code=status.HTTP_201_CREATED)
async def create_cart(
    cart_create: CartCreate,
    service: CartService = Depends(get_cart_service)
):
    """Create a new cart with session_id."""
    return await service.create_cart(cart_create.session_id)


@router.get("/{session_id}", response_model=CartResponse)
async def get_cart(
    session_id: str,
    service: CartService = Depends(get_cart_service)
):
    """Get cart by session_id with all items."""
    return await service.get_cart(session_id)


@router.delete("/{session_id}")
async def clear_cart(
    session_id: str,
    service: CartService = Depends(get_cart_service)
):
    """Clear all items from cart."""
    return await service.clear_cart(session_id)


# ---------------------- CART ITEM ROUTES ----------------------

@router.post(
    "/{session_id}/items",
    response_model=CartItemResponse,
    status_code=status.HTTP_201_CREATED
)
async def add_item(
    session_id: str,
    item_create: CartItemCreate,
    service: CartService = Depends(get_cart_service)
):
    """Add item to cart."""
    return await service.add_item(session_id, item_create)


@router.put("/{session_id}/items/{item_id}", response_model=CartItemResponse)
async def update_item(
    session_id: str,
    item_id: int,
    item_update: CartItemUpdate,
    service: CartService = Depends(get_cart_service)
):
    return await service.update_item(session_id, item_id, item_update)


@router.delete("/{session_id}/items/{item_id}")
async def delete_item(
    session_id: str,
    item_id: int,
    service: CartService = Depends(get_cart_service)
):
    return await service.delete_item(session_id, item_id)
