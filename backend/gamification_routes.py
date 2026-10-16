"""
Gamification & Leaderboard API Routes
"""

from fastapi import APIRouter
from backend.gamification_data import MOCK_LEADERBOARD, USER_STATS, CERTIFICATES

router = APIRouter(prefix="/api/gamification", tags=["gamification"])

@router.get("/user-stats")
def get_user_stats():
    """Returns current user XP, streak, completed lessons, and badges."""
    return {"status": "success", "stats": USER_STATS}

@router.get("/leaderboard")
def get_leaderboard():
    """Returns global XP & streak leaderboard."""
    return {"status": "success", "leaderboard": MOCK_LEADERBOARD}

@router.get("/certificates")
def get_certificates():
    """Returns user verified certificates."""
    return {"status": "success", "certificates": CERTIFICATES}
