import httpx
import json
from typing import List, Dict, Any
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from config.settings import settings

class GeminiService:
    """Service for interacting with Google Gemini AI API"""
    
    def __init__(self):
        self.api_key = settings.GEMINI_API_KEY
        self.api_url = settings.GEMINI_API_URL
    
    async def filter_small_businesses(
        self, 
        places: List[Dict[str, Any]], 
        search_query: str
    ) -> List[Dict[str, Any]]:
        """
        Use Gemini AI to filter places and return only small businesses
        
        Args:
            places: List of places from Google Maps
            search_query: Original search query
            
        Returns:
            Filtered list of small businesses
        """
        if not places:
            return []
        
        try:
            # Prepare simplified place information for Gemini
            places_info = [
                {
                    "id": idx,
                    "name": place.get("name"),
                    "address": place.get("formatted_address"),
                    "types": place.get("types", []),
                    "rating": place.get("rating"),
                    "user_ratings_total": place.get("user_ratings_total")
                }
                for idx, place in enumerate(places)
            ]
            
            # Create prompt for Gemini
            prompt = self._create_filter_prompt(places_info, search_query)
            
            # Call Gemini API
            payload = {
                "contents": [{
                    "parts": [{
                        "text": prompt
                    }]
                }]
            }
            
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.api_url}?key={self.api_key}",
                    json=payload,
                    timeout=30.0
                )
                response.raise_for_status()
                data = response.json()
            
            # Parse Gemini response
            gemini_text = data.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "[]")
            
            # Extract the array of IDs
            small_business_ids = self._parse_gemini_response(gemini_text)
            
            # Filter original places based on Gemini's selection
            filtered_places = [
                places[idx] 
                for idx in small_business_ids 
                if idx < len(places)
            ]
            
            # Return filtered places or fallback to first 5
            return filtered_places if filtered_places else places[:5]
            
        except Exception as e:
            print(f"Gemini filtering error: {e}")
            # If filtering fails, return all places as fallback
            return places
    
    def _create_filter_prompt(self, places_info: List[Dict], search_query: str) -> str:
        """Create the prompt for Gemini AI"""
        return f"""You are an expert at identifying small businesses vs chains/franchises.

Given this list of places for the search "{search_query}", identify which ones are likely SMALL, LOCAL, INDEPENDENT businesses (not chains or franchises).

Places:
{json.dumps(places_info, indent=2)}

Return ONLY a JSON array of the IDs (just the numbers) of places that are small businesses. Consider:
- Local, independent establishments are small businesses
- Chain restaurants, franchises, big box stores are NOT small businesses
- Family-owned shops, local cafes, independent stores ARE small businesses
- Well-known national/international brands are NOT small businesses

Return format: [0, 2, 5] (just the array of ID numbers that are small businesses)
Return ONLY the array, no other text."""
    
    def _parse_gemini_response(self, response_text: str) -> List[int]:
        """Parse Gemini's response to extract business IDs"""
        import re
        
        try:
            # Try to find array pattern in response
            match = re.search(r'\[[\d,\s]*\]', response_text)
            if match:
                return json.loads(match.group(0))
            return []
        except Exception as e:
            print(f"Error parsing Gemini response: {e}")
            return []
