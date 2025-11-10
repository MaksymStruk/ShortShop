# tests/test_server_routes.py
import pytest
from httpx import AsyncClient
from app.main import app

@pytest.mark.asyncio
async def test_root_endpoint():
    """Перевіряє, що сервер повертає коректний корінь /"""
    async with AsyncClient(app=app, base_url="http://testserver") as client:
        response = await client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "status" in data
        assert data["status"] == "OK"
        assert "message" in data
        assert "version" in data

@pytest.mark.asyncio
async def test_health_endpoint():
    """Перевіряє ендпоінт /health"""
    async with AsyncClient(app=app, base_url="http://testserver") as client:
        response = await client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "API is running normally" in data["message"]
        assert "timestamp" in data
