# utils/firebase.py
import os
import json
import base64
from pathlib import Path

import firebase_admin
from firebase_admin import credentials
from decouple import config
import requests


def init_firebase():
    """
    Inicializa Firebase Admin usando:
    1) FIREBASE_CREDENTIALS_BASE64 (JSON de la cuenta de servicio en base64), o
    2) secrets/firebase_credentials.json (fallback local).
    """
    if firebase_admin._apps:
        return

    b64 = None
    try:
        
        b64 = config("FIREBASE_CREDENTIALS_BASE64", default=None)
    except Exception:
        b64 = None

    cred = None
    if b64:
        try:
            raw = base64.b64decode(b64).decode("utf-8")
            data = json.loads(raw)  
            cred = credentials.Certificate(data)
        except Exception as e:
            raise RuntimeError(f"FIREBASE_CREDENTIALS_BASE64 inválido: {e}")

    if cred is None:
        cred_path = Path("secrets/firebase_credentials.json")
        if not cred_path.exists():
            raise RuntimeError(
                "Falta secrets/firebase_credentials.json o la variable FIREBASE_CREDENTIALS_BASE64"
            )
        cred = credentials.Certificate(str(cred_path))

    firebase_admin.initialize_app(cred)


def firebase_login(email: str, password: str) -> dict:

    api_key = config("FIREBASE_API_KEY")
    url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={api_key}"
    resp = requests.post(
        url,
        json={"email": email, "password": password, "returnSecureToken": True},
        timeout=15,
    )
    if resp.status_code != 200:
        try:
            err = resp.json().get("error", {}).get("message", "Credenciales inválidas")
        except Exception:
            err = "Credenciales inválidas"
        raise ValueError(err)
    return resp.json()


def get_admin_project_id() -> str:
    """Devuelve el projectId que está usando el Admin SDK, para diagnóstico."""
    import firebase_admin
    try:
        app = firebase_admin.get_app()
        pid = getattr(app, "project_id", None)
        return pid or app.options.get("projectId") or "UNKNOWN"
    except Exception:
        return "UNKNOWN"
