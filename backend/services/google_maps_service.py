import httpx
from typing import List, Dict, Any, Optional
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from config.settings import settings

class GoogleMapsService:
    """Service for interacting with Google Maps API"""
    
    def __init__(self):
        self.api_key = settings.GOOGLE_MAPS_API_KEY
        self.search_radius = settings.SEARCH_RADIUS
    
    async def search_places(self, query: str, lat: float, lng: float) -> List[Dict[str, Any]]:
        """
        Search for places using Google Maps Places API Text Search
        
        Args:
            query: Search query
            lat: Latitude
            lng: Longitude
            
        Returns:
            List of places
        """
        url = settings.GOOGLE_PLACES_TEXT_SEARCH
        
        params = {
            "query": f"{query} near {lat},{lng}",
            "radius": self.search_radius,
            "key": self.api_key
        }
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(url, params=params, timeout=30.0)
                response.raise_for_status()
                data = response.json()
                
                if data.get("status") not in ["OK", "ZERO_RESULTS"]:
                    raise Exception(f"Google Maps API error: {data.get('status')}")
                
                return data.get("results", [])
        except Exception as e:
            print(f"Error searching places: {e}")
            raise
    
    async def get_place_details(self, place_id: str) -> Dict[str, Any]:
        """
        Get detailed information about a place
        
        Args:
            place_id: Google Place ID
            
        Returns:
            Place details
        """
        url = settings.GOOGLE_PLACE_DETAILS
        
        params = {
            "place_id": place_id,
            "key": self.api_key
        }
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(url, params=params, timeout=30.0)
                response.raise_for_status()
                return response.json()
        except Exception as e:
            print(f"Error getting place details: {e}")
            raise
