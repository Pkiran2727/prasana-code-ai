import os
import logging
from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from backend.database import supabase, get_user_role

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/auth", tags=["auth"])
security = HTTPBearer()

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> dict:
    """
    Dependency injection to validate authentication credentials.
    Fails closed: strictly rejects mock tokens, empty tokens, and invalid signatures.
    """
    token = credentials.credentials
    if not token or not token.strip():
        raise HTTPException(status_code=401, detail="Authentication required. Please log in.")
        
    if not supabase:
        logger.error("Authentication service (Supabase) is not configured.")
        raise HTTPException(status_code=503, detail="Authentication service unavailable.")

    try:
        user_res = supabase.auth.get_user(token)
        user = user_res.user
        if not user:
            raise HTTPException(status_code=401, detail="Invalid token session.")
            
        role = get_user_role(user.email)
        return {
            "id": user.id,
            "email": user.email,
            "role": role
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"JWT validation failed: {e}")
        raise HTTPException(status_code=401, detail="Invalid token or session expired.")

def get_admin_user(current_user: dict = Depends(get_current_user)) -> dict:
    """Dependency to check if user has admin privileges."""
    if current_user.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Admin permissions required.")
    return current_user

@router.post("/register")
async def register(payload: dict):
    email = payload.get("email")
    password = payload.get("password")
    if not email or not password:
        raise HTTPException(status_code=400, detail="Email and password required.")
    
    if not supabase:
        raise HTTPException(status_code=503, detail="Authentication service unavailable.")
        
    try:
        res = supabase.auth.sign_up({"email": email, "password": password})
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
        raise HTTPException(status_code=503, detail="Authentication service unavailable.")
        
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

@router.get("/oauth/{provider}")
async def get_oauth_url(provider: str, redirect_to: str = None):
    if not supabase:
        raise HTTPException(status_code=503, detail="Authentication service unavailable.")
    try:
        options = {}
        if redirect_to:
            options["redirect_to"] = redirect_to
        res = supabase.auth.get_oauth_sign_in_url(provider, options=options)
        return {"url": res.url if hasattr(res, "url") else str(res)}
    except Exception as e:
        logger.error(f"OAuth URL error: {e}")
        raise HTTPException(status_code=400, detail=str(e))

