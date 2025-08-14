# controllers/auth_controller.py
from fastapi import HTTPException
from utils.firebase import init_firebase, get_admin_project_id
from firebase_admin import auth as admin_auth
from utils.security import create_access_token
from utils.db import users_collection
from datetime import datetime
from pydantic import BaseModel, EmailStr
from typing import Optional

# Cliente Pyrebase unificado con el mismo proyecto del Admin SDK
from utils.firebase_auth import auth as client_auth, PROJECT_ID as CLIENT_PROJECT_ID


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
        try:
            init_firebase()
            admin_pid = get_admin_project_id()
            email = user_data.get("email")

            # Diagnóstico opcional (se verá en logs de Railway)
            print(f"[REGISTER] email={email} admin_project={admin_pid} pyrebase_project={CLIENT_PROJECT_ID}")

            # 1) Verificar en Admin SDK si ya existe
            try:
                admin_auth.get_user_by_email(email)
                print(f"[REGISTER] email ya existe en Admin SDK: {email}")
                raise HTTPException(400, "El correo ya está registrado")
            except admin_auth.UserNotFoundError:
                pass  # no existe → seguimos

            # 2) Crear en Firebase (Pyrebase, mismo projectId)
            firebase_user = client_auth.create_user_with_email_and_password(
                email,
                user_data["password"]
            )

            # 3) Guardar en Mongo (evitar duplicados por carrera)
            if users_collection.find_one({"email": email}):
                raise HTTPException(400, "El correo ya está registrado")

            user_db = {
                "firebase_uid": firebase_user["localId"],
                "email": email,
                "nombre": user_data["nombre"],
                "perfil_artista": user_data.get("perfil_artista", ""),
                "fecha_registro": datetime.utcnow()
            }
            result = users_collection.insert_one(user_db)

            return {
                "id": str(result.inserted_id),
                "firebase_uid": user_db["firebase_uid"],
                "email": user_db["email"],
                "nombre": user_db["nombre"],
                "perfil_artista": user_db["perfil_artista"],
                "fecha_registro": user_db["fecha_registro"].isoformat()
            }

        except HTTPException:
            raise
        except Exception as e:
            msg = str(e)
            print(f"[REGISTER][ERROR] email={user_data.get('email')} err={msg}")
            if "EMAIL_EXISTS" in msg:
                raise HTTPException(400, "El correo ya está registrado")
            raise HTTPException(400, f"Error en registro: {msg}")

    @staticmethod
    async def login_user(credentials: dict) -> dict:
        try:
            firebase_user = client_auth.sign_in_with_email_and_password(
                credentials["email"],
                credentials["password"]
            )
            uid = firebase_user["localId"]
            token = create_access_token({"sub": uid, "email": credentials["email"], "uid": uid})
            return {
                "access_token": token,
                "token_type": "bearer",
                "uid": uid
            }
        except Exception as e:
            msg = str(e)
            if "INVALID_PASSWORD" in msg or "EMAIL_NOT_FOUND" in msg:
                raise HTTPException(401, "Correo o contraseña incorrectos")
            raise HTTPException(401, f"Error en autenticación: {msg}")
