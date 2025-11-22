from fastapi import APIRouter, HTTPException
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from models.schemas import SearchRequest, SearchResponse, ErrorResponse
from services.google_maps_service import GoogleMapsService
from services.gemini_service import GeminiService

router = APIRouter()

# Initialize services
google_maps_service = GoogleMapsService()
gemini_service = GeminiService()

@router.post("/search", response_model=SearchResponse)
async def search_businesses(request: SearchRequest):
    """
    Search for small businesses near a location
    
    Args:
        request: SearchRequest containing query and location
        
    Returns:
        SearchResponse with filtered small businesses
    """
    try:
        print(f"Search request: {request.query} at ({request.location.lat}, {request.location.lng})")
        
        # Validate input
        if not request.query or not request.query.strip():
            raise HTTPException(status_code=400, detail="Query cannot be empty")
        
        # Search places using Google Maps
        print("Calling Google Maps API...")
        places = await google_maps_service.search_places(
            query=request.query,
            lat=request.location.lat,
            lng=request.location.lng
        )
        print(f"Google Maps returned {len(places)} places")
        
        if not places:
            return SearchResponse(
                success=True,
                places=[],
                total=0
            )
        
        # Filter for small businesses using Gemini AI
        filtered_places = await gemini_service.filter_small_businesses(
            places=places,
            search_query=request.query
        )
        
        return SearchResponse(
            success=True,
            places=filtered_places,
            total=len(filtered_places)
        )
        
    except HTTPException:
        raise
    except Exception as e:
        import traceback
        print(f"Search error: {str(e)}")
        print(traceback.format_exc())
        raise HTTPException(
            status_code=500,
            detail=f"Failed to search for places: {str(e)}"
        )

@router.get("/place/{place_id}")
async def get_place_details(place_id: str):
    """
    Get detailed information about a specific place
    
    Args:
        place_id: Google Place ID
        
    Returns:
        Place details from Google Maps API
    """
    try:
        details = await google_maps_service.get_place_details(place_id)
        return details
        
    except Exception as e:
        print(f"Place details error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get place details: {str(e)}"
        )
