import os
import shutil
import logging
from backend.session_manager import get_session_path, get_user_id_for_session
from backend.database import save_user_file, delete_user_file

logger = logging.getLogger("backend.files")

def secure_resolve_path(session_id: str, relative_path: str) -> str:
    """Resolves a relative path within the session directory and ensures no directory traversal."""
    session_path = get_session_path(session_id)
    
    # Strip any leading slashes or dot-dot components
    cleaned_path = relative_path.lstrip("/").replace("../", "").replace("..\\", "")
    abs_target_path = os.path.abspath(os.path.join(session_path, cleaned_path))
    
    # Verify that the target path is strictly inside the session directory
    if not abs_target_path.startswith(session_path):
        logger.warning(f"Traversals detected! session={session_id}, path={relative_path}")
        raise PermissionError("Access denied: path is outside the session workspace.")
        
    return abs_target_path

def list_files(session_id: str) -> list:
    """Returns a hierarchical directory structure list of all files and folders."""
    session_path = get_session_path(session_id)
    
    if not os.path.exists(session_path):
        raise FileNotFoundError("Session workspace directory does not exist.")
        
    def _walk(current_dir):
        nodes = []
        try:
            items = sorted(os.listdir(current_dir))
        except Exception:
            return nodes
            
        for item in items:
            # Skip hidden files and keepalive files
            if item.startswith('.') or item == ".keep":
                continue
                
            full_path = os.path.join(current_dir, item)
            # Compute relative path using forward slashes for cross-platform frontend compatibility
            rel_path = os.path.relpath(full_path, session_path).replace("\\", "/")
            
            if os.path.isdir(full_path):
                nodes.append({
                    "name": item,
                    "path": rel_path,
                    "type": "directory",
                    "children": _walk(full_path)
                })
            else:
                nodes.append({
                    "name": item,
                    "path": rel_path,
                    "type": "file"
                })
        return nodes

    return _walk(session_path)

def read_file(session_id: str, relative_path: str) -> str:
    """Reads content from a file inside the session workspace."""
    abs_path = secure_resolve_path(session_id, relative_path)
    
    if not os.path.exists(abs_path):
        raise FileNotFoundError(f"File not found: {relative_path}")
        
    if os.path.isdir(abs_path):
        raise IsADirectoryError(f"Path is a directory: {relative_path}")
        
    with open(abs_path, "r", encoding="utf-8") as f:
        return f.read()

def write_file(session_id: str, relative_path: str, content: str):
    """Writes content to a file, creating parent folders if they do not exist."""
    abs_path = secure_resolve_path(session_id, relative_path)
    
    if os.path.isdir(abs_path):
        raise IsADirectoryError(f"Cannot write file, path is a directory: {relative_path}")
        
    # Ensure parent folders exist
    os.makedirs(os.path.dirname(abs_path), exist_ok=True)
    
    with open(abs_path, "w", encoding="utf-8") as f:
        f.write(content)
        
    # Sync with Supabase Storage
    user_id = get_user_id_for_session(session_id)
    if user_id:
        try:
            save_user_file(user_id, relative_path, content)
        except Exception as e:
            logger.error(f"Failed syncing write to Supabase Storage: {e}")
        
    # Update directory timestamp to keep session active
    session_path = get_session_path(session_id)
    os.utime(session_path, None)
    logger.debug(f"Saved file: {relative_path} in session {session_id}")

def create_folder(session_id: str, relative_path: str):
    """Creates a new folder directory under the session workspace."""
    abs_path = secure_resolve_path(session_id, relative_path)
    os.makedirs(abs_path, exist_ok=True)
    
    # Sync folder structure using a .keep file in Supabase Storage
    user_id = get_user_id_for_session(session_id)
    if user_id:
        try:
            save_user_file(user_id, os.path.join(relative_path, ".keep"), "")
        except Exception as e:
            logger.error(f"Failed syncing folder creation to Supabase Storage: {e}")
            
    # Touch session dir to extend TTL
    session_path = get_session_path(session_id)
    os.utime(session_path, None)
    logger.debug(f"Created folder: {relative_path} in session {session_id}")

def delete_path(session_id: str, relative_path: str) -> bool:
    """Removes a file or folder directory recursively."""
    abs_path = secure_resolve_path(session_id, relative_path)
    
    if not os.path.exists(abs_path):
        raise FileNotFoundError(f"Path does not exist: {relative_path}")
        
    try:
        user_id = get_user_id_for_session(session_id)
        
        # If directory, we need to list and delete recursively from Supabase Storage
        if os.path.isdir(abs_path):
            if user_id:
                # Find all files inside this directory locally to delete from Supabase
                for root, _, files in os.walk(abs_path):
                    for file in files:
                        local_file_path = os.path.join(root, file)
                        rel_file_path = os.path.relpath(local_file_path, get_session_path(session_id))
                        try:
                            delete_user_file(user_id, rel_file_path)
                        except Exception as se:
                            logger.error(f"Failed deleting file {rel_file_path} from Supabase: {se}")
            shutil.rmtree(abs_path)
        else:
            if user_id:
                try:
                    delete_user_file(user_id, relative_path)
                except Exception as se:
                    logger.error(f"Failed deleting file {relative_path} from Supabase: {se}")
            os.remove(abs_path)
            
        # Touch session dir to extend TTL
        session_path = get_session_path(session_id)
        os.utime(session_path, None)
        logger.debug(f"Deleted path: {relative_path} in session {session_id}")
        return True
    except Exception as e:
        logger.error(f"Failed to delete {relative_path} in session {session_id}: {e}")
        return False
