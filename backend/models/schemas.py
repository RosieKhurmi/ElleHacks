from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

class Location(BaseModel):
    """Location coordinates"""
    lat: float = Field(..., description="Latitude")
    lng: float = Field(..., description="Longitude")

class SearchRequest(BaseModel):
    """Request model for business search"""
    query: str = Field(..., description="Search query (e.g., 'coffee shop')")
    location: Location = Field(..., description="User's location")

class PlaceGeometry(BaseModel):
    """Place geometry information"""
    location: Location

class PlaceInfo(BaseModel):
    """Basic place information"""
    place_id: str
    name: str
    formatted_address: Optional[str] = None
    vicinity: Optional[str] = None
    geometry: PlaceGeometry
    rating: Optional[float] = None
    user_ratings_total: Optional[int] = None
    types: Optional[List[str]] = None
    opening_hours: Optional[Dict[str, Any]] = None

class SearchResponse(BaseModel):
    """Response model for business search"""
    success: bool
    places: List[Dict[str, Any]]
    total: int

class PlaceDetailsResponse(BaseModel):
    """Response model for place details"""
    result: Optional[Dict[str, Any]] = None
    status: str

class ErrorResponse(BaseModel):
    """Error response model"""
    error: str
    details: Optional[str] = None

class HealthResponse(BaseModel):
    """Health check response"""
    status: str
    message: str
    google_maps_api_configured: bool
    gemini_api_configured: bool
