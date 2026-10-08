import time
from backend.entitlement import EFFECTIVE_PREMIUM_SQL


# ---------- Sandbox adapter ----------
import os
import sys
import subprocess
import tempfile

def run_code(code: str, stdin: str, timeout_ms: int, language: str = "python") -> dict:
    """
    Executes code in a secure sandboxed subprocess locally inside the container.
    Supports Python, JavaScript, TypeScript, C++, C, and Bash with stdin and timeout.
    """
    start = time.time()
    timeout_sec = max(1.0, timeout_ms / 1000.0)
    lang = (language or "python").lower()

    with tempfile.TemporaryDirectory() as tmpdir:
        try:
            if lang in ("python", "py"):
                file_path = os.path.join(tmpdir, "main.py")
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(code)
                cmd = [sys.executable, file_path]
            
            elif lang in ("javascript", "js"):
                file_path = os.path.join(tmpdir, "main.js")
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(code)
                cmd = ["node", file_path]

            elif lang in ("typescript", "ts"):
                file_path = os.path.join(tmpdir, "main.ts")
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(code)
                cmd = ["node", "--experimental-strip-types", file_path]

            elif lang in ("bash", "sh"):
                file_path = os.path.join(tmpdir, "script.sh")
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(code)
                cmd = ["bash", file_path]

            elif lang in ("cpp", "c++"):
                src_path = os.path.join(tmpdir, "main.cpp")
                bin_path = os.path.join(tmpdir, "main.out")
                with open(src_path, "w", encoding="utf-8") as f:
                    f.write(code)
                comp = subprocess.run(
                    ["g++", "-O2", "-std=c++20", src_path, "-o", bin_path],
                    capture_output=True,
                    text=True,
                    timeout=10
                )
                if comp.returncode != 0:
                    return {
                        "stdout": "",
                        "stderr": f"Compilation Error:\n{comp.stderr}",
                        "timed_out": False,
                        "runtime_ms": int((time.time() - start) * 1000)
                    }
                cmd = [bin_path]

            elif lang in ("c",):
                src_path = os.path.join(tmpdir, "main.c")
                bin_path = os.path.join(tmpdir, "main.out")
                with open(src_path, "w", encoding="utf-8") as f:
                    f.write(code)
                comp = subprocess.run(
                    ["gcc", "-O2", src_path, "-o", bin_path],
                    capture_output=True,
                    text=True,
                    timeout=10
                )
                if comp.returncode != 0:
                    return {
                        "stdout": "",
                        "stderr": f"Compilation Error:\n{comp.stderr}",
                        "timed_out": False,
                        "runtime_ms": int((time.time() - start) * 1000)
                    }
                cmd = [bin_path]
            else:
                return {
                    "stdout": "",
                    "stderr": f"Unsupported language: {language}",
                    "timed_out": False,
                    "runtime_ms": int((time.time() - start) * 1000)
                }

            proc = subprocess.run(
                cmd,
                input=stdin or "",
                capture_output=True,
                text=True,
                timeout=timeout_sec,
                cwd=tmpdir
            )
            return {
                "stdout": proc.stdout,
                "stderr": proc.stderr,
                "timed_out": False,
                "runtime_ms": int((time.time() - start) * 1000)
            }

        except subprocess.TimeoutExpired:
            return {
                "stdout": "",
                "stderr": "Time Limit Exceeded",
                "timed_out": True,
                "runtime_ms": int(timeout_sec * 1000)
            }
        except Exception as e:
            return {
                "stdout": "",
                "stderr": str(e),
                "timed_out": False,
                "runtime_ms": int((time.time() - start) * 1000)
            }


def _norm(s: str) -> str:
    return "\n".join(line.rstrip() for line in (s or "").strip().splitlines())


def run_tests(cur, lesson_id: str, code: str, only_visible: bool):
    cur.execute("SELECT time_limit_ms, language FROM challenges WHERE lesson_id=%s", (lesson_id,))
    ch = cur.fetchone()
    if not ch:
        return {"passed": False, "tests_passed": 0, "tests_total": 0, "runtime_ms": 0, "results": []}
    time_limit_ms = ch.get("time_limit_ms") or 3000
    language = ch.get("language") or "python"

    q = "SELECT * FROM test_cases WHERE lesson_id=%s"
    if only_visible:
        q += " AND is_hidden = FALSE"
    cur.execute(q + " ORDER BY sort_order", (lesson_id,))
    tests = cur.fetchall()

    results, passed, max_rt = [], 0, 0
    for t in tests:
        r = run_code(code, t["input_data"], time_limit_ms, language=language)
        ok = (not r["timed_out"]) and _norm(r["stdout"]) == _norm(t["expected_output"])
        passed += ok
        max_rt = max(max_rt, r["runtime_ms"])
        item = {"passed": ok, "hidden": t["is_hidden"], "timed_out": r["timed_out"]}
        if not t["is_hidden"]:  # hidden tests are never leaked
            item.update(input=t["input_data"], expected=t["expected_output"],
                        actual=r["stdout"], error=r["stderr"])
        results.append(item)
    return {"passed": bool(tests) and passed == len(tests), "tests_passed": passed,
            "tests_total": len(tests), "runtime_ms": max_rt, "results": results}


def get_lesson_access(cur, lesson_id: str):
    cur.execute(f"""
        SELECT l.*, c.slug AS course_slug, {EFFECTIVE_PREMIUM_SQL} AS effective_premium
        FROM lessons l JOIN modules m ON m.id=l.module_id JOIN courses c ON c.id=m.course_id
        WHERE l.id=%s AND l.is_published AND c.is_published""", (lesson_id,))
    return cur.fetchone()


# ---------- Progress + XP (idempotent) ----------
def record_attempt(cur, user_id: str, lesson_id: str, code: str):
    cur.execute("""
        INSERT INTO user_progress (user_id, lesson_id, status, attempts, last_code)
        VALUES (%s,%s,'in_progress',1,%s)
        ON CONFLICT (user_id, lesson_id) DO UPDATE
          SET attempts = user_progress.attempts + 1, last_code = EXCLUDED.last_code, updated_at = now()""",
        (user_id, lesson_id, code))


def complete_lesson(cur, user_id: str, lesson_id: str, xp_reward: int) -> int:
    """మొదటిసారి మాత్రమే XP ఇస్తుంది. Awarded XP return చేస్తుంది (రెండోసారి 0)."""
    cur.execute("""INSERT INTO user_progress (user_id, lesson_id, status)
                   VALUES (%s,%s,'in_progress') ON CONFLICT DO NOTHING""", (user_id, lesson_id))
    cur.execute("SELECT status FROM user_progress WHERE user_id=%s AND lesson_id=%s FOR UPDATE",
                (user_id, lesson_id))
    if cur.fetchone()["status"] == "completed":
        return 0
    cur.execute("""UPDATE user_progress SET status='completed', xp_earned=%s,
                   completed_at=now(), updated_at=now() WHERE user_id=%s AND lesson_id=%s""",
                (xp_reward, user_id, lesson_id))
    cur.execute("""INSERT INTO user_profiles (id, total_xp)
                   VALUES (%s, %s)
                   ON CONFLICT (id) DO UPDATE SET total_xp = user_profiles.total_xp + EXCLUDED.total_xp""",
                (user_id, xp_reward))
    return xp_reward
