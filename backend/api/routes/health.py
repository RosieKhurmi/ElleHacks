from fastapi import APIRouter
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from models.schemas import HealthResponse
from config.settings import settings

router = APIRouter()

@router.get("/health", response_model=HealthResponse)
async def health_check():
    """
    Health check endpoint to verify API is running and configured
    
    Returns:
        HealthResponse with status and configuration info
    """
    return HealthResponse(
        status="ok",
        message="Server is running",
        google_maps_api_configured=bool(settings.GOOGLE_MAPS_API_KEY),
        gemini_api_configured=bool(settings.GEMINI_API_KEY)
    )
