import os
import logging
from fastapi import APIRouter, HTTPException, Depends, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from backend.database import supabase, get_user_role

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/auth", tags=["auth"])
security = HTTPBearer()

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> dict:
    """
    Dependency injection for FastAPI endpoints to validate the Supabase JWT.
    Returns user details (id, email, role).
    """
    token = credentials.credentials
    if not supabase:
        # Local mock user if Supabase is offline
        logger.warning("Supabase offline. Returning local mock user credentials.")
        return {"id": "00000000-0000-0000-0000-000000000001", "email": "mandaprasannakiran@gmail.com", "role": "admin"}
    try:
        user_res = supabase.auth.get_user(token)
        user = user_res.user
        role = get_user_role(user.email)
        return {
            "id": user.id,
            "email": user.email,
            "role": role
        }
    except Exception as e:
        logger.error(f"JWT validation failed: {e}")
        raise HTTPException(status_code=401, detail="Invalid token or session expired.")

def get_admin_user(current_user: dict = Depends(get_current_user)) -> dict:
    """Dependency to check if user has admin privileges."""
    if current_user.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Admin permissions required.")
    return current_user

# Proxy routes in case frontend prefers to authenticate via FastAPI backend
@router.post("/register")
async def register(payload: dict):
    email = payload.get("email")
    password = payload.get("password")
    if not email or not password:
        raise HTTPException(status_code=400, detail="Email and password required.")
    
    if not supabase:
        # Local mock register
        return {"message": "Registration successful (Mock)."}
        
    try:
        res = supabase.auth.sign_up({"email": email, "password": password})
        # Trigger role mapping profile initialization
        get_user_role(email)
        return {"message": "Registration successful. Please verify email.", "user": res.user}
    except Exception as e:
        logger.error(f"Sign up error: {e}")
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/login")
async def login(payload: dict):
    email = payload.get("email")
    password = payload.get("password")
    if not email or not password:
        raise HTTPException(status_code=400, detail="Email and password required.")
    
    if not supabase:
        # Local mock login
        role = "admin" if email == "mandaprasannakiran@gmail.com" else "user"
        return {
            "access_token": "mock_token",
            "user": {
                "id": "00000000-0000-0000-0000-000000000001",
                "email": email,
                "role": role
            }
        }
        
    try:
        res = supabase.auth.sign_in_with_password({"email": email, "password": password})
        role = get_user_role(email)
        return {
            "access_token": res.session.access_token,
            "user": {
                "id": res.user.id,
                "email": res.user.email,
                "role": role
            }
        }
    except Exception as e:
        logger.error(f"Sign in error: {e}")
        raise HTTPException(status_code=401, detail="Invalid email or password.")
