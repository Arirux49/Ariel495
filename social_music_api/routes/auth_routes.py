# routes/auth_routes.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr
from controllers.auth_controller import AuthController

router = APIRouter(tags=["Auth"])

class SignupIn(BaseModel):
    email: EmailStr
    password: str
    firstname: str
    lastname: str

class LoginIn(BaseModel):
    email: EmailStr
    password: str

@router.post("/signup")
async def signup(body: SignupIn):
    try:
        data = {
            "email": body.email.strip().lower(),
            "password": body.password,
            "firstname": body.firstname,
            "lastname": body.lastname,
        }
        res = await AuthController.register_user(data)
        return {"ok": True, **res}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(400, f"No se pudo registrar: {e}")

@router.post("/login")
async def login(body: LoginIn):
    try:
        data = {"email": body.email.strip().lower(), "password": body.password}
        res = await AuthController.login_user(data)
        token = res.get("access_token") or res.get("token") or res.get("id_token")
        if not token:
            raise HTTPException(500, "El servidor no generó token")
        return {"access_token": token, "token_type": "bearer"}
    except HTTPException:
        raise
    except RuntimeError as e:
        raise HTTPException(500, f"Config incompleta: {e}")
    except Exception as e:
        raise HTTPException(401, f"Credenciales inválidas o error: {e}")
