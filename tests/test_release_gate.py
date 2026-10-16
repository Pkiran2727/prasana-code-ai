"""
RELEASE GATE for Prasana Code AI  -  "100% correct" ki definition.

Run (from repo root, with a seeded Postgres):
    export DATABASE_URL=postgresql://user:pass@host:5432/prasana_code_ai
    pip install pytest
    pytest tests/test_release_gate.py -v

Rule: deploy cheyyadaniki ee file lo ALL tests PASS avvali (0 failed).
Each test asserts the SECURE / CORRECT behaviour. On the audited commit (8403a0a) most of these FAIL.
Tests that need a DB are skipped if DATABASE_URL is not set.
RELEASE RULE = TWO RUNS, both must show 0 failed:
  Run A (host / CI, repo root, has docker-compose.yml + frontend/):  pytest tests/test_release_gate.py -v
  Run B (inside backend container, real runtime user + filesystem): docker compose exec backend pytest tests/test_release_gate.py -v
      (needs pytest + tests/ in the image or mounted; repo-file tests are auto-skipped there)
Run A must have 0 skipped "repo files" tests; Run B is what proves sandbox/env/uid behaviour.
"""
import os, re, sys, glob, json, uuid, warnings, logging
import pytest

warnings.filterwarnings("ignore"); logging.disable(logging.CRITICAL)
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, ROOT)
SECRET = "RELEASE-GATE-SECRET-xyz"
os.environ["GATE_SECRET_TEST"] = SECRET
for k in ("SUPABASE_URL", "SUPABASE_KEY", "RAZORPAY_KEY_ID", "RAZORPAY_KEY_SECRET"):
    os.environ.pop(k, None)           # worst case: misconfigured production (env missing)

HAS_DB = bool(os.environ.get("DATABASE_URL"))
needs_db = pytest.mark.skipif(not HAS_DB, reason="DATABASE_URL not set")

REPO_FILES = os.path.exists(os.path.join(ROOT, "docker-compose.yml")) and os.path.isdir(os.path.join(ROOT, "frontend"))
needs_repo = pytest.mark.skipif(not REPO_FILES, reason="needs full repo checkout (run on host/CI from repo root)")

def read(path):
    p = os.path.join(ROOT, path)
    return open(p, encoding="utf-8", errors="ignore").read() if os.path.exists(p) else ""

@pytest.fixture(scope="module")
def client():
    from fastapi.testclient import TestClient
    from backend.main import app
    return TestClient(app, raise_server_exceptions=False)

FAKE = {"Authorization": "Bearer attacker-with-no-account"}

# ------------------------------------------------------------------ 1. AUTH (fail-closed)
class TestAuth:
    def test_login_wrong_password_gives_no_token(self, client):
        r = client.post("/auth/login", json={"email": "admin@example.com", "password": "wrong"})
        assert r.status_code >= 400 and "access_token" not in r.text

    def test_fake_bearer_cannot_reach_admin(self, client):
        assert client.get("/admin/metrics", headers=FAKE).status_code in (401, 403, 503)

    def test_fake_bearer_cannot_create_session(self, client):
        assert client.post("/session/create", headers=FAKE).status_code in (401, 403, 503)

    def test_fake_bearer_cannot_run_code(self, client):
        assert client.post("/run/00000000-0000-0000-0000-000000000000", headers=FAKE,
                           json={"path": "x.py"}).status_code in (401, 403, 404, 503)

    def test_no_shared_guest_identity_in_code(self):
        assert "00000000-0000-0000-0000-000000000001" not in read("backend/db.py") + read("backend/auth.py")

    def test_no_mock_token_bypass_in_code(self):
        assert "mock_token" not in read("backend/main.py") + read("backend/auth.py")

    @needs_repo
    def test_frontend_has_no_fake_login(self):
        src = read("frontend/src/components/auth/LoginScreen.jsx")
        assert "google_oauth_token" not in src and "123456" not in src

# ------------------------------------------------------------------ 2. SANDBOX
class TestSandbox:
    def test_student_code_cannot_read_server_env(self):
        from backend.progress_service import run_code
        r = run_code("import os\nprint(os.environ.get('GATE_SECRET_TEST'))", "", 3000, "python")
        assert SECRET not in r["stdout"]

    def test_student_code_not_root(self):
        from backend.progress_service import run_code
        r = run_code("import os\nprint(os.getuid())", "", 3000, "python")
        assert r["stdout"].strip() != "0"

    def test_student_code_cannot_read_dotenv_or_app_files(self):
        from backend.progress_service import run_code
        code = ("import glob\nprint(len(glob.glob('/app/.env*'))+len(glob.glob('/app/backend/*.py')))")
        assert run_code(code, "", 3000, "python")["stdout"].strip() in ("0", "")

    def test_infinite_loop_is_killed(self):
        from backend.progress_service import run_code
        r = run_code("while True: pass", "", 1000, "python")
        assert r["timed_out"] is True

    def test_memory_bomb_is_contained(self):
        from backend.progress_service import run_code
        r = run_code("x = bytearray(3 * 1024**3)\nprint('ALLOCATED')", "", 4000, "python")
        assert "ALLOCATED" not in r["stdout"]

    @needs_repo
    def test_dockerfile_does_not_bake_env_and_not_root(self):
        d = read("Dockerfile.backend")
        assert not re.search(r"COPY\s+\.env", d) and re.search(r"^\s*USER\s+(?!root)", d, re.M)

# ------------------------------------------------------------------ 3. FILES / PATH TRAVERSAL
class TestFiles:
    @pytest.mark.parametrize("evil", ["../../x.txt", "....//....//x.txt", "/etc/passwd", "a/../../x.txt",
                                      "..\\..\\x.txt", "%2e%2e/%2e%2e/x.txt", "..%2f..%2fx.txt"])
    def test_cannot_escape_session_dir(self, evil):
        from backend.session_manager import create_session, get_session_path
        from backend.file_manager import secure_resolve_path
        sid = create_session(user_id=str(uuid.uuid4()), email="t@example.com")
        base = os.path.realpath(get_session_path(sid))
        try:
            out = os.path.realpath(secure_resolve_path(sid, evil))
        except (PermissionError, ValueError):
            return
        assert os.path.commonpath([base, out]) == base

    def test_sibling_prefix_dir_not_allowed(self):
        from backend.session_manager import create_session, get_session_path
        from backend.file_manager import secure_resolve_path
        sid = create_session(user_id=str(uuid.uuid4()), email="t@example.com")
        base = get_session_path(sid)
        with pytest.raises((PermissionError, ValueError)):
            secure_resolve_path(sid, "../" + os.path.basename(base) + "-evil/x")

# ------------------------------------------------------------------ 4. DATABASE & NEW API
@needs_db
class TestDatabase:
    @pytest.fixture(scope="class")
    def cur(self):
        import psycopg2
        c = psycopg2.connect(os.environ["DATABASE_URL"]); cur = c.cursor(); yield cur; c.close()

    def test_user_profiles_has_plan_columns(self, cur):
        cur.execute("""select column_name from information_schema.columns where table_name='user_profiles'""")
        cols = {r[0] for r in cur.fetchall()}
        assert {"plan", "plan_expires_at", "total_xp"} <= cols, f"user_profiles columns: {cols}"

    def test_python_lessons_have_hidden_tests(self, cur):
        cur.execute("""select count(*) from lessons l join test_cases t on t.lesson_id=l.id
                       where l.slug like 'py-f-%' and t.is_hidden""")
        assert cur.fetchone()[0] >= 10

    def test_every_challenge_has_solution_code(self, cur):
        cur.execute("select count(*) from challenges where coalesce(solution_code,'')=''")
        assert cur.fetchone()[0] == 0

    def test_quiz_questions_seeded(self, cur):
        cur.execute("select count(*) from quiz_questions"); assert cur.fetchone()[0] >= 20

    def test_telugu_content_seeded(self, cur):
        cur.execute("select count(*) from lesson_content where lang='te'"); assert cur.fetchone()[0] >= 10

    def test_rls_enabled_on_all_public_tables(self, cur):
        """Supabase exposes public tables via its REST API (anon key). Without RLS, solution_code / hidden tests leak."""
        cur.execute("""select c.relname from pg_class c join pg_namespace n on n.oid=c.relnamespace
                       where n.nspname='public' and c.relkind='r' and not c.relrowsecurity""")
        missing = [r[0] for r in cur.fetchall()]
        assert not missing, f"RLS disabled on: {missing}"

    def test_catalog_metadata_matches_reality(self):
        from backend.curriculum_data import JOURNEYS_DATA as J
        bad = [(j["id"], j.get("totalLessons"), sum(len(c["lessons"]) for c in j["courses"]))
               for j in J if j.get("totalLessons") != sum(len(c["lessons"]) for c in j["courses"])]
        assert not bad, f"fake totalLessons: {bad}"

@needs_db
class TestApiFlow:
    @pytest.fixture(scope="class")
    def authed(self, client):
        """Authenticated test user via dependency override (adjust name if you rename the dependency)."""
        from backend.main import app
        from backend.db import get_current_user_id
        uid = str(uuid.uuid4())
        app.dependency_overrides[get_current_user_id] = lambda: uid
        yield client, uid
        app.dependency_overrides.pop(get_current_user_id, None)

    def _lesson_id(self, slug="py-f-m01-l01-print"):
        import psycopg2
        c = psycopg2.connect(os.environ["DATABASE_URL"]); cur = c.cursor()
        cur.execute("select id from lessons where slug=%s", (slug,)); row = cur.fetchone(); c.close()
        return str(row[0]) if row else None

    def test_course_outline_works(self, authed):
        client, _ = authed
        import psycopg2
        c = psycopg2.connect(os.environ["DATABASE_URL"]); cur = c.cursor()
        cur.execute("select slug from courses limit 1"); slug = cur.fetchone()[0]; c.close()
        assert client.get(f"/api/courses/{slug}").status_code == 200

    def test_me_progress_works(self, authed):
        assert authed[0].get("/api/me/progress").status_code == 200

    def test_lesson_never_leaks_solution_or_hidden(self, authed):
        r = authed[0].get(f"/api/lessons/{self._lesson_id()}")
        assert r.status_code == 200 and "solution_code" not in r.text and '"hidden": true' not in r.text.lower()

    def test_wrong_answer_does_not_complete(self, authed):
        client, _ = authed
        r = client.post(f"/api/lessons/{self._lesson_id()}/submit", json={"code": "print('nope')"})
        assert r.status_code == 200 and r.json()["passed"] is False

    def test_hardcoded_answer_fails_hidden_tests(self, authed):
        """Lesson with input must not be passable by hardcoding one visible answer."""
        import psycopg2
        c = psycopg2.connect(os.environ["DATABASE_URL"]); cur = c.cursor()
        cur.execute("""select l.id, t.expected_output from lessons l join test_cases t on t.lesson_id=l.id
                       where l.slug like 'py-f-%' and t.input_data<>'' limit 1""")
        row = cur.fetchone(); c.close()
        assert row, "no input-driven python lesson seeded"
        r = authed[0].post(f"/api/lessons/{row[0]}/submit", json={"code": f"print({row[1]!r})"})
        assert r.status_code == 200 and r.json()["passed"] is False

    def test_xp_awarded_once(self, authed):
        client, uid = authed
        import psycopg2
        c = psycopg2.connect(os.environ["DATABASE_URL"]); cur = c.cursor()
        cur.execute("select l.id, ch.solution_code from lessons l join challenges ch on ch.lesson_id=l.id "
                    "where l.slug='py-f-m01-l01-print'"); lid, sol = cur.fetchone(); c.close()
        a = client.post(f"/api/lessons/{lid}/submit", json={"code": sol}); b = client.post(f"/api/lessons/{lid}/submit", json={"code": sol})
        assert a.status_code == 200 and a.json()["xp_awarded"] > 0 and b.json()["xp_awarded"] == 0

    def test_run_endpoint_hides_hidden_test_data(self, authed):
        r = authed[0].post(f"/api/lessons/{self._lesson_id()}/run", json={"code": "print(1)"})
        assert r.status_code == 200 and all("expected" not in x for x in r.json()["results"] if x.get("hidden"))

# ------------------------------------------------------------------ 5. CHEAT ENDPOINTS
class TestCheating:
    def test_verify_solution_client_expected_removed(self, client):
        r = client.post("/api/verify-solution", json={"code": "print('x')", "expected_output": "x", "language": "python"})
        assert r.status_code in (401, 403, 404, 405, 410)

    def test_award_xp_endpoint_closed(self, client):
        r = client.post("/api/gamification/award-xp", json={"xp": 99999, "amount": 99999, "user_id": "x"})
        assert r.status_code in (401, 403, 404, 405, 410)

# ------------------------------------------------------------------ 6. PAYMENTS
class TestPayments:
    def test_mock_order_cannot_activate_plan(self, client):
        r = client.post("/api/payment/verify-payment", json={
            "razorpay_order_id": "order_mock_1", "razorpay_payment_id": "p", "razorpay_signature": "s",
            "user_email": "a@b.com", "plan_id": "lifetime"})
        assert r.status_code >= 400

    def test_client_cannot_choose_amount(self, client):
        r = client.post("/api/payment/create-order", headers=FAKE,
                        json={"plan_id": "lifetime", "amount": 1, "user_email": "a@b.com"})
        assert r.status_code >= 400 or r.json().get("amount") != 1

    @needs_repo
    def test_razorpay_in_requirements(self):
        assert "razorpay" in read("requirements.txt").lower()

    @needs_repo
    def test_no_hardcoded_default_razorpay_secret(self):
        assert "PrasanaSecret12345" not in read("backend/payment_routes.py") + read("docker-compose.yml") + read("backend/config.py")

    def test_constant_time_signature_compare(self):
        src = read("backend/payment_routes.py")
        assert "compare_digest" in src or "verify_payment_signature" in src

# ------------------------------------------------------------------ 7. SECRETS / INFRA
class TestInfra:
    @needs_repo
    def test_no_password_in_compose_or_seed_defaults(self):
        t = read("docker-compose.yml") + read("backend/seed_curriculum.py") + read(".env.example")
        assert "PrasanaSecureDBPassword2026" not in t

    @needs_repo
    def test_db_port_not_public(self):
        assert not re.search(r'^\s*-\s*"?5432:5432"?', read("docker-compose.yml"), re.M)

    def test_cors_not_wildcard(self, client):
        r = client.options("/api/journeys", headers={"Origin": "https://evil.example", "Access-Control-Request-Method": "GET"})
        assert r.headers.get("access-control-allow-origin") not in ("*", "https://evil.example")

    def test_no_personal_email_hardcoded(self):
        code = "".join(read(p) for p in ("backend/auth.py", "backend/main.py", "backend/config.py", "backend/payment_routes.py"))
        assert "mandaprasannakiran" not in code

    @needs_repo
    def test_dockerignore_excludes_env(self):
        assert re.search(r"^\.env", read(".dockerignore"), re.M)

    def test_docs_disabled_outside_development(self):
        assert "docs_url" in read("backend/main.py")

# ------------------------------------------------------------------ 7b. AI TUTOR (Mitra)
class TestTutor:
    def test_irrelevant_tools_removed(self):
        src = read("backend/agent.py")
        bad = [t for t in ("get_weather", "get_stock", "get_crypto", "read_url") if t in src]
        assert not bad, f"tutor still has tools: {bad}"

    def test_prompt_does_not_hand_out_full_solution(self):
        assert "unless they explicitly ask" not in read("backend/agent.py")

    def test_ai_quota_exists(self):
        code = "".join(open(f, encoding="utf-8", errors="ignore").read()
                       for f in glob.glob(os.path.join(ROOT, "backend", "*.py")))
        assert "ai_usage" in code, "no per-user AI quota (ai_usage) found"

# ------------------------------------------------------------------ 8. FRONTEND / BRAND
class TestFrontend:
    @needs_repo
    def test_no_localhost_in_frontend(self):
        hits = [f for f in glob.glob(os.path.join(ROOT, "frontend/src/**/*.js*"), recursive=True) if "localhost:8000" in open(f, encoding="utf-8").read()]
        assert not hits, hits

    @needs_repo
    def test_brand_uniform(self):
        files = [os.path.join(ROOT, "frontend/index.html")] + glob.glob(os.path.join(ROOT, "frontend/src/**/*.js*"), recursive=True)
        hits = [f for f in files if "LiveCodeAI" in open(f, encoding="utf-8").read()]
        assert not hits, hits

    @needs_repo
    def test_lesson_view_uses_server_grading(self):
        src = read("frontend/src/components/views/InteractiveLessonView.jsx")
        assert "/submit" in src and "/api/verify-solution" not in src

    @needs_repo
    def test_upi_qr_is_url_encoded(self):
        src = read("frontend/src/components/views/PricingView.jsx")
        assert "api.qrserver.com" not in src or "encodeURIComponent" in src

# ------------------------------------------------------------------ 9. CONTENT QUALITY
class TestContent:
    FILES = sorted(glob.glob(os.path.join(ROOT, "content/**/*.json"), recursive=True))

    def test_lessons_exist(self):
        assert len(self.FILES) >= 10

    @pytest.mark.parametrize("path", FILES, ids=lambda p: os.path.basename(p))
    def test_lesson_passes_strict_validator(self, path):
        sys.path.insert(0, os.path.dirname(__file__))      # tests/strict_validator.py (strict rules, ships with this gate)
        import importlib; v = importlib.import_module("strict_validator")
        assert v.validate(path) == []

    @pytest.mark.parametrize("path", FILES, ids=lambda p: os.path.basename(p))
    def test_no_dummy_padding_tests(self, path):
        d = json.load(open(path, encoding="utf-8")); t = d["challenge"]["tests"]
        stdins = [x["stdin"].strip() for x in t]; exps = {x["expected"] for x in t}
        padded = len(exps) == 1 and len(set(stdins)) > 1 and not d["challenge"].get("uses_stdin", False) \
                 and "input(" not in d["challenge"]["solution_code"]
        assert not padded, "tests differ in stdin but solution ignores input (fake tests)"
