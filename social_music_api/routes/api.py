from fastapi import APIRouter
from .instrumento_routes import router as instrumentos_router
from .sample_routes import router as samples_router
from .debug_routes import router as debug_router

api_router = APIRouter()
api_router.include_router(instrumentos_router)
api_router.include_router(samples_router)
api_router.include_router(debug_router)
