from fastapi import HTTPException
from utils.firebase import init_firebase, get_admin_project_id
from firebase_admin import auth as admin_auth
from utils.security import create_access_token
from utils.db import users_collection
from datetime import datetime
from pydantic import BaseModel, EmailStr
from typing import Optional
from utils.firebase_auth import get_client_auth, get_project_id_safe

class UserRegister(BaseModel):
    email: EmailStr
    password: str
    nombre: str
    perfil_artista: Optional[str] = ""

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class AuthController:
    @staticmethod
    async def register_user(user_data: dict) -> dict:
        import requests
        from decouple import config
        from firebase_admin import auth as admin_auth  # para ver si ya existe, si hay Admin listo
        try:
            email = user_data["email"]

            # 0) Si tenemos Admin inicializado, verificar si existe (mejor mensaje)
            try:
                init_firebase()
                try:
                    admin_auth.get_user_by_email(email)
                    raise HTTPException(400, "El correo ya está registrado")
                except admin_auth.UserNotFoundError:
                    pass
            except Exception:
                # Si Admin no está bien configurado, seguimos sin romper
                pass

            # 1) Crear en Firebase Auth con REST /accounts:signUp (solo API key, evita invalid_grant)
            api_key = config("FIREBASE_API_KEY", default=None)
            if not api_key:
                raise HTTPException(500, "Falta FIREBASE_API_KEY")

            url = f"https://identitytoolkit.googleapis.com/v1/accounts:signUp?key={api_key}"
            payload = {"email": email, "password": user_data["password"], "returnSecureToken": True}
            resp = requests.post(url, json=payload, timeout=15)

            if resp.status_code != 200:
                try:
                    err = resp.json().get("error", {}).get("message", "")
                except Exception:
                    err = ""
                if "EMAIL_EXISTS" in err:
                    raise HTTPException(400, "El correo ya está registrado")
                raise HTTPException(400, f"Error en registro Firebase: {err or 'desconocido'}")

            data = resp.json()  # contiene localId
            local_id = data.get("localId")
            if not local_id:
                raise HTTPException(400, "Registro incompleto: falta localId")

            # 2) Guardar en Mongo (evitar duplicado por carrera)
            if users_collection.find_one({"email": email}):
                raise HTTPException(400, "El correo ya está registrado")
            user_db = {
                "firebase_uid": local_id,
                "email": email,
                "nombre": user_data["nombre"],
                "perfil_artista": user_data.get("perfil_artista", ""),
                "fecha_registro": datetime.utcnow(),
            }
            res = users_collection.insert_one(user_db)
            return {
                "id": str(res.inserted_id),
                "firebase_uid": user_db["firebase_uid"],
                "email": user_db["email"],
                "nombre": user_db["nombre"],
                "perfil_artista": user_db["perfil_artista"],
                "fecha_registro": user_db["fecha_registro"].isoformat(),
            }

        except HTTPException:
            raise
        except Exception as e:
            msg = str(e)
            if "EMAIL_EXISTS" in msg:
                raise HTTPException(400, "El correo ya está registrado")
            raise HTTPException(400, f"Error en registro: {msg}")


    @staticmethod
    async def login_user(credentials: dict) -> dict:
        """Login con Pyrebase y emisión de JWT propio."""
        try:
            fb_user = get_client_auth().sign_in_with_email_and_password(
                credentials["email"], credentials["password"]
            )
            uid = fb_user["localId"]
            token = create_access_token({"sub": uid, "email": credentials["email"], "uid": uid})
            return {"access_token": token, "token_type": "bearer", "uid": uid}
        except Exception as e:
            msg = str(e)
            if "INVALID_PASSWORD" in msg or "EMAIL_NOT_FOUND" in msg:
                raise HTTPException(401, "Correo o contraseña incorrectos")
            raise HTTPException(401, f"Error en autenticación: {msg}")
