import logging
from fastapi import APIRouter, Depends, Request, HTTPException
from backend.auth import get_admin_user, get_current_user
from backend.database import get_admin_metrics, log_engagement_ping, delete_user_file, list_user_files

logger = logging.getLogger(__name__)

router = APIRouter(tags=["admin"])

@router.get("/admin/metrics", dependencies=[Depends(get_admin_user)])
async def fetch_metrics():
    """Returns analytics data (users, engagement, audit logs) for the admin Monitor."""
    try:
        metrics = get_admin_metrics()
        return metrics
    except Exception as e:
        logger.error(f"Error fetching admin metrics: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve metrics.")

@router.post("/engagement/ping")
async def ping_heartbeat(request: Request, current_user: dict = Depends(get_current_user)):
    """Receives client pings every 30s to update user engagement duration."""
    try:
        # Resolve IP Address
        ip = request.client.host
        # Forward headers if running behind Modal or Nginx proxies
        forwarded = request.headers.get("X-Forwarded-For")
        if forwarded:
            ip = forwarded.split(",")[0].strip()
            
        session_id = request.headers.get("X-Session-ID", "unknown_session")
        
        log_engagement_ping(
            user_id=current_user["id"],
            email=current_user["email"],
            ip=ip,
            session_id=session_id
        )
        return {"status": "heartbeat_saved"}
    except Exception as e:
        logger.error(f"Error processing engagement ping: {e}")
        return {"status": "error", "message": str(e)}

@router.get("/admin/files/{user_id}", dependencies=[Depends(get_admin_user)])
async def list_files(user_id: str):
    """Lists files for a specific user."""
    return list_user_files(user_id)

@router.delete("/admin/files/{user_id}/{filename}", dependencies=[Depends(get_admin_user)])
async def remove_file(user_id: str, filename: str):
    """Deletes a specific user's file."""
    res = delete_user_file(user_id, filename)
    if res:
        return {"status": "file_deleted"}
    else:
        raise HTTPException(status_code=404, detail="File not found.")
