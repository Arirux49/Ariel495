# Importamos el componente APIRouter de FastAPI, que permite agrupar rutas
from fastapi import APIRouter

# Importamos los routers definidos en cada uno de los módulos de rutas
from .auth_routes import router as auth_router                  # Rutas de autenticación
from .usuario_routes import router as usuario_router            # Rutas relacionadas con usuarios
from .instrumento_routes import router as instrumento_router    # Rutas relacionadas con instrumentos
from .sample_routes import router as sample_router              # Rutas para samples de audio
from .grabacion_routes import router as grabacion_router        # Rutas para grabaciones
from .comentario_routes import router as comentario_router      # Rutas para comentarios

# Se crea una instancia principal de APIRouter, que consolidará todas las rutas anteriores
api_router = APIRouter()

# Se integran todos los subrouters a la instancia principal del router
api_router.include_router(auth_router)          # Incluye las rutas de autenticación
api_router.include_router(usuario_router)       # Incluye las rutas de usuarios
api_router.include_router(instrumento_router)   # Incluye las rutas de instrumentos
api_router.include_router(sample_router)        # Incluye las rutas de samples
api_router.include_router(grabacion_router)     # Incluye las rutas de grabaciones
api_router.include_router(comentario_router)    # Incluye las rutas de comentarios

# Ruta de verificación del estado del sistema
@api_router.get("/health", tags=["System"])
async def health_check():
    """
    Endpoint de salud del sistema. Se puede usar para verificar
    si la API está activa y responde correctamente.
    """
    return {"status": "ok"}  # Devuelve una respuesta simple indicando que el sistema está operativo
