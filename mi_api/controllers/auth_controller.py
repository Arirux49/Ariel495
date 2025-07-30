from fastapi import HTTPException
from utils.firebase import auth, verify_firebase_token
from utils.security import create_access_token
from utils.db import users_collection
from datetime import datetime
from pydantic import BaseModel, EmailStr
from typing import Optional


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
            firebase_user = auth.create_user_with_email_and_password(
                user_data["email"],
                user_data["password"]
            )

            user_db = {
                "firebase_uid": firebase_user["localId"],
                "email": user_data["email"],
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

        except Exception as e:
            error_message = str(e)
            if "EMAIL_EXISTS" in error_message:
                raise HTTPException(400, "El correo ya está registrado")
            raise HTTPException(400, f"Error en registro: {error_message}")

    @staticmethod
    async def login_user(credentials: dict) -> dict:
        try:
            firebase_user = auth.sign_in_with_email_and_password(
                credentials["email"],
                credentials["password"]
            )

            token = create_access_token(firebase_user["localId"])

            return {
                "access_token": token,
                "token_type": "bearer",
                "uid": firebase_user["localId"]
            }

        except Exception as e:
            error_message = str(e)
            if "INVALID_PASSWORD" in error_message or "EMAIL_NOT_FOUND" in error_message:
                raise HTTPException(401, "Correo o contraseña incorrectos")
            raise HTTPException(401, f"Error en autenticación: {error_message}")
