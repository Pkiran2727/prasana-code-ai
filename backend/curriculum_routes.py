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

class VerifySolutionRequest(BaseModel):
    session_id: str
    code: str
    language: str
    expected_output: str

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
    Executes student code and checks if stdout matches the expected test output.
    """
    from backend.file_manager import write_file
    
    # Save student code to temp file in session workspace
    filename = "main.py" if req.language == "python" else "solution.js"
    write_file(req.session_id, filename, req.code)
    
    # Run code
    result = await run_code(req.session_id, filename)
    actual_stdout = result.get("stdout", "")
    
    passed = actual_stdout.strip() == req.expected_output.strip()
    
    return {
        "status": "success",
        "passed": passed,
        "actual_output": actual_stdout,
        "expected_output": req.expected_output,
        "stderr": result.get("stderr", ""),
        "exit_code": result.get("exit_code", 0)
    }
