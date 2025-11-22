from fastapi import APIRouter, HTTPException, Header
from typing import Optional
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from models.schemas import (
    RegisterRequest, LoginRequest, AuthResponse, 
    FavoriteRequest, FavoriteResponse, MessageResponse
)
from database.db import (
    create_user, verify_user, create_session, verify_session,
    delete_session, add_favorite, remove_favorite, get_favorites, is_favorite
)

router = APIRouter()

@router.post("/register", response_model=AuthResponse)
async def register(request: RegisterRequest):
    """Register a new user"""
    user_id = create_user(request.username, request.email, request.password)
    
    if not user_id:
        raise HTTPException(status_code=400, detail="Username or email already exists")
    
    token = create_session(user_id)
    
    return AuthResponse(
        success=True,
        token=token,
        user={
            "id": user_id,
            "username": request.username,
            "email": request.email
        }
    )

@router.post("/login", response_model=AuthResponse)
async def login(request: LoginRequest):
    """Login user"""
    user = verify_user(request.username, request.password)
    
    if not user:
        raise HTTPException(status_code=401, detail="Invalid username or password")
    
    token = create_session(user['id'])
    
    return AuthResponse(
        success=True,
        token=token,
        user=user
    )

@router.post("/logout", response_model=MessageResponse)
async def logout(authorization: Optional[str] = Header(None)):
    """Logout user"""
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    token = authorization.replace("Bearer ", "")
    delete_session(token)
    
    return MessageResponse(success=True, message="Logged out successfully")

@router.get("/me")
async def get_current_user(authorization: Optional[str] = Header(None)):
    """Get current user info"""
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    token = authorization.replace("Bearer ", "")
    user_id = verify_session(token)
    
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    
    from database.db import get_db_connection
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, username, email FROM users WHERE id = ?", (user_id,))
    user = cursor.fetchone()
    conn.close()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return {"success": True, "user": dict(user)}

@router.post("/favorites", response_model=MessageResponse)
async def add_to_favorites(
    request: FavoriteRequest,
    authorization: Optional[str] = Header(None)
):
    """Add a place to favorites"""
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    token = authorization.replace("Bearer ", "")
    user_id = verify_session(token)
    
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    
    success = add_favorite(user_id, request.place_data)
    
    if not success:
        raise HTTPException(status_code=400, detail="Place already in favorites")
    
    return MessageResponse(success=True, message="Added to favorites")

@router.delete("/favorites/{place_id}", response_model=MessageResponse)
async def remove_from_favorites(
    place_id: str,
    authorization: Optional[str] = Header(None)
):
    """Remove a place from favorites"""
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    token = authorization.replace("Bearer ", "")
    user_id = verify_session(token)
    
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    
    success = remove_favorite(user_id, place_id)
    
    if not success:
        raise HTTPException(status_code=404, detail="Favorite not found")
    
    return MessageResponse(success=True, message="Removed from favorites")

@router.get("/favorites", response_model=FavoriteResponse)
async def get_user_favorites(authorization: Optional[str] = Header(None)):
    """Get all user favorites"""
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    token = authorization.replace("Bearer ", "")
    user_id = verify_session(token)
    
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    
    favorites = get_favorites(user_id)
    
    return FavoriteResponse(success=True, favorites=favorites)

@router.get("/favorites/check/{place_id}")
async def check_favorite(
    place_id: str,
    authorization: Optional[str] = Header(None)
):
    """Check if a place is in favorites"""
    if not authorization or not authorization.startswith("Bearer "):
        return {"is_favorite": False}
    
    token = authorization.replace("Bearer ", "")
    user_id = verify_session(token)
    
    if not user_id:
        return {"is_favorite": False}
    
    return {"is_favorite": is_favorite(user_id, place_id)}
