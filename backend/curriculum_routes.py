"""
Curriculum & Practice Problem Routes for Prasana Code AI
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List
from backend.curriculum_data import JOURNEYS_DATA, PRACTICE_PROBLEMS
from backend.code_runner import run_code
import os

router = APIRouter(prefix="/api", tags=["curriculum"])

from backend.progress_service import run_code as sandbox_run_code

class VerifySolutionRequest(BaseModel):
    session_id: Optional[str] = "default_session"
    code: str
    language: Optional[str] = "python"
    expected_output: str
    stdin: Optional[str] = ""

@router.get("/journeys")
def get_journeys():
    """Returns all learning journeys with embedded courses & lesson metadata."""
    return {"status": "success", "journeys": JOURNEYS_DATA}

@router.get("/journeys/{journey_id}")
def get_journey_by_id(journey_id: str):
    """Returns details for a specific journey."""
    journey = next((j for j in JOURNEYS_DATA if j["id"] == journey_id), None)
    if not journey:
        raise HTTPException(status_code=404, detail="Journey not found")
    return {"status": "success", "journey": journey}

@router.get("/problems")
def get_practice_problems():
    """Returns list of practice & DSA problems."""
    return {"status": "success", "problems": PRACTICE_PROBLEMS}

@router.get("/problems/{problem_id}")
def get_problem_by_id(problem_id: str):
    """Returns details for a specific practice problem."""
    problem = next((p for p in PRACTICE_PROBLEMS if p["id"] == problem_id), None)
    if not problem:
        raise HTTPException(status_code=404, detail="Problem not found")
    return {"status": "success", "problem": problem}

@router.post("/verify-solution")
async def verify_solution(req: VerifySolutionRequest):
    """
    Executes student code securely in sandbox and checks if stdout matches expected output.
    Supports stdin, timeout, stderr, and multiple programming languages.
    """
    lang = req.language or "python"
    result = sandbox_run_code(req.code, req.stdin or "", 3000, language=lang)
    actual_stdout = (result.get("stdout") or "").rstrip()
    expected = (req.expected_output or "").rstrip()
    
    passed = (actual_stdout == expected) and not result.get("stderr") and not result.get("timed_out")
    
    return {
        "status": "success",
        "passed": passed,
        "actual_output": result.get("stdout", ""),
        "expected_output": req.expected_output,
        "stderr": result.get("stderr", ""),
        "exit_code": 0 if not result.get("stderr") else 1,
        "timed_out": result.get("timed_out", False),
        "runtime_ms": result.get("runtime_ms", 0)
    }
