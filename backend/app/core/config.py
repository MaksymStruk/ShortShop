"""Application configuration settings.

This module contains all configuration settings for the Task Manager application,
including database URLs, Celery settings, and environment-specific configurations.
"""

import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings
from app.log.custom_logger import custom_logger as logger

load_dotenv()


class Settings(BaseSettings):
    """Application settings configuration.

    Uses Pydantic BaseSettings for environment variable management.
    All settings can be overridden via environment variables.
    """
    PROJECT_NAME: str = "ShortShop API"
    DESCRIPTION: str = "API for e-commerce"
    VERSION: str = "0.0.1"
    DEBUG: bool = True

    DATABASE_URL: str = os.getenv("DATABASE_URL")
    REDIS_URL: str = os.getenv("REDIS_URL")

    BASE_DIR: str = os.path.dirname(os.path.abspath(__file__))

    class Config:
        """Pydantic configuration for settings."""
        env_file = ".env"

# Global settings instance
try:
    settings = Settings()
    logger.info(f"[Config] Loaded settings for {settings.PROJECT_NAME} v{settings.VERSION}")
except Exception as exc:
    logger.critical(f"[Config] Error loading settings: {exc}")
    raise
