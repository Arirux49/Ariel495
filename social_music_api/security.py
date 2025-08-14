# utils/security.py
from datetime import datetime, timedelta
from typing import Dict, Any, Optional

from fastapi import HTTPException, Header
from jose import jwt, JWTError
from decouple import config

ALGORITHM = "HS256"

def create_access_token(payload: Dict[str, Any], minutes: int = 60 * 24 * 7) -> str:
    """
    Genera un JWT con exp válido (por defecto 7 días) y HS256.
    payload debe incluir al menos: { "sub": uid, "email": ..., "uid": ... }
    """
    secret = config("SECRET_KEY", default=None)
    if not secret:
        raise RuntimeError("SECRET_KEY no configurado")

    to_encode = payload.copy()
    expire = datetime.utcnow() + timedelta(minutes=minutes)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, secret, algorithm=ALGORITHM)

def decode_token(token: str) -> Dict[str, Any]:
    secret = config("SECRET_KEY", default=None)
    if not secret:
        raise RuntimeError("SECRET_KEY no configurado")
    try:
        return jwt.decode(token, secret, algorithms=[ALGORITHM])
    except JWTError as e:
        raise HTTPException(status_code=401, detail=f"Token inválido: {e}")

# Dependencia simple para rutas protegidas (si la usas)
def get_current_user(authorization: Optional[str] = Header(None)) -> Dict[str, Any]:
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="No autorizado")
    token = authorization.split(" ", 1)[1]
    return decode_token(token)
