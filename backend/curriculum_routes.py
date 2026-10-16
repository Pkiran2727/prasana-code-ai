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
