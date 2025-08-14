# social_music_api/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes.api import api_router
# Routers nuevos (funcionales y para cumplir la rúbrica)
from routes.instrumento_routes import router as instrumentos_router
from routes.sample_routes import router as samples_router
from routes.debug_routes import router as debug_router  # /health, /whoami, etc.

from utils.db import ping_db
from utils.seed import seed_instruments

app = FastAPI(title="Social Music API - Full")

# CORS para permitir llamadas desde Vite/producción
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "*"  # si quieres restringir, pon aquí tu dominio de Railway/producción
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers existentes
app.include_router(api_router)

# Routers nuevos (sin prefijo)
app.include_router(instrumentos_router)
app.include_router(samples_router)
app.include_router(debug_router)

# Montar también bajo /api por compatibilidad con el front
app.include_router(instrumentos_router, prefix="/api")
app.include_router(samples_router, prefix="/api")
app.include_router(debug_router, prefix="/api")
app.include_router(api_router, prefix="/api")  # si tu router principal no estaba bajo /api

@app.on_event("startup")
def startup():
    ok = ping_db()
    if not ok:
        print("⚠️  No se pudo hacer ping a MongoDB (verifica MONGODB_URI).")
    seed_instruments()
