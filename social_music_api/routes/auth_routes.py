
from fastapi import APIRouter, HTTPException, status
from utils.firebase import init_firebase, firebase_login
from utils.security import create_access_token
from utils.db import users_collection
from models.usuario import UserCreate, UserLogin
from firebase_admin import auth as fb_auth

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/registro", status_code=201)
async def registro(user: UserCreate):
    init_firebase()
    try:
        fb_user = fb_auth.create_user(email=user.email, password=user.password, display_name=user.nombre)
    except Exception as e:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, f"No se pudo crear usuario Firebase: {e}")
    if users_collection.find_one({"email": user.email}):
        raise HTTPException(400, "Email ya registrado")
    doc = {"nombre": user.nombre, "email": user.email, "firebase_uid": fb_user.uid, "perfil_artista": user.perfil_artista}
    res = users_collection.insert_one(doc)
    return {"_id": str(res.inserted_id), "nombre": user.nombre, "email": user.email}

@router.post("/login")
async def login(credentials: UserLogin):
    try:
        info = firebase_login(credentials.email, credentials.password)
    except Exception:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Credenciales inválidas")
    u = users_collection.find_one({"email": credentials.email})
    uid = str(u["_id"]) if u else info.get("localId")
    token = create_access_token({"sub": uid, "email": credentials.email, "uid": info.get("localId")})
    return {"access_token": token, "token_type": "bearer", "uid": info.get("localId")}

# Aliases requeridos por la rúbrica
alias_router = APIRouter(tags=["Auth (aliases)"])

@alias_router.post("/users", status_code=201)
async def users_alias(user: UserCreate):
    return await registro(user)

@alias_router.post("/login")
async def login_alias(credentials: UserLogin):
    return await login(credentials)
