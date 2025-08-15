# utils/firebase_auth.py (lazy init)
import base64, json
from typing import Optional
from decouple import config

_project_id: Optional[str] = None
_auth = None

def _load_config():
    global _project_id
    if _project_id is not None:
        return _project_id

    api_key = config("FIREBASE_API_KEY", default=None)
    if not api_key:
        raise RuntimeError("FIREBASE_API_KEY no configurado")

    b64 = config("FIREBASE_CREDENTIALS_BASE64", default=None)
    if not b64:
        raise RuntimeError("FIREBASE_CREDENTIALS_BASE64 no configurado")

    raw = base64.b64decode(b64).decode("utf-8")
    data = json.loads(raw)
    _project_id = data["project_id"]
    return _project_id

def get_client_auth():
    global _auth
    if _auth is not None:
        return _auth
    pid = _load_config()
    api_key = config("FIREBASE_API_KEY")

    import pyrebase  # imported lazily
    firebase_config = {
        "apiKey": api_key,
        "authDomain": f"{pid}.firebaseapp.com",
        "databaseURL": f"https://{pid}.firebaseio.com",
        "projectId": pid,
        "storageBucket": f"{pid}.appspot.com",
    }
    firebase = pyrebase.initialize_app(firebase_config)
    _auth = firebase.auth()
    return _auth

def get_project_id_safe() -> str:
    try:
        return _load_config()
    except Exception:
        return "UNKNOWN"
