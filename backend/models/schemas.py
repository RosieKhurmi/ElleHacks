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

# Auth schemas
class RegisterRequest(BaseModel):
    """User registration request"""
    username: str = Field(..., min_length=3, max_length=50)
    email: str = Field(..., pattern=r'^[\w\.-]+@[\w\.-]+\.\w+$')
    password: str = Field(..., min_length=6)

class LoginRequest(BaseModel):
    """User login request"""
    username: str
    password: str

class AuthResponse(BaseModel):
    """Authentication response"""
    success: bool
    token: str
    user: Dict[str, Any]

class MessageResponse(BaseModel):
    """Generic message response"""
    success: bool
    message: str

class FavoriteRequest(BaseModel):
    """Add favorite request"""
    place_data: Dict[str, Any]

class FavoriteResponse(BaseModel):
    """Favorites list response"""
    success: bool
    favorites: List[Dict[str, Any]]
