from fastapi import APIRouter
from .auth_routes import router as auth_router
from .usuario_routes import router as usuario_router
from .instrumento_routes import router as instrumento_router
from .sample_routes import router as sample_router
from .grabacion_routes import router as grabacion_router
from .comentario_routes import router as comentario_router

api_router = APIRouter()
api_router.include_router(auth_router)
api_router.include_router(usuario_router)
api_router.include_router(instrumento_router)
api_router.include_router(sample_router)
api_router.include_router(grabacion_router)
api_router.include_router(comentario_router)

@api_router.get("/health", tags=["System"])
async def health_check():
    return {"status": "ok"}