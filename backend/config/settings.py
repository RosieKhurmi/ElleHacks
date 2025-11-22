import os
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables from backend directory
backend_dir = Path(__file__).parent.parent
env_path = backend_dir / '.env'
load_dotenv(dotenv_path=env_path)

class Settings:
    """Application settings and configuration"""
    
    # API Keys
    GOOGLE_MAPS_API_KEY: str = os.getenv("GOOGLE_MAPS_API_KEY", "")
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    
    # Server Settings
    PORT: int = int(os.getenv("PORT", 5000))
    HOST: str = os.getenv("HOST", "0.0.0.0")
    
    # Google Maps Settings
    SEARCH_RADIUS: int = 5000  # 5km radius
    
    # API Endpoints
    GOOGLE_PLACES_TEXT_SEARCH: str = "https://maps.googleapis.com/maps/api/place/textsearch/json"
    GOOGLE_PLACE_DETAILS: str = "https://maps.googleapis.com/maps/api/place/details/json"
    GEMINI_API_URL: str = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"
    
    def validate(self) -> bool:
        """Validate that required settings are present"""
        if not self.GOOGLE_MAPS_API_KEY:
            print("Warning: GOOGLE_MAPS_API_KEY is not set")
            return False
        if not self.GEMINI_API_KEY:
            print("Warning: GEMINI_API_KEY is not set")
            return False
        return True

settings = Settings()

# Validate settings on import
if not settings.validate():
    print("Warning: Some API keys are not configured. Check your .env file.")
