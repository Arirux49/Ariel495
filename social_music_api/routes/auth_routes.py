# routes/auth_routes.py
from fastapi import APIRouter
from models.usuario import UserCreate, UserLogin
from controllers.auth_controller import AuthController

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/registro", status_code=201)
async def registro(user: UserCreate):
    # Delegamos al controlador para un flujo único y consistente
    return await AuthController.register_user(user.dict())

@router.post("/login")
async def login(credentials: UserLogin):
    return await AuthController.login_user(credentials.dict())

# Aliases requeridos por la rúbrica
alias_router = APIRouter(tags=["Auth (aliases)"])

@alias_router.post("/users", status_code=201)
async def users_alias(user: UserCreate):
    return await AuthController.register_user(user.dict())

@alias_router.post("/login")
async def login_alias(credentials: UserLogin):
    return await AuthController.login_user(credentials.dict())
