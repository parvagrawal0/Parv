import os

import requests


def supabase_is_configured() -> bool:
    url = os.environ.get("SUPABASE_URL", "").strip()
    key = os.environ.get("SUPABASE_SERVICE_ROLE_KEY", "").strip()
    return bool(url and key)


def _get_supabase_rest_config() -> tuple[str, str]:
    url = os.environ.get("SUPABASE_URL", "").strip().rstrip("/")
    key = os.environ.get("SUPABASE_SERVICE_ROLE_KEY", "").strip()

    if not url or not key:
        raise RuntimeError(
            "Supabase env vars missing. Set SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY."
        )

    return url, key


def insert_user_to_supabase(user: dict) -> None:
    """
    Insert a user row into Supabase Postgres via PostgREST.
    Requires SUPABASE_SERVICE_ROLE_KEY for reliable server-side inserts.
    """
    url, key = _get_supabase_rest_config()
    endpoint = f"{url}/rest/v1/users"

    headers = {
        "apikey": key,
        "Authorization": f"Bearer {key}",
        "Content-Type": "application/json",
        "Prefer": "return=minimal",
    }

    resp = requests.post(endpoint, json=user, headers=headers, timeout=15)
    if resp.status_code not in (200, 201, 204):
        # Surface Supabase error message for debugging
        raise RuntimeError(f"Supabase insert failed ({resp.status_code}): {resp.text}")

