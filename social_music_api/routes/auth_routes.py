from fastapi import APIRouter
from models.usuario import UserCreate, UserLogin
from controllers.auth_controller import AuthController

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/registro", status_code=201)
async def registro(user: UserCreate):
    return await AuthController.register_user(user.dict())

@router.post("/login")
async def login(credentials: UserLogin):
    return await AuthController.login_user(credentials.dict())

# Aliases (compat)
alias_router = APIRouter(tags=["Auth (aliases)"])

@alias_router.post("/users", status_code=201)
async def users_alias(user: UserCreate):
    return await AuthController.register_user(user.dict())

@alias_router.post("/login")
async def login_alias(credentials: UserLogin):
    return await AuthController.login_user(credentials.dict())


@router.get("/debug/firebase")
async def debug_firebase():
    from utils.firebase import get_admin_project_id
    try:
        from utils.firebase_auth import get_project_id_safe
    except Exception:
        def get_project_id_safe(): return None
    return {"admin_project": get_admin_project_id(), "client_project": get_project_id_safe()}
