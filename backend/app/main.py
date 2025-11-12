"""FastAPI application main module.

This module creates and configures the FastAPI application with
async database initialization, middleware setup, and route registration.
"""

from datetime import datetime
from contextlib import asynccontextmanager
import asyncio
import asyncpg

from fastapi import FastAPI

from app.log.custom_logger import logger_test, custom_logger as logger
from app.db.database import Base, async_engine
from app.models import product
from app.routers.v1 import server, product, cart, review
from app.core.config import settings
from app.core.ascii_art import ASCII_ART
from app.core.middleware import setup_middlewares

async def wait_for_db():
    """Wait until the PostgreSQL database is ready to accept connections."""
    retries = 10
    while retries > 0:
        try:
            conn = await asyncpg.connect(
                user="postgres",
                password="password",
                database="shortshop_db",
                host="db",
            )
            await conn.close()
            return
        except Exception:
            retries -= 1
            await asyncio.sleep(2)
    raise Exception("Database not ready after multiple retries")

# --- Async database initialization ---
async def init_db():
    """Initialize database tables asynchronously."""
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    logger.info("[Startup] Database tables created")

# --- FastAPI lifespan management ---
@asynccontextmanager
async def lifespan(application: FastAPI):
    """Manage application startup and shutdown lifecycle.

    Args:
        application: FastAPI application instance

    Yields:
        None: Control back to FastAPI during runtime
    """
    # --- startup ---
    if settings.DEBUG:
        logger_test()
    logger.info(f"[Startup] {settings.PROJECT_NAME} {settings.VERSION} starting...")

    # Wait until database is ready
    await wait_for_db()

    # Initialize database tables
    await init_db()

    logger.success(f"[Startup] Server started at {datetime.now()}\n{ASCII_ART}")

    yield  # FastAPI handles requests here

    # --- shutdown ---
    logger.info("[Shutdown] FastAPI server is stopping...")

# --- FastAPI application initialization ---
app = FastAPI(
    title=settings.PROJECT_NAME,
    description=settings.DESCRIPTION,
    version=settings.VERSION,
    lifespan=lifespan
)

# Enable CORS and other middleware
setup_middlewares(app)

# --- Route registration ---
app.include_router(server.router)
app.include_router(product.router, prefix="/api/v1")
app.include_router(cart.router, prefix="/api/v1")
app.include_router(review.router, prefix="/api/v1")
