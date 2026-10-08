import os
import uuid
import shutil
import time
import re
import logging
from backend.config import SESSIONS_DIR, SESSION_TTL_MINUTES

logger = logging.getLogger("backend.sessions")

# Compile a basic regex to validate UUID formats for session safety
UUID_REGEX = re.compile(r"^[a-fA-F0-9]{8}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{12}$")

DEFAULT_FIBONACCI_CODE = """# Fibonacci implementation with a bug
def fibonacci(n):
    if n <= 1:
        return n
    # BUG: calling fib instead of fibonacci
    return fib(n-1) + fib(n-2)

print("Fibonacci sequence for 10 terms:")
for i in range(10):
    print(fibonacci(i), end=" ")
print()
"""

DEFAULT_UTILS_CODE = """# Helper utilities for string operations
def reverse_string(s):
    return s[::-1]

def uppercase_string(s):
    return s.upper()
"""

DEFAULT_TESTS_CODE = """import unittest
from main import fibonacci

class TestFibonacci(unittest.TestCase):
    def test_fib(self):
        self.assertEqual(fibonacci(0), 0)
        self.assertEqual(fibonacci(1), 1)

if __name__ == "__main__":
    unittest.main()
"""

# Global in-memory map of session_id to user_id (and email)
SESSION_TO_USER = {}

def get_user_id_for_session(session_id: str) -> str or None:
    return SESSION_TO_USER.get(session_id, {}).get("id")

def get_user_email_for_session(session_id: str) -> str or None:
    return SESSION_TO_USER.get(session_id, {}).get("email")

def is_safe_session_id(session_id: str) -> bool:
    """Validate that session_id contains only safe alphanumeric/hyphen/underscore characters."""
    if not session_id or ".." in session_id or "/" in session_id or "\\" in session_id:
        return False
    return bool(re.match(r"^[a-zA-Z0-9_-]+$", session_id))

def get_session_path(session_id: str) -> str:
    """Return absolute path to session directory if safe."""
    user_id = get_user_id_for_session(session_id)
    if user_id:
        path = os.path.abspath(os.path.join(SESSIONS_DIR, user_id))
        os.makedirs(path, exist_ok=True)
        return path
        
    if not is_safe_session_id(session_id):
        raise ValueError("Invalid or unsafe session_id format")
    return os.path.abspath(os.path.join(SESSIONS_DIR, session_id))

def create_session(user_id: str = None, email: str = None) -> str:
    """Creates a new workspace session and syncs/initializes files with Supabase."""
    session_id = str(uuid.uuid4())
    
    if user_id and email:
        SESSION_TO_USER[session_id] = {"id": user_id, "email": email}
        
    session_path = get_session_path(session_id)
    os.makedirs(session_path, exist_ok=True)
    
    # Try syncing from Supabase Storage first
    from backend.database import list_user_files, read_user_file, save_user_file
    
    db_files = []
    if user_id:
        try:
            db_files = list_user_files(user_id)
        except Exception as err:
            logger.error(f"Failed to list Supabase files for user {user_id}: {err}")
            
    if db_files:
        logger.info(f"Syncing {len(db_files)} files from Supabase for user {user_id}...")
        for db_file in db_files:
            name = db_file["name"]
            content = read_user_file(user_id, name)
            local_file_path = os.path.join(session_path, name)
            os.makedirs(os.path.dirname(local_file_path), exist_ok=True)
            with open(local_file_path, "w", encoding="utf-8") as f:
                f.write(content)
    else:
        # Default initialization for new users
        logger.info(f"Initializing default workspace template for user {user_id or 'anonymous'}")
        
        main_path = os.path.join(session_path, "main.py")
        utils_path = os.path.join(session_path, "utils.py")
        tests_dir = os.path.join(session_path, "tests")
        test_main_path = os.path.join(tests_dir, "test_main.py")
        
        os.makedirs(tests_dir, exist_ok=True)
        
        with open(main_path, "w", encoding="utf-8") as f:
            f.write(DEFAULT_FIBONACCI_CODE)
        with open(utils_path, "w", encoding="utf-8") as f:
            f.write(DEFAULT_UTILS_CODE)
        with open(test_main_path, "w", encoding="utf-8") as f:
            f.write(DEFAULT_TESTS_CODE)
            
        # Upload these initial files to Supabase if logged in
        if user_id:
            try:
                save_user_file(user_id, "main.py", DEFAULT_FIBONACCI_CODE)
                save_user_file(user_id, "utils.py", DEFAULT_UTILS_CODE)
                save_user_file(user_id, "tests/test_main.py", DEFAULT_TESTS_CODE)
            except Exception as err:
                logger.error(f"Failed saving initial files to Supabase: {err}")
        
    logger.info(f"Created session workspace: {session_id} mapped to user {user_id}")
    return session_id

def destroy_session(session_id: str) -> bool:
    """Deletes session workspace files and directory."""
    try:
        session_path = get_session_path(session_id)
        if os.path.exists(session_path):
            shutil.rmtree(session_path)
            logger.info(f"Destroyed session workspace: {session_id}")
        if session_id in SESSION_TO_USER:
            del SESSION_TO_USER[session_id]
        return True
    except Exception as e:
        logger.error(f"Error destroying session {session_id}: {e}")
    return False

def check_session_exists(session_id: str) -> bool:
    """Checks if a session is currently active and on disk."""
    if session_id in SESSION_TO_USER:
        return True
    try:
        session_path = get_session_path(session_id)
        return os.path.exists(session_path) and os.path.isdir(session_path)
    except ValueError:
        return False

def cleanup_old_sessions():
    """Garbage collector background task to clean up old session folders."""
    logger.info("Starting session garbage collection pass...")
    now = time.time()
    ttl_seconds = SESSION_TTL_MINUTES * 60
    
    if not os.path.exists(SESSIONS_DIR):
        return

    cleaned_count = 0
    for folder in os.listdir(SESSIONS_DIR):
        if not is_safe_session_id(folder):
            continue
            
        folder_path = os.path.join(SESSIONS_DIR, folder)
        if not os.path.isdir(folder_path):
            continue
            
        # Check folder last modified timestamp
        mtime = os.path.getmtime(folder_path)
        age_seconds = now - mtime
        
        if age_seconds > ttl_seconds:
            try:
                shutil.rmtree(folder_path)
                logger.info(f"Garbage collector deleted expired session: {folder} (Age: {age_seconds/60:.1f}m)")
                cleaned_count += 1
            except Exception as e:
                logger.error(f"Failed to garbage collect session folder {folder}: {e}")
                
    if cleaned_count > 0:
        logger.info(f"Garbage collection completed. Cleaned {cleaned_count} expired sessions.")
