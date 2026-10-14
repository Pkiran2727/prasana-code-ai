"""DB pool + auth dependency. DATABASE_URL env var లో Postgres connection string ఉండాలి."""
import os
from contextlib import contextmanager
from psycopg2.pool import ThreadedConnectionPool
from psycopg2.extras import RealDictCursor
from fastapi import Header, HTTPException, Depends

_pool = None

def get_pool():
    global _pool
    if _pool is None:
        dsn = os.environ.get("DATABASE_URL")
        if not dsn:
            raise RuntimeError("DATABASE_URL environment variable is not set.")
        _pool = ThreadedConnectionPool(1, 10, dsn=dsn)
    return _pool


@contextmanager
def get_cursor():
    """ఒక transaction: success అయితే commit, error వస్తే rollback."""
    pool = get_pool()
    conn = pool.getconn()
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            yield cur
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        pool.putconn(conn)


from backend.auth import get_current_user
from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional

security = HTTPBearer(auto_error=False)

def get_current_user_id(credentials: Optional[HTTPAuthorizationCredentials] = Depends(security)) -> str:
    """Uses the auth module to validate user token. Fails closed with 401 if missing or invalid."""
    if credentials:
        user = get_current_user(credentials)
        return user["id"]
    raise HTTPException(status_code=401, detail="Authentication required. Please log in.")

def get_optional_user_id(credentials: Optional[HTTPAuthorizationCredentials] = Depends(security)) -> Optional[str]:
    """Allows anonymous/public access (returns None), but resolves user_id if valid bearer token provided."""
    if credentials:
        try:
            user = get_current_user(credentials)
            return user["id"]
        except Exception:
            return None
    return None


