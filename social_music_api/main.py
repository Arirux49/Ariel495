# social_music_api/main.py
from fastapi import FastAPI
from routes.api import api_router
from utils.db import ping_db
from utils.seed import seed_instruments

# ⬇️ NUEVO
from fastapi.middleware.cors import CORSMiddleware

# ⬇️ NUEVO: importar las rutas que te pasé en el ZIP
from routes.auth_routes import router as auth_router
from routes.tipo_routes import router as tipo_router
from routes.modelo_routes import router as modelo_router

app = FastAPI(title="Social Music API - Full")

# Rutas antiguas de tu API
app.include_router(api_router)

# ⬇️ NUEVO: incluir las rutas nuevas
app.include_router(auth_router)
app.include_router(tipo_router)
app.include_router(modelo_router)

# Permite peticiones desde tu UI (Vite)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "*"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup():
    ok = ping_db()
    if not ok:
        print("⚠️  No se pudo hacer ping a MongoDB (verifica MONGODB_URI).")
    seed_instruments()
