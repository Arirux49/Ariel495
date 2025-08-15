# utils/firebase_utils.py
import os
import base64
import json
import requests
import firebase_admin
from firebase_admin import credentials, auth as admin_auth

FIREBASE_PROJECT_ID = None

def init_firebase():
    """Initialize Firebase Admin using Base64 env or local file.
    Idempotent: safe to call multiple times.
    """
    global FIREBASE_PROJECT_ID
    if firebase_admin._apps:
        try:
            FIREBASE_PROJECT_ID = firebase_admin.get_app().project_id
        except Exception:
            pass
        return

    b64 = os.getenv("FIREBASE_CREDENTIALS_BASE64")
    cred_obj = None
    try:
        if b64:
            decoded = base64.b64decode(b64).decode("utf-8")
            info = json.loads(decoded)
            cred_obj = credentials.Certificate(info)
        else:
            # fallback to local file
            path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS", "secrets/firebase-secret.json")
            cred_obj = credentials.Certificate(path)
        app = firebase_admin.initialize_app(cred_obj)
        try:
            FIREBASE_PROJECT_ID = app.project_id
        except Exception:
            FIREBASE_PROJECT_ID = None
    except Exception as e:
        print(f"⚠️  No se pudo inicializar Firebase Admin: {e}")
        FIREBASE_PROJECT_ID = None

def sign_in_with_password(email: str, password: str) -> dict:
    """Sign in using Firebase Identity Toolkit REST API (requires FIREBASE_API_KEY)."""
    api_key = os.getenv("FIREBASE_API_KEY")
    if not api_key:
        raise RuntimeError("FIREBASE_API_KEY no configurado")
    url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={api_key}"
    data = {"email": email, "password": password, "returnSecureToken": True}
    r = requests.post(url, json=data, timeout=15)
    if r.status_code != 200:
        try:
            err = r.json()
        except Exception:
            err = {"error": {"message": r.text}}
        raise RuntimeError(f"Firebase login error: {err}")
    return r.json()

def debug_firebase():
    """Return a dict with debug info about Firebase config presence."""
    api_key = os.getenv("FIREBASE_API_KEY")
    has_b64 = bool(os.getenv("FIREBASE_CREDENTIALS_BASE64"))
    creds_source = "base64_env" if has_b64 else ("file" if os.path.exists("secrets/firebase-secret.json") else "none")
    info = {
        "admin_project": FIREBASE_PROJECT_ID,
        "has_api_key": bool(api_key),
        "credentials_source": creds_source,
        "api_key_masked": (api_key[:6] + "..." + api_key[-4:]) if api_key else None,
    }
    return info
