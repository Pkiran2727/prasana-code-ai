from datetime import datetime, timezone


def user_has_premium(profile: dict | None) -> bool:
    """plan 'free' కాకపోతే, expiry లేదా భవిష్యత్తులో ఉంటే premium. Admin అయితే unconditional premium."""
    if not profile:
        return False
    if profile.get("role") == "admin":
        return True
    if profile.get("plan", "free") == "free":
        return False
    exp = profile.get("plan_expires_at")
    return exp is None or exp > datetime.now(timezone.utc)


def get_profile(cur, user_id: str) -> dict | None:
    cur.execute("SELECT plan, plan_expires_at, total_xp, role FROM user_profiles WHERE id=%s", (user_id,))
    return cur.fetchone()


# Effective premium: lesson -> module -> course
EFFECTIVE_PREMIUM_SQL = "COALESCE(l.is_premium, m.is_premium, c.is_premium, FALSE)"
