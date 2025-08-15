# social_music_api/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.proxy_headers import ProxyHeadersMiddleware

from routes.api import api_router              # /instrumentos y /samples
from routes.auth_routes import router as auth_router

# (opcionales)
try:
    from routes.tipo_routes import router as tipo_router
    from routes.modelo_routes import router as modelo_router
except Exception:
    tipo_router = None
    modelo_router = None

from utils.db import ping_db
from utils.seed import seed_instruments

app = FastAPI(title="Social Music API - Full")

# ✅ Reconoce X-Forwarded-Proto/Host del proxy (Railway) para que NO construya redirects a http
app.add_middleware(ProxyHeadersMiddleware, trusted_hosts="*")

# ✅ CORS (HTTPS y HTTP del mismo dominio + localhost)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "https://friendly-charisma-production-8624.up.railway.app",
        "http://friendly-charisma-production-8624.up.railway.app",
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# Rutas principales
app.include_router(api_router)
app.include_router(auth_router)
if tipo_router: app.include_router(tipo_router)
if modelo_router: app.include_router(modelo_router)

@app.on_event("startup")
def startup():
    if not ping_db():
        print("⚠️  No se pudo hacer ping a MongoDB (verifica MONGODB_URI).")
    seed_instruments()
