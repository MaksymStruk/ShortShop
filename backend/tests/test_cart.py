import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_cart_crud(client: AsyncClient):
    # --- CREATE CART ---
    cart_data = {"session_id": "test-session-123"}
    response = await client.post("/api/v1/cart/", json=cart_data)
    assert response.status_code == 201
    cart = response.json()
    session_id = cart["session_id"]
    assert cart["items"] == []

    # --- GET CART ---
    response = await client.get(f"/api/v1/cart/{session_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["session_id"] == session_id
    assert data["items"] == []

    # --- ADD ITEM ---
    product_data = {
        "name": "Test Shirt",
        "price": 19.99,
        "description": "A test shirt",
        "lifetime_guarantee": True,
        "variants": [{"color": "Red", "size": "M", "in_stock": True}],
        "images": [{"color": "Red", "image_url": "http://example.com/shirt.png"}]
    }
    product_resp = await client.post("/api/v1/product/", json=product_data)
    product_resp.raise_for_status()
    variant_id = product_resp.json()["variants"][0]["id"]

    cart_item_data = {"variant_id": variant_id, "quantity": 2}
    response = await client.post(f"/api/v1/cart/{session_id}/items", json=cart_item_data)
    assert response.status_code == 201
    item = response.json()
    item_id = item["id"]
    assert item["quantity"] == 2
    assert item["variant_id"] == variant_id

    # --- UPDATE ITEM ---
    update_data = {"quantity": 5}
    response = await client.put(f"/api/v1/cart/{session_id}/items/{item_id}", json=update_data)
    assert response.status_code == 200
    data = response.json()
    assert data["quantity"] == 5

    # --- DELETE ITEM ---
    response = await client.delete(f"/api/v1/cart/{session_id}/items/{item_id}")
    assert response.status_code == 200
    assert response.json()["message"] == "Cart item deleted"

    # --- CLEAR CART ---
    response = await client.delete(f"/api/v1/cart/{session_id}")
    assert response.status_code == 200
