# utils/firebase_auth.py
import base64
import json
import pyrebase
from decouple import config

# Leer API key desde las variables de entorno
api_key = config("FIREBASE_API_KEY", default=None)
if not api_key:
    raise RuntimeError("Falta la variable FIREBASE_API_KEY")

# Leer credenciales en base64 y decodificar
b64 = config("FIREBASE_CREDENTIALS_BASE64", default=None)
if not b64:
    raise RuntimeError("Falta la variable FIREBASE_CREDENTIALS_BASE64")

try:
    raw_json = base64.b64decode(b64).decode("utf-8")
    service_account_info = json.loads(raw_json)
except Exception as e:
    raise RuntimeError(f"Credenciales Base64 inválidas: {e}")

# Usar el mismo projectId que el Admin SDK
project_id = service_account_info["project_id"]

firebase_config = {
    "apiKey": api_key,
    "authDomain": f"{project_id}.firebaseapp.com",
    "databaseURL": f"https://{project_id}.firebaseio.com",
    "projectId": project_id,
    "storageBucket": f"{project_id}.appspot.com",
    "messagingSenderId": service_account_info.get("client_id", ""),
    "appId": "",  # opcional
}

# Inicializar Pyrebase
firebase = pyrebase.initialize_app(firebase_config)
auth = firebase.auth()
