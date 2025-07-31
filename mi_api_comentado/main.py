# Importamos FastAPI, el framework principal para construir APIs web
from fastapi import FastAPI

# Importamos CORS middleware para permitir solicitudes de otros dominios (Cross-Origin Resource Sharing)
from fastapi.middleware.cors import CORSMiddleware

# Importamos el enrutador principal que agrupa todas las rutas del sistema
from routes.api import api_router

# Función que verifica la conexión con MongoDB
from utils.db import ping_db

# Uvicorn es el servidor ASGI que ejecuta la aplicación FastAPI
import uvicorn

# Instanciamos la aplicación FastAPI con parámetros personalizados
app = FastAPI(
    title="Social Music API",            # Título de la documentación
    description="API social para musicos",  # Descripción visible en Swagger
    version="1.0.0",                     # Versión de la API
    openapi_url="/openapi.json",        # Ruta del esquema OpenAPI
    docs_url="/docs",                   # Ruta de la documentación Swagger
    redoc_url="/redoc"                  # Ruta de la documentación ReDoc
)

# Middleware CORS: permite que otras aplicaciones (como un frontend) hagan peticiones a esta API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],     # Se permite cualquier origen. En producción es mejor restringir.
    allow_methods=["*"],     # Se permite cualquier método (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],     # Se permiten todos los encabezados HTTP
)

# Se incluyen todas las rutas definidas en el módulo `routes/api.py`
app.include_router(api_router)

# Evento que se ejecuta cuando la aplicación se inicia
@app.on_event("startup")
async def startup_event():
    # Verificamos si MongoDB está disponible
    if not ping_db():
        raise RuntimeError("Error al conectar con MongoDB")  # Lanzamos error si falla la conexión

# Ruta simple para verificar que el sistema está activo
@app.get("/health", tags=["System"])
async def health_check():
    return {
        "status": "active",                                    # Estado general
        "database": "MongoDB" if ping_db() else "offline",     # Verificación en tiempo real de MongoDB
        "services": ["Firebase Auth", "Firebase Storage"]      # Servicios externos en uso
    }

# Si se ejecuta directamente (python main.py), inicia el servidor Uvicorn
if __name__ == "__main__":
    uvicorn.run(
        "main:app",             # Ruta al objeto FastAPI (archivo:objeto)
        host="0.0.0.0",         # Escucha en todas las interfaces de red
        port=8000,              # Puerto en el que correrá la API
        reload=True,            # Recarga automática en desarrollo al detectar cambios
        log_level="debug"       # Nivel de logging detallado
    )
