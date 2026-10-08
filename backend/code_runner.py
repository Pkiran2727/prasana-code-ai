import os
import sys
import asyncio
import logging
import subprocess
import httpx
from backend.config import SESSIONS_DIR

logger = logging.getLogger(__name__)

# Map file extensions to language names
EXTENSION_MAP = {
    ".py": "python",
    ".js": "javascript",
    ".ts": "typescript",
    ".go": "go",
    ".cpp": "cpp",
    ".c": "c",
    ".sh": "bash",
}

async def run_code(session_id: str, relative_path: str) -> dict:
    """
    Executes a script file from a session workspace sandbox.
    Uses local execution (with compilation where necessary) as primary executor,
    and falls back to Piston API if local execution is not supported or fails.
    """
    from backend.session_manager import get_session_path
    try:
        session_path = get_session_path(session_id)
    except Exception:
        session_path = os.path.abspath(os.path.join(SESSIONS_DIR, session_id))
    target_path = os.path.abspath(os.path.join(session_path, relative_path))

    if not target_path.startswith(session_path):
        return {
            "stdout": "",
            "stderr": "Access denied: Path traversal detected.",
            "exit_code": 1
        }

    if not os.path.exists(target_path) or os.path.isdir(target_path):
        return {
            "stdout": "",
            "stderr": f"Error: File '{relative_path}' not found in workspace.",
            "exit_code": 1
        }

    _, ext = os.path.splitext(relative_path)
    language = EXTENSION_MAP.get(ext.lower())

    if not language:
        return {
            "stdout": "",
            "stderr": f"Error: Language runner not supported for extension '{ext}'",
            "exit_code": 1
        }

    # --- 1. Primary: Local Subprocess Execution ---
    cmd = []
    binary_path = None

    if language == "python":
        cmd = [sys.executable, target_path]
    elif language == "javascript":
        cmd = ["node", target_path]
    elif language == "typescript":
        cmd = ["node", "--experimental-strip-types", target_path]
    elif language == "bash":
        cmd = ["bash", target_path]
    elif language == "cpp":
        binary_path = os.path.join(session_path, f"bin_{os.path.basename(target_path)}")
        # Compile using g++
        compile_cmd = ["g++", "-O3", "-std=c++20", target_path, "-o", binary_path]
        try:
            logger.info(f"Compiling C++ locally: {compile_cmd}")
            proc = await asyncio.create_subprocess_exec(
                *compile_cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                cwd=session_path
            )
            stdout, stderr = await asyncio.wait_for(proc.communicate(), timeout=15.0)
            if proc.returncode != 0:
                return {
                    "stdout": stdout.decode("utf-8", errors="replace"),
                    "stderr": "Compilation Error:\n" + stderr.decode("utf-8", errors="replace"),
                    "exit_code": proc.returncode
                }
            cmd = [binary_path]
        except Exception as compile_err:
            logger.warning(f"C++ local compilation failed: {compile_err}")

    elif language == "c":
        binary_path = os.path.join(session_path, f"bin_{os.path.basename(target_path)}")
        # Compile using gcc
        compile_cmd = ["gcc", "-O3", target_path, "-o", binary_path]
        try:
            logger.info(f"Compiling C locally: {compile_cmd}")
            proc = await asyncio.create_subprocess_exec(
                *compile_cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                cwd=session_path
            )
            stdout, stderr = await asyncio.wait_for(proc.communicate(), timeout=15.0)
            if proc.returncode != 0:
                return {
                    "stdout": stdout.decode("utf-8", errors="replace"),
                    "stderr": "Compilation Error:\n" + stderr.decode("utf-8", errors="replace"),
                    "exit_code": proc.returncode
                }
            cmd = [binary_path]
        except Exception as compile_err:
            logger.warning(f"C local compilation failed: {compile_err}")

    if cmd:
        try:
            logger.info(f"Executing locally: {cmd} (cwd={session_path})")
            proc = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                cwd=session_path
            )
            stdout, stderr = await asyncio.wait_for(proc.communicate(), timeout=5.0)
            
            # Clean up binary if compiled
            if binary_path and os.path.exists(binary_path):
                try:
                    os.remove(binary_path)
                except Exception:
                    pass

            return {
                "stdout": stdout.decode("utf-8", errors="replace"),
                "stderr": stderr.decode("utf-8", errors="replace"),
                "exit_code": proc.returncode
            }
        except asyncio.TimeoutError:
            try:
                proc.kill()
            except Exception:
                pass
            if binary_path and os.path.exists(binary_path):
                try:
                    os.remove(binary_path)
                except Exception:
                    pass
            return {
                "stdout": "",
                "stderr": "Time Limit Exceeded (TLE): Code execution exceeded 5.0 seconds limit.",
                "exit_code": -1
            }
        except Exception as local_err:
            logger.warning(f"Local run failed, attempting Piston fallback: {local_err}")
            if binary_path and os.path.exists(binary_path):
                try:
                    os.remove(binary_path)
                except Exception:
                    pass

    # --- 2. Fallback: Call public Piston API ---
    try:
        with open(target_path, "r", encoding="utf-8") as f:
            content = f.read()
    except Exception as e:
        return {
            "stdout": "",
            "stderr": f"Error reading file content: {str(e)}",
            "exit_code": 1
        }

    piston_url = "https://emkc.org/api/v2/piston/execute"
    payload = {
        "language": language,
        "version": "*",
        "files": [
            {
                "name": os.path.basename(relative_path),
                "content": content
            }
        ]
    }

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(piston_url, json=payload, timeout=15.0)
            
        if response.status_code != 200:
            return {
                "stdout": "",
                "stderr": f"Piston execution API error: Status {response.status_code}\n{response.text}",
                "exit_code": 1
            }
            
        data = response.json()
        run_result = data.get("run", {})
        
        return {
            "stdout": run_result.get("stdout", ""),
            "stderr": run_result.get("stderr", ""),
            "exit_code": run_result.get("code", 0)
        }
        
    except httpx.RequestError as e:
        logger.error(f"Piston connection failed: {e}")
        return {
            "stdout": "",
            "stderr": f"Code Execution Failed: Unable to contact sandbox runner ({str(e)})",
            "exit_code": 1
        }
