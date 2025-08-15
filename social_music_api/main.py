# social_music_api/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes.api import api_router
from routes.instrumento_routes import router as instrumentos_router
from routes.sample_routes import router as samples_router
from routes.debug_routes import router as debug_router

from utils.db import ping_db
from utils.seed import seed_instruments

app = FastAPI(title="Social Music API - Full Clean")

# CORS sin credenciales para permitir "*" y evitar problemas de preflight
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Rutas en raíz
app.include_router(api_router)

# Rutas con prefijo /api (compatibilidad)
app.include_router(api_router, prefix="/api")
app.include_router(instrumentos_router, prefix="/api")
app.include_router(samples_router, prefix="/api")
app.include_router(debug_router, prefix="/api")

@app.on_event("startup")
async def startup():
    ok = await ping_db()
    if not ok:
        print("⚠️  No se pudo hacer ping a MongoDB (verifica MONGODB_URI / allowlist).")
    try:
        await seed_instruments()
    except Exception as e:
        print("Seed falló:", e)
