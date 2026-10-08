from datetime import datetime, timezone


def user_has_premium(profile: dict | None) -> bool:
    """plan 'free' కాకపోతే, expiry లేదా భవిష్యత్తులో ఉంటే premium."""
    if not profile or profile.get("plan", "free") == "free":
        return False
    exp = profile.get("plan_expires_at")
    return exp is None or exp > datetime.now(timezone.utc)


def get_profile(cur, user_id: str) -> dict | None:
    # NOTE: user_profiles primary key column పేరు 'id' అని assume చేసాను; వేరే అయితే మార్చండి.
    cur.execute("SELECT plan, plan_expires_at, total_xp FROM user_profiles WHERE id=%s", (user_id,))
    return cur.fetchone()


# Effective premium: lesson -> module -> course
EFFECTIVE_PREMIUM_SQL = "COALESCE(l.is_premium, m.is_premium, c.is_premium, FALSE)"
