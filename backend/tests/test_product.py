import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_product_crud(client: AsyncClient):
    # --- CREATE PRODUCT ---
    product_data = {
        "name": "Test Shirt",
        "price": 19.99,
        "description": "A test shirt",
        "lifetime_guarantee": True,
        "variants": [{"color": "Red", "size": "M", "in_stock": True}],
        "images": [{"color": "Red", "image_url": "http://example.com/shirt.png"}]
    }
    response = await client.post("/api/v1/product/", json=product_data)
    assert response.status_code == 201
    product = response.json()
    product_id = product["id"]

    # --- GET PRODUCT ---
    response = await client.get(f"/api/v1/product/{product_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test Shirt"
    assert len(data["variants"]) == 1
    assert len(data["images"]) == 1

    # --- UPDATE PRODUCT ---
    update_data = {"name": "Updated Shirt", "price": 24.99, "description": "Updated", "lifetime_guarantee": False}
    response = await client.put(f"/api/v1/product/{product_id}", json=update_data)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Updated Shirt"

    # --- DELETE PRODUCT ---
    response = await client.delete(f"/api/v1/product/{product_id}")
    assert response.status_code == 200
    assert response.json()["message"] == "Product deleted"