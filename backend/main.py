import os
import json
import asyncio
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, BackgroundTasks, Depends, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from backend.config import BASE_DIR, CORS_ORIGINS
from backend.session_manager import (
    create_session, 
    destroy_session, 
    check_session_exists, 
    cleanup_old_sessions,
    get_user_id_for_session
)
from backend.file_manager import (
    list_files, 
    read_file, 
    write_file, 
    create_folder, 
    delete_path
)
from backend.code_runner import run_code
from backend.agent import execute_agent_loop
from backend.auth import router as auth_router, get_current_user
from backend.admin_routes import router as admin_router
from backend.curriculum import router as curriculum_router
from backend.curriculum_routes import router as legacy_curriculum_router
from backend.payment_routes import router as payment_router
from backend.gamification_routes import router as gamification_router
from backend.database import supabase


# Setup logging configuration
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("backend.main")

# Asynchronous background loop for garbage collection
async def periodic_session_cleanup():
    while True:
        try:
            cleanup_old_sessions()
        except Exception as e:
            logger.error(f"Error running periodic session garbage collection: {e}")
        # Clean up every 30 minutes
        await asyncio.sleep(1800)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup actions
    logger.info("Initializing Prasana Code AI backend service...")
    cleanup_task = asyncio.create_task(periodic_session_cleanup())
    yield
    # Shutdown actions
    logger.info("Stopping Prasana Code AI backend service...")
    cleanup_task.cancel()
    try:
        await cleanup_task
    except asyncio.CancelledError:
        pass

app = FastAPI(
    title="Prasana Code AI Backend API",
    description="Workspace session, curriculum, gamification, and payment API service for Prasana Code AI",
    version="1.0.0",
    lifespan=lifespan
)

# Configure CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(auth_router)
app.include_router(admin_router)
app.include_router(curriculum_router)
app.include_router(legacy_curriculum_router)
app.include_router(payment_router)
app.include_router(gamification_router)

# Request Models
class CreateNodeRequest(BaseModel):
    path: str = Field(..., description="Relative path of the new file or directory")
    type: str = Field("file", description="Type of workspace node: 'file' or 'directory'")
    content: str = Field("", description="Optional initial content for files")

class UpdateFileRequest(BaseModel):
    content: str = Field(..., description="Updated file content string")

# Helper to verify session exists and belongs to the authenticated user
def require_session(session_id: str, current_user: dict = Depends(get_current_user)):
    if not check_session_exists(session_id):
        raise HTTPException(status_code=404, detail="Workspace session not found or expired.")
        
    owner_id = get_user_id_for_session(session_id)
    if owner_id and owner_id != current_user["id"]:
        raise HTTPException(status_code=403, detail="Access denied: You do not own this session.")
        
    return session_id

# Endpoint: Create session workspace
@app.post("/session/create", status_code=201)
def api_create_session(current_user: dict = Depends(get_current_user)):
    try:
        session_id = create_session(user_id=current_user["id"], email=current_user["email"])
        return {"session_id": session_id}
    except Exception as e:
        logger.error(f"Failed to initialize session: {e}")
        raise HTTPException(status_code=500, detail="Internal server error initializing workspace session.")

# Endpoint: Destroy session workspace
@app.delete("/session/{session_id}")
def api_destroy_session(session_id: str, current_user: dict = Depends(get_current_user)):
    # Verify ownership before destroying
    if check_session_exists(session_id):
        owner_id = get_user_id_for_session(session_id)
        if owner_id and owner_id != current_user["id"]:
            raise HTTPException(status_code=403, detail="Access denied: You do not own this session.")
            
    success = destroy_session(session_id)
    if not success:
        raise HTTPException(status_code=404, detail="Session not found or already deleted.")
    return {"status": "success", "message": f"Session {session_id} destroyed."}

# Endpoint: List session workspace files
@app.get("/files/{session_id}")
def api_list_files(session_id: str = Depends(require_session)):
    try:
        files = list_files(session_id)
        return {"files": files}
    except Exception as e:
        logger.error(f"Failed listing files for session {session_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal error listing workspace files.")

# Endpoint: Create file or directory inside session workspace
@app.post("/files/{session_id}")
def api_create_node(req: CreateNodeRequest, session_id: str = Depends(require_session)):
    try:
        if req.type == "directory":
            create_folder(session_id, req.path)
        else:
            write_file(session_id, req.path, req.content)
        return {"status": "success", "message": f"Created {req.type} at {req.path}"}
    except PermissionError as pe:
        raise HTTPException(status_code=403, detail=str(pe))
    except Exception as e:
        logger.error(f"Failed creating node {req.path} in session {session_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint: Read file contents
@app.get("/files/{session_id}/{file_path:path}")
def api_read_file(file_path: str, session_id: str = Depends(require_session)):
    try:
        content = read_file(session_id, file_path)
        # Determine language from extension
        ext = file_path.split(".")[-1] if "." in file_path else "plaintext"
        language_map = {
            "py": "python",
            "js": "javascript",
            "ts": "typescript",
            "java": "java",
            "cpp": "cpp",
            "c": "c",
            "go": "go",
            "rs": "rust",
            "sh": "bash"
        }
        language = language_map.get(ext, "plaintext")
        return {
            "path": file_path,
            "content": content,
            "language": language
        }
    except PermissionError as pe:
        raise HTTPException(status_code=403, detail=str(pe))
    except FileNotFoundError as fe:
        raise HTTPException(status_code=404, detail=str(fe))
    except IsADirectoryError as de:
        raise HTTPException(status_code=400, detail=str(de))
    except Exception as e:
        logger.error(f"Error reading file {file_path} in session {session_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error reading file.")

# Endpoint: Update/write file contents
@app.put("/files/{session_id}/{file_path:path}")
def api_update_file(file_path: str, req: UpdateFileRequest, session_id: str = Depends(require_session)):
    try:
        write_file(session_id, file_path, req.content)
        return {"status": "success", "message": f"Updated file {file_path}"}
    except PermissionError as pe:
        raise HTTPException(status_code=403, detail=str(pe))
    except IsADirectoryError as de:
        raise HTTPException(status_code=400, detail=str(de))
    except Exception as e:
        logger.error(f"Error updating file {file_path} in session {session_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error updating file.")

# Endpoint: Delete file or directory inside session workspace
@app.delete("/files/{session_id}/{file_path:path}")
def api_delete_node(file_path: str, session_id: str = Depends(require_session)):
    try:
        delete_path(session_id, file_path)
        return {"status": "success", "message": f"Deleted {file_path}"}
    except PermissionError as pe:
        raise HTTPException(status_code=403, detail=str(pe))
    except FileNotFoundError as fe:
        raise HTTPException(status_code=404, detail=str(fe))
    except Exception as e:
        logger.error(f"Error deleting path {file_path} in session {session_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error deleting path.")

class RunRequest(BaseModel):
    path: str = Field(..., description="Relative path of the script file to execute")

# Endpoint: Run code inside workspace sandbox via Piston API
@app.post("/run/{session_id}")
async def api_run_code(req: RunRequest, session_id: str = Depends(require_session)):
    try:
        result = await run_code(session_id, req.path)
        return result
    except Exception as e:
        logger.error(f"Error executing code in session {session_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error running code.")

# WebSocket Endpoint: Stream token chunks and tool updates for AI Agent
@app.websocket("/ws/{session_id}")
async def websocket_endpoint(websocket: WebSocket, session_id: str, token: str = None):
    # Verify session before accepting connection
    if not check_session_exists(session_id):
        await websocket.close(code=4004)
        return
        
    # Check JWT Ownership if Supabase is active
    if supabase and token and token != "mock_token":
        try:
            user_res = supabase.auth.get_user(token)
            user = user_res.user
            owner_id = get_user_id_for_session(session_id)
            if owner_id and owner_id != user.id:
                await websocket.close(code=4003)
                return
        except Exception as e:
            logger.error(f"WebSocket auth failed: {e}")
            await websocket.close(code=4002)
            return

    await websocket.accept()
    logger.info(f"WebSocket client connected to session {session_id}")
    
    # Track active agent task so we can cancel it on request
    active_agent_task: asyncio.Task | None = None

    # Persistent multi-turn conversation history for this session
    # Initialised once with the system prompt, then grows across all prompts
    conversation_history = [
        {"role": "system", "content": "You are an advanced AI coding assistant that operates on a sandboxed workspace. You can read, write, and run code files. Respond ONLY in structured JSON format as defined in your system instructions."}
    ]
    
    try:
        while True:
            # Receive user message
            data = await websocket.receive_text()
            try:
                msg = json.loads(data)
            except Exception:
                msg = {"prompt": data}

            msg_type = msg.get("type", "prompt")

            # --- Handle Stop Signal ---
            if msg_type == "stop":
                if active_agent_task and not active_agent_task.done():
                    active_agent_task.cancel()
                    logger.info(f"Agent task cancelled by user for session {session_id}")
                    await websocket.send_json({
                        "type": "agent_stopped",
                        "text": "⛔ Agent execution stopped by user."
                    })
                continue

            # --- Handle Prompt ---
            prompt = msg.get("prompt", "")
            if not prompt:
                continue
                
            logger.info(f"Agent prompt received: '{prompt[:100]}...'")
            
            # Callback function to stream agent events back to UI
            async def stream_callback(event_data: dict):
                try:
                    await websocket.send_json(event_data)
                except Exception as send_err:
                    logger.error(f"Failed to send websocket message: {send_err}")
            
            # Wrap agent execution in a cancellable Task
            async def run_agent():
                try:
                    await execute_agent_loop(session_id, prompt, stream_callback, conversation_history)
                except asyncio.CancelledError:
                    logger.info(f"Agent loop cancelled mid-execution for session {session_id}")

            active_agent_task = asyncio.create_task(run_agent())
            await active_agent_task
            
    except WebSocketDisconnect:
        logger.info(f"WebSocket client disconnected from session {session_id}")
        if active_agent_task and not active_agent_task.done():
            active_agent_task.cancel()
    except Exception as ws_err:
        logger.error(f"WebSocket error in session {session_id}: {ws_err}")
        try:
            await websocket.close()
        except Exception:
            pass

# Static files mount - serve compiled React frontend if built
frontend_dist = os.path.join(BASE_DIR, "frontend", "dist")
if os.path.exists(frontend_dist):
    logger.info(f"Mounting production React client static assets from {frontend_dist}")
    app.mount("/", StaticFiles(directory=frontend_dist, html=True), name="static")
else:
    logger.warning("React production build files directory not found. Serving API routes only.")
