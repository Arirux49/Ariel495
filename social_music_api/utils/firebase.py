
import firebase_admin
from firebase_admin import credentials, auth
from decouple import config
import requests
from pathlib import Path

def init_firebase():
    cred_path = Path("secrets/firebase_credentials.json")
    if firebase_admin._apps:
        return
    if not cred_path.exists():
        raise RuntimeError("Falta secrets/firebase_credentials.json")
    cred = credentials.Certificate(str(cred_path))
    firebase_admin.initialize_app(cred)

def firebase_login(email: str, password: str) -> dict:
    api_key = config("FIREBASE_API_KEY")
    url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={api_key}"
    resp = requests.post(url, json={"email": email, "password": password, "returnSecureToken": True})
    if resp.status_code != 200:
        raise ValueError("Credenciales inválidas")
    return resp.json()
