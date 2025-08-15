# utils/security.py
import os
import time
import hmac
import base64
import json
from hashlib import sha256

# Simple JWT (HS256) helpers with graceful SECRET_KEY handling.
# If SECRET_KEY is missing, we generate a TEMP key (process-local) and log a warning.
# For production, always set SECRET_KEY in Railway Variables.

_SECRET_KEY = os.getenv("SECRET_KEY")
if not _SECRET_KEY:
    # 32 random bytes -> base64
    _SECRET_KEY = base64.urlsafe_b64encode(os.urandom(32)).decode("utf-8").rstrip("=")
    print("⚠️  SECRET_KEY no configurado. Se generó una clave temporal para esta ejecución.")
ALGO = "HS256"

def _b64url(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).decode("utf-8").rstrip("=")

def _b64url_json(obj) -> str:
    return _b64url(json.dumps(obj, separators=(",", ":"), ensure_ascii=False).encode("utf-8"))

def _sign(header_b64: str, payload_b64: str) -> str:
    msg = f"{header_b64}.{payload_b64}".encode("utf-8")
    sig = hmac.new(_SECRET_KEY.encode("utf-8"), msg, sha256).digest()
    return _b64url(sig)

def create_access_token(claims: dict, expires_minutes: int = 120) -> str:
    now = int(time.time())
    header = {"alg": ALGO, "typ": "JWT"}
    payload = dict(claims or {})
    payload.setdefault("iat", now)
    payload.setdefault("exp", now + expires_minutes * 60)
    if "sub" not in payload and "uid" in payload:
        payload["sub"] = payload["uid"]
    header_b64 = _b64url_json(header)
    payload_b64 = _b64url_json(payload)
    sig_b64 = _sign(header_b64, payload_b64)
    return f"{header_b64}.{payload_b64}.{sig_b64}"
