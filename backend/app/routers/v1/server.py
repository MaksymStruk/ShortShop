from fastapi import APIRouter
from datetime import datetime
from app.core.config import settings

router = APIRouter(
    tags=['Server']
)

@router.get("/")
async def root():
    """API root endpoint.

    Returns basic information about the Task Manager API.
    """
    return {
        "status": "OK",
        "message": f"{settings.PROJECT_NAME} is running (˶ᵔ ᵕ ᵔ˶)",
        "version": settings.VERSION
    }


@router.get("/health")
async def health_check():
    """Health check endpoint.

    Check if the API server is running and healthy. This endpoint is typically
    used by monitoring systems and load balancers.
    """
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "message": "API is running normally (˶ˆᗜˆ˵)"
    }
