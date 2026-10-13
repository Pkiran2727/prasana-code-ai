"""Usage: python scripts/validate_content.py "content/**/*.json" [--fill-expected]
Runs from the repo root (so `backend.progress_service` imports). If that import fails, a simple
local runner (python only, NOT sandboxed) is used - fine for authoring on your own machine."""
import json, sys, glob, re, subprocess, time

try:
    from backend.progress_service import run_code      # run_code(code, stdin, timeout_ms, language) -> dict
except Exception:                                      # local fallback (python only)
    def run_code(code, stdin, timeout_ms, language="python"):
        s = time.time()
        try:
            p = subprocess.run([sys.executable, "-c", code], input=stdin, capture_output=True,
                               text=True, timeout=timeout_ms / 1000)
            return {"stdout": p.stdout, "stderr": p.stderr, "timed_out": False,
                    "runtime_ms": int((time.time() - s) * 1000)}
        except subprocess.TimeoutExpired:
            return {"stdout": "", "stderr": "TLE", "timed_out": True, "runtime_ms": timeout_ms}

def norm(s):
    return "\n".join(l.rstrip() for l in (s or "").strip().splitlines())

def words_outside_code(md):
    md = re.sub(r"```.*?```", " ", md, flags=re.S)                    # fenced code
    md = "\n".join(l for l in md.splitlines() if not l.strip().startswith("|"))   # tables
    return len(re.findall(r"[A-Za-z0-9'`\-\.]+", md))

def validate(path, fill_expected=False):
    errs = []
    d = json.load(open(path, encoding="utf-8"))
    ch = d.get("challenge")
    if d["type"] != "challenge" or not ch:
        return errs
    lang, limit = ch["language"], ch.get("time_limit_ms", 3000)
    tests, fixed = ch["tests"], ch.get("fixed_output", False)

    # --- structure -------------------------------------------------------------------
    if "te" not in d["content"]: errs.append("missing Telugu content")
    wc = words_outside_code(d["content"]["en"]["body_md"])
    if not 150 <= wc <= 200: errs.append(f"concept text {wc} words (want 150-200)")
    if len(ch.get("hints", [])) != 3: errs.append("need exactly 3 hints")
    if len(ch.get("hints_te", [])) != 3: errs.append("need exactly 3 Telugu hints")
    for h in ch.get("hints", []):
        if len(h.split()) > 40: errs.append(f"hint longer than 40 words: {h[:30]}...")
    if len(ch.get("wrong_solutions", [])) < 2: errs.append("need >= 2 wrong_solutions")
    if len(d.get("quiz", [])) < 2: errs.append("need >= 2 quiz questions")
    if fixed:
        if len(tests) < 1: errs.append("need >= 1 test")
    else:
        if len(tests) < 5: errs.append("need >= 5 tests")
        if sum(1 for t in tests if t["hidden"]) < 2: errs.append("need >= 2 hidden tests")

    # --- reference solution: expected / determinism / speed ---------------------------
    for t in tests:
        r1 = run_code(ch["solution_code"], t["stdin"], limit, language=lang)
        r2 = run_code(ch["solution_code"], t["stdin"], limit, language=lang)
        if r1["timed_out"] or r1["stderr"]: errs.append(f"solution error on {t['stdin']!r}: {r1['stderr'][:100]}")
        if norm(r1["stdout"]) != norm(r2["stdout"]): errs.append(f"non-deterministic on {t['stdin']!r}")
        if r1["runtime_ms"] > 0.3 * limit: errs.append(f"solution too slow ({r1['runtime_ms']} ms)")
        if t.get("expected") is None:
            if fill_expected: t["expected"] = norm(r1["stdout"])
            else: errs.append("expected is null (run with --fill-expected)")
        elif norm(t["expected"]) != norm(r1["stdout"]):
            errs.append(f"expected mismatch on {t['stdin']!r}")

    # --- quiz checks ----------------------------------------------------------------
    for i, q in enumerate(d.get("quiz", [])):
        if q["qtype"] == "predict_output":
            if "code" not in q:
                errs.append(f"quiz[{i}] predict_output has no `code` field (answer cannot be verified)")
                continue
            r = run_code(q["code"], q.get("stdin", ""), 3000, language=lang)
            if norm(r["stdout"]) != norm(q["answer"]):
                errs.append(f"quiz[{i}] answer {q['answer']!r} != actual {norm(r['stdout'])!r}")
        elif q["qtype"] in ("mcq_single", "mcq_multi"):
            ids = {o["id"] for o in q["options"]}
            if not set(q["answer"]) <= ids: errs.append(f"quiz[{i}] answer id not in options")
            if q["qtype"] == "mcq_single" and len(q["answer"]) != 1: errs.append(f"quiz[{i}] needs exactly 1 answer")

    if any(t.get("expected") is None for t in tests):
        return errs

    # --- starter must fail; wrong solutions must fail --------------------------------
    def passes_all(code):
        for t in tests:
            r = run_code(code, t["stdin"], limit, language=lang)
            if r["timed_out"] or norm(r["stdout"]) != norm(t["expected"]):
                return False
        return True
    if passes_all(ch["starter_code"]): errs.append("starter_code already passes (pre-solved)")
    for w in ch["wrong_solutions"]:
        if passes_all(w["code"]): errs.append(f"wrong solution '{w['label']}' passes (tests too weak)")
    if passes_all(ch["solution_code"]) is False: errs.append("solution does not pass its own tests")

    if fill_expected and not errs:
        json.dump(d, open(path, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    return errs

if __name__ == "__main__":
    fill = "--fill-expected" in sys.argv
    files = sorted(f for a in sys.argv[1:] if not a.startswith("--") for f in glob.glob(a, recursive=True))
    bad = 0
    for f in files:
        e = validate(f, fill)
        print(("FAIL " if e else "OK   ") + f.split("/")[-1])
        for m in e: print("   -", m)
        bad += bool(e)
    print(f"\n{len(files)-bad}/{len(files)} lessons OK")
    sys.exit(1 if bad else 0)
