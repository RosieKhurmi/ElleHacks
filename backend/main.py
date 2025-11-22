from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os
import sys
from pathlib import Path

# Add backend directory to Python path
backend_dir = Path(__file__).parent
sys.path.insert(0, str(backend_dir))

from api.routes import search, health

# Load environment variables from backend directory
env_path = backend_dir / '.env'
load_dotenv(dotenv_path=env_path)

# Initialize FastAPI app
app = FastAPI(
    title="Small Business Finder API",
    description="API for finding small businesses using Google Maps and Gemini AI",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React app
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(search.router, prefix="/api", tags=["search"])
app.include_router(health.router, prefix="/api", tags=["health"])

# Root endpoint
@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "Small Business Finder API",
        "version": "1.0.0",
        "endpoints": {
            "health": "/api/health",
            "search": "/api/search",
            "place_details": "/api/place/{place_id}",
            "docs": "/docs",
            "redoc": "/redoc"
        }
    }

if __name__ == "__main__":
    import uvicorn
    print(f"Starting server on http://localhost:8000")
    print(f"API Documentation available at http://localhost:8000/docs")
    uvicorn.run("main:app", host="0.0.0.0", reload=True)
