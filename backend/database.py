import os
import logging
from supabase import create_client, Client

logger = logging.getLogger(__name__)

SUPABASE_URL = os.environ.get("SUPABASE_URL", "")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY", "")

# Initialize client lazily to avoid throwing errors if credentials aren't loaded yet
supabase: Client = None
try:
    if SUPABASE_URL and SUPABASE_KEY:
        supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
        logger.info("Supabase client initialized successfully.")
    else:
        logger.warning("Supabase credentials not found in env. DB integration running in fallback mode.")
except Exception as e:
    logger.error(f"Error initializing Supabase client: {e}")

BUCKET_NAME = "user-workspaces"

# --- Storage Methods ---

def ensure_bucket_exists():
    """Ensures our workspace storage bucket is active."""
    if not supabase:
        return
    try:
        buckets = supabase.storage.list_buckets()
        exists = any(b.name == BUCKET_NAME for b in buckets)
        if not exists:
            supabase.storage.create_bucket(BUCKET_NAME, options={"public": False})
            logger.info(f"Created Supabase storage bucket '{BUCKET_NAME}'")
    except Exception as e:
        logger.error(f"Failed to check/create bucket: {e}")

def save_user_file(user_id: str, filepath: str, content: bytes or str) -> bool:
    """Uploads/overwrites a file in the user's workspace bucket."""
    if not supabase:
        # Local fallback if Supabase not configured
        local_path = os.path.join("workspace", user_id, filepath)
        os.makedirs(os.path.dirname(local_path), exist_ok=True)
        mode = "wb" if isinstance(content, bytes) else "w"
        with open(local_path, mode, encoding=None if isinstance(content, bytes) else "utf-8") as f:
            f.write(content)
        return True

    try:
        ensure_bucket_exists()
        destination = f"{user_id}/{filepath.lstrip('/')}"
        data = content if isinstance(content, bytes) else content.encode("utf-8")
        
        # Check if file exists to decide on upload or update
        try:
            supabase.storage.from_(BUCKET_NAME).upload(
                path=destination,
                file=data,
                file_options={"content-type": "text/plain", "x-upsert": "true"}
            )
        except Exception:
            # Fallback update if upload fails (upsert not working as expected on some buckets)
            supabase.storage.from_(BUCKET_NAME).update(
                path=destination,
                file=data,
                file_options={"content-type": "text/plain"}
            )
        return True
    except Exception as e:
        logger.error(f"Error saving file to Supabase: {e}")
        return False

def read_user_file(user_id: str, filepath: str) -> str:
    """Downloads file content from the user's workspace bucket."""
    if not supabase:
        local_path = os.path.join("workspace", user_id, filepath)
        if os.path.exists(local_path):
            with open(local_path, "r", encoding="utf-8") as f:
                return f.read()
        return ""

    try:
        destination = f"{user_id}/{filepath.lstrip('/')}"
        response = supabase.storage.from_(BUCKET_NAME).download(destination)
        return response.decode("utf-8")
    except Exception as e:
        logger.error(f"Error reading file from Supabase: {e}")
        return ""

def delete_user_file(user_id: str, filepath: str) -> bool:
    """Deletes a file from the user's workspace bucket."""
    if not supabase:
        local_path = os.path.join("workspace", user_id, filepath)
        if os.path.exists(local_path):
            os.remove(local_path)
            return True
        return False

    try:
        destination = f"{user_id}/{filepath.lstrip('/')}"
        supabase.storage.from_(BUCKET_NAME).remove([destination])
        return True
    except Exception as e:
        logger.error(f"Error deleting file from Supabase: {e}")
        return False

def list_user_files(user_id: str) -> list:
    """Lists files under user_id/ in the bucket."""
    if not supabase:
        local_dir = os.path.join("workspace", user_id)
        if not os.path.exists(local_dir):
            return []
        files = []
        for root, _, filenames in os.walk(local_dir):
            for f in filenames:
                full = os.path.join(root, f)
                rel = os.path.relpath(full, local_dir)
                files.append({"name": rel, "metadata": {"size": os.path.getsize(full)}})
        return files

    try:
        ensure_bucket_exists()
        # Storage list lists folder contents
        res = supabase.storage.from_(BUCKET_NAME).list(user_id)
        files = []
        for item in res:
            if item.get("id") is not None:  # is a file
                files.append({
                    "name": item["name"],
                    "metadata": {"size": item.get("metadata", {}).get("size", 0)}
                })
        return files
    except Exception as e:
        logger.error(f"Error listing files in Supabase: {e}")
        return []

# --- DB Profiles & Engagement Logging ---

# In-memory stores for local fallback mode
mock_user_profiles = [{"email": "mandaprasannakiran@gmail.com", "role": "admin"}]
mock_engagement_logs = []
mock_audit_logs = []

def get_user_role(user_email: str) -> str:
    """Returns 'admin' or 'user' based on email/profile mapping."""
    if not supabase:
        # Local fallback based on email pattern
        role = "admin" if user_email == "mandaprasannakiran@gmail.com" else "user"
        if not any(u["email"] == user_email for u in mock_user_profiles):
            mock_user_profiles.append({"id": f"mock_u_{len(mock_user_profiles)+1}", "email": user_email, "role": role})
        return role

    try:
        # Query user_profiles table
        res = supabase.table("user_profiles").select("role").eq("email", user_email).execute()
        if res.data:
            return res.data[0]["role"]
        
        # Default profile creation
        role = "admin" if user_email == "mandaprasannakiran@gmail.com" else "user"
        supabase.table("user_profiles").insert({"email": user_email, "role": role}).execute()
        return role
    except Exception as e:
        logger.error(f"Error fetching user role: {e}")
        return "user"

def log_engagement_ping(user_id: str, email: str, ip: str, session_id: str):
    """Logs active engagement and updates last heartbeat time."""
    if not supabase:
        # Local in-memory logging
        found = False
        for log in mock_engagement_logs:
            if log["session_id"] == session_id:
                log["engagement_seconds"] += 30
                log["ip_address"] = ip
                log["email"] = email
                found = True
                break
        if not found:
            mock_engagement_logs.append({
                "user_id": user_id,
                "email": email,
                "ip_address": ip,
                "session_id": session_id,
                "engagement_seconds": 30
            })
        return

    try:
        # Upsert engagement log
        res = supabase.table("engagement_logs").select("id, engagement_seconds").eq("session_id", session_id).execute()
        if res.data:
            row_id = res.data[0]["id"]
            current_seconds = res.data[0].get("engagement_seconds", 0)
            supabase.table("engagement_logs").update({
                "engagement_seconds": current_seconds + 30,
                "ip_address": ip,
                "email": email
            }).eq("id", row_id).execute()
        else:
            supabase.table("engagement_logs").insert({
                "user_id": user_id,
                "email": email,
                "ip_address": ip,
                "session_id": session_id,
                "engagement_seconds": 30
            }).execute()
    except Exception as e:
        logger.error(f"Failed to log engagement heartbeat: {e}")

def log_audit_action(user_id: str, email: str, action: str, details: str):
    """Inserts a security audit record into DB."""
    if not supabase:
        import datetime
        mock_audit_logs.insert(0, {
            "id": f"mock_l_{len(mock_audit_logs)+1}",
            "user_id": user_id,
            "email": email,
            "action": action,
            "details": details,
            "created_at": datetime.datetime.utcnow().isoformat()
        })
        logger.info(f"AUDIT LOG (Local): User {email} did {action} - {details}")
        return

    try:
        supabase.table("audit_logs").insert({
            "user_id": user_id,
            "email": email,
            "action": action,
            "details": details
        }).execute()
    except Exception as e:
        logger.error(f"Failed to log audit action: {e}")

def get_admin_metrics() -> dict:
    """Gathers overall usage stats for the Admin Dashboard."""
    if not supabase:
        return {
            "users": mock_user_profiles,
            "engagement": mock_engagement_logs,
            "logs": mock_audit_logs[:50]
        }
    try:
        # 1. Fetch profiles
        profiles_res = supabase.table("user_profiles").select("*").execute()
        users = profiles_res.data or []

        # 2. Fetch engagement totals
        engagement_res = supabase.table("engagement_logs").select("*").execute()
        engagement = engagement_res.data or []

        # 3. Fetch audit logs
        audit_res = supabase.table("audit_logs").select("*").order("created_at", desc=True).limit(50).execute()
        logs = audit_res.data or []

        return {
            "users": users,
            "engagement": engagement,
            "logs": logs
        }
    except Exception as e:
        logger.error(f"Failed to retrieve admin dashboard metrics: {e}")
        return {"users": [], "engagement": [], "logs": []}
