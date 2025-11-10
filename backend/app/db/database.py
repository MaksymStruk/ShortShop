"""Database configuration and session management.

This module provides async database engines and session management for both
FastAPI and Celery workers, with proper cleanup and isolation.
"""

from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, AsyncEngine
from sqlalchemy.orm import sessionmaker, declarative_base

from app.core.config import settings
from app.log.custom_logger import custom_logger as logger

# === Base class for SQLAlchemy models ===
Base = declarative_base()

# === Async session for FastAPI ===
async_engine = create_async_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,
)

AsyncSessionLocal = sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

async def get_db_session():
    """Async dependency for FastAPI database sessions.
    
    Yields:
        AsyncSession: Database session for FastAPI endpoints
    """
    async with AsyncSessionLocal() as db:
        try:
            yield db
        finally:
            pass