from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from backend.db import get_cursor, get_current_user_id
from backend.entitlement import user_has_premium, get_profile, EFFECTIVE_PREMIUM_SQL
from backend import progress_service as ps

router = APIRouter(prefix="/api", tags=["curriculum"])


class CodeIn(BaseModel):
    code: str = Field(max_length=50_000)


def _accessible_lesson(cur, lesson_id: str, user_id: str):
    lesson = ps.get_lesson_access(cur, lesson_id)
    if not lesson:
        raise HTTPException(404, "Lesson not found")
    if lesson["effective_premium"] and not user_has_premium(get_profile(cur, user_id)):
        raise HTTPException(402, "Premium required")  # content ఎప్పుడూ పంపము
    return lesson


@router.get("/catalog")
def catalog(user_id: str = Depends(get_current_user_id)):
    with get_cursor() as cur:
        cur.execute("SELECT id, slug, title, description FROM categories ORDER BY sort_order")
        cats = cur.fetchall()
        cur.execute("""
            SELECT c.id, c.category_id, c.slug, c.title, c.description, c.difficulty, c.is_premium,
                   COUNT(l.id) AS total_lessons,
                   COUNT(up.lesson_id) FILTER (WHERE up.status='completed') AS completed_lessons
            FROM courses c
            LEFT JOIN modules m ON m.course_id=c.id
            LEFT JOIN lessons l ON l.module_id=m.id AND l.is_published
            LEFT JOIN user_progress up ON up.lesson_id=l.id AND up.user_id=%s
            WHERE c.is_published GROUP BY c.id ORDER BY c.sort_order""", (user_id,))
        courses = cur.fetchall()
    for c in cats:
        c["courses"] = []
    by_id = {c["id"]: c for c in cats}
    for co in courses:
        co["progress_pct"] = round(100 * co["completed_lessons"] / co["total_lessons"]) if co["total_lessons"] else 0
        by_id[co.pop("category_id")]["courses"].append(co)
    return {"categories": cats}


@router.get("/courses/{slug}")
def course_outline(slug: str, user_id: str = Depends(get_current_user_id)):
    with get_cursor() as cur:
        cur.execute("SELECT id, slug, title, description FROM courses WHERE slug=%s AND is_published", (slug,))
        course = cur.fetchone()
        if not course:
            raise HTTPException(404, "Course not found")
        premium = user_has_premium(get_profile(cur, user_id))
        cur.execute(f"""
            SELECT m.id AS module_id, m.title AS module_title,
                   l.id, l.slug, l.title, l.type, l.xp_reward,
                   {EFFECTIVE_PREMIUM_SQL} AS is_premium,
                   COALESCE(up.status,'not_started') AS status
            FROM modules m JOIN courses c ON c.id=m.course_id
            JOIN lessons l ON l.module_id=m.id AND l.is_published
            LEFT JOIN user_progress up ON up.lesson_id=l.id AND up.user_id=%s
            WHERE m.course_id=%s ORDER BY m.sort_order, l.sort_order""", (user_id, course["id"]))
        rows = cur.fetchall()
    modules = {}
    for r in rows:
        mod = modules.setdefault(r["module_id"], {"id": r["module_id"], "title": r["module_title"], "lessons": []})
        mod["lessons"].append({"id": r["id"], "slug": r["slug"], "title": r["title"], "type": r["type"],
                               "xp_reward": r["xp_reward"], "status": r["status"],
                               "is_premium": r["is_premium"], "locked": r["is_premium"] and not premium})
    course["modules"] = list(modules.values())
    return course


@router.get("/lessons/{lesson_id}")
def get_lesson(lesson_id: str, user_id: str = Depends(get_current_user_id)):
    with get_cursor() as cur:
        lesson = _accessible_lesson(cur, lesson_id, user_id)
        out = {k: lesson[k] for k in ("id", "title", "type", "content_md", "xp_reward", "course_slug")}
        cur.execute("SELECT status, last_code FROM user_progress WHERE user_id=%s AND lesson_id=%s",
                    (user_id, lesson_id))
        prog = cur.fetchone() or {"status": "not_started", "last_code": None}
        out["progress"] = prog
        if lesson["type"] == "challenge":
            cur.execute("""SELECT instructions_md, language, starter_code FROM challenges
                           WHERE lesson_id=%s""", (lesson_id,))  # solution_code ఎప్పుడూ select చేయము
            out["challenge"] = cur.fetchone()
            cur.execute("""SELECT input_data, expected_output FROM test_cases
                           WHERE lesson_id=%s AND NOT is_hidden ORDER BY sort_order""", (lesson_id,))
            out["visible_tests"] = cur.fetchall()
            cur.execute("SELECT COUNT(*) AS n FROM challenge_hints WHERE lesson_id=%s", (lesson_id,))
            out["hint_count"] = cur.fetchone()["n"]
        return out


@router.get("/lessons/{lesson_id}/hints/{level}")
def get_hint(lesson_id: str, level: int, user_id: str = Depends(get_current_user_id)):
    with get_cursor() as cur:
        _accessible_lesson(cur, lesson_id, user_id)
        cur.execute("SELECT level, content FROM challenge_hints WHERE lesson_id=%s AND level=%s",
                    (lesson_id, level))
        hint = cur.fetchone()
    if not hint:
        raise HTTPException(404, "No such hint")
    return hint


@router.post("/lessons/{lesson_id}/run")
def run(lesson_id: str, body: CodeIn, user_id: str = Depends(get_current_user_id)):
    with get_cursor() as cur:
        _accessible_lesson(cur, lesson_id, user_id)
        return ps.run_tests(cur, lesson_id, body.code, only_visible=True)


@router.post("/lessons/{lesson_id}/submit")
def submit(lesson_id: str, body: CodeIn, user_id: str = Depends(get_current_user_id)):
    with get_cursor() as cur:  # ఒకే transaction
        lesson = _accessible_lesson(cur, lesson_id, user_id)
        if lesson["type"] != "challenge":
            raise HTTPException(400, "Not a challenge")
        res = ps.run_tests(cur, lesson_id, body.code, only_visible=False)
        cur.execute("""INSERT INTO submissions (user_id, lesson_id, code, passed, tests_passed, tests_total, runtime_ms)
                       VALUES (%s,%s,%s,%s,%s,%s,%s)""",
                    (user_id, lesson_id, body.code, res["passed"], res["tests_passed"],
                     res["tests_total"], res["runtime_ms"]))
        ps.record_attempt(cur, user_id, lesson_id, body.code)
        res["xp_awarded"] = ps.complete_lesson(cur, user_id, lesson_id, lesson["xp_reward"]) if res["passed"] else 0
        return res


@router.post("/lessons/{lesson_id}/complete")
def complete_theory(lesson_id: str, user_id: str = Depends(get_current_user_id)):
    """Theory lesson (type='lesson') చదివాక mark complete."""
    with get_cursor() as cur:
        lesson = _accessible_lesson(cur, lesson_id, user_id)
        if lesson["type"] != "lesson":
            raise HTTPException(400, "Challenges are completed via /submit")
        return {"xp_awarded": ps.complete_lesson(cur, user_id, lesson_id, lesson["xp_reward"])}


@router.post("/lessons/{lesson_id}/save")
def save(lesson_id: str, body: CodeIn, user_id: str = Depends(get_current_user_id)):
    with get_cursor() as cur:
        _accessible_lesson(cur, lesson_id, user_id)
        cur.execute("""INSERT INTO user_progress (user_id, lesson_id, status, last_code)
                       VALUES (%s,%s,'in_progress',%s)
                       ON CONFLICT (user_id, lesson_id) DO UPDATE
                       SET last_code=EXCLUDED.last_code, updated_at=now()""", (user_id, lesson_id, body.code))
    return {"saved": True}


@router.get("/me/progress")
def my_progress(user_id: str = Depends(get_current_user_id)):
    with get_cursor() as cur:
        profile = get_profile(cur, user_id) or {}
        cur.execute("""SELECT COUNT(*) FILTER (WHERE status='completed') AS completed,
                              COUNT(*) FILTER (WHERE status='in_progress') AS in_progress
                       FROM user_progress WHERE user_id=%s""", (user_id,))
        counts = cur.fetchone()
    return {"total_xp": profile.get("total_xp", 0), **counts}


@router.get("/me/continue")
def continue_learning(user_id: str = Depends(get_current_user_id)):
    with get_cursor() as cur:
        cur.execute("""SELECT lesson_id AS id FROM user_progress
                       WHERE user_id=%s AND status='in_progress' ORDER BY updated_at DESC LIMIT 1""", (user_id,))
        row = cur.fetchone()
        if not row:  # ఏదీ ఆగలేదంటే తదుపరి పూర్తికాని lesson
            cur.execute("""
                SELECT l.id FROM lessons l JOIN modules m ON m.id=l.module_id JOIN courses c ON c.id=m.course_id
                LEFT JOIN user_progress up ON up.lesson_id=l.id AND up.user_id=%s
                WHERE l.is_published AND c.is_published AND COALESCE(up.status,'not_started')<>'completed'
                ORDER BY c.sort_order, m.sort_order, l.sort_order LIMIT 1""", (user_id,))
            row = cur.fetchone()
    return {"lesson_id": row["id"] if row else None}
