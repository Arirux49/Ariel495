from fastapi import APIRouter
from controllers.auth_controller import AuthController, UserRegister, UserLogin

router = APIRouter(prefix="/auth", tags=["Autenticación"])

@router.post("/registro", status_code=201)
async def register(user: UserRegister):
    return await AuthController.register_user(user.dict())

@router.post("/login")
async def login(user: UserLogin):
    return await AuthController.login_user(user.dict())
