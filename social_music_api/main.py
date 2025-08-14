# social_music_api/main.py
from fastapi import FastAPI
from routes.api import api_router
from utils.db import ping_db
from utils.seed import seed_instruments

from fastapi.middleware.cors import CORSMiddleware
from decouple import config

app = FastAPI(title="Social Music API - Full")

# Permite cualquier puerto en localhost / 127.0.0.1 en desarrollo.
# (Evita errores si Vite cambia de puerto o usas 127.0.0.1 vs localhost)
DEV_ORIGIN_REGEX = r"https?://(localhost|127\.0\.0\.1)(:\d+)?$"

# Orígenes adicionales opcionales (producción), coma-separados en env:
# FRONTEND_ORIGINS="https://mi-frontend.com,https://otro.com"
extra_origins = [
    o.strip() for o in config("FRONTEND_ORIGINS", default="").split(",") if o.strip()
]

app.add_middleware(
    CORSMiddleware,
    # Usamos regex para dev y además la lista explícita por si agregas dominios
    allow_origin_regex=DEV_ORIGIN_REGEX,
    allow_origins=extra_origins,          # ← aquí puedes poner tu dominio de FE si lo tienes
    allow_credentials=True,               # ok porque NO usamos "*" como origen
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["*"],                  # Authorization, Content-Type, etc.
    expose_headers=["*"],                 # opcional: por si necesitas leer headers
)

app.include_router(api_router)

@app.on_event("startup")
def startup():
    ok = ping_db()
    if not ok:
        print("⚠️  No se pudo hacer ping a MongoDB (verifica MONGODB_URI).")
    seed_instruments()
