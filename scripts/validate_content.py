"""Usage: python scripts/validate_content.py content/python/py-foundations/**/*.json [--fill-expected]"""
import json, sys, glob
from backend.progress_service import run_code   # run_code(code, stdin, timeout_ms, language) -> dict

def norm(s: str) -> str:
    return "\n".join(l.rstrip() for l in (s or "").strip().splitlines())

def run(code, stdin, lang, limit):
    return run_code(code, stdin, limit, language=lang)

def validate(path, fill_expected=False):
    errs = []
    d = json.load(open(path, encoding="utf-8"))
    ch = d.get("challenge")
    if d["type"] != "challenge" or not ch:
        return errs                                    # (quiz/concept checks separate)

    lang, limit = ch["language"], ch.get("time_limit_ms", 3000)
    tests = ch["tests"]
    if len(tests) < 5: errs.append("need >= 5 tests")
    if sum(1 for t in tests if t["hidden"]) < 2: errs.append("need >= 2 hidden tests")
    if len(ch.get("hints", [])) != 3: errs.append("need exactly 3 hints")
    if len(ch.get("wrong_solutions", [])) < 2: errs.append("need >= 2 wrong_solutions")

    # 1) reference solution -> compute/verify expected, determinism
    for t in tests:
        r1 = run(ch["solution_code"], t["stdin"], lang, limit)
        r2 = run(ch["solution_code"], t["stdin"], lang, limit)
        if r1["timed_out"] or r1["stderr"]: errs.append(f"solution error on {t['stdin']!r}: {r1['stderr'][:100]}")
        if norm(r1["stdout"]) != norm(r2["stdout"]): errs.append(f"non-deterministic on {t['stdin']!r}")
        if r1["runtime_ms"] > 0.3 * limit: errs.append(f"solution too slow ({r1['runtime_ms']} ms)")
        if t.get("expected") is None:
            if fill_expected: t["expected"] = norm(r1["stdout"])
            else: errs.append("expected is null (run with --fill-expected)")
        elif norm(t["expected"]) != norm(r1["stdout"]):
            errs.append(f"expected mismatch on {t['stdin']!r}")

    if any(t.get("expected") is None for t in tests):
        return errs                                    # expected lekunda starter/wrong checks cheyyalemu

    # 2) starter must FAIL at least one test
    def passes_all(code):
        for t in tests:
            r = run(code, t["stdin"], lang, limit)
            if r["timed_out"] or norm(r["stdout"]) != norm(t["expected"] or ""):
                return False
        return True
    if passes_all(ch["starter_code"]): errs.append("starter_code already passes (pre-solved)")

    # 3) wrong solutions must FAIL
    for w in ch.get("wrong_solutions", []):
        if passes_all(w["code"]): errs.append(f"wrong solution '{w['label']}' passes (tests too weak)")

    if fill_expected and not errs:
        json.dump(d, open(path, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    return errs

if __name__ == "__main__":
    fill = "--fill-expected" in sys.argv
    files = [f for a in sys.argv[1:] if not a.startswith("--") for f in glob.glob(a, recursive=True)]
    bad = 0
    for f in files:
        e = validate(f, fill)
        print(("FAIL " if e else "OK   ") + f)
        for m in e: print("   -", m)
        bad += bool(e)
    sys.exit(1 if bad else 0)
