"""
Gamification & Leaderboard State for Prasana Code AI
Tracks XP, Streaks, Achievements, and Certificates.
"""

from pydantic import BaseModel
from typing import List, Dict

MOCK_LEADERBOARD = [
    {"rank": 1, "name": "Prasana", "xp": 1450, "streak": 14, "badge": "Master 🔥"},
    {"rank": 2, "name": "Alex Dev", "xp": 1200, "streak": 9, "badge": "Python Pro 🐍"},
    {"rank": 3, "name": "Sofia Coder", "xp": 980, "streak": 7, "badge": "Web Dev 🌐"},
    {"rank": 4, "name": "Rahul Tech", "xp": 750, "streak": 5, "badge": "DSA Solver ⚡"},
    {"rank": 5, "name": "Elena AI", "xp": 620, "streak": 4, "badge": "Prompt Eng 🤖"}
]

USER_STATS = {
    "xp": 350,
    "streak": 3,
    "completed_lessons": ["py-l1"],
    "completed_problems": ["prob-1"],
    "badges": [
        {"id": "b1", "name": "First Code", "icon": "🚀", "desc": "Wrote your first line of code"},
        {"id": "b2", "name": "3-Day Streak", "icon": "🔥", "desc": "Coded for 3 consecutive days"}
    ]
}

CERTIFICATES = [
    {
        "id": "cert-py-101",
        "title": "Python Developer Certification",
        "issued_to": "Prasana",
        "date": "2026-10-07",
        "verify_id": "PCAI-PY-2026-9876",
        "course_name": "Python Essentials & Data Types"
    }
]
