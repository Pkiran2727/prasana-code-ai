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
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional

security_optional = HTTPBearer(auto_error=False)

def get_current_user_id(credentials: Optional[HTTPAuthorizationCredentials] = Depends(security_optional)) -> str:
    """Uses the auth module if token present, or returns default guest ID."""
    if credentials:
        try:
            user = get_current_user(credentials)
            return user["id"]
        except Exception:
            pass
    return "00000000-0000-0000-0000-000000000001"
