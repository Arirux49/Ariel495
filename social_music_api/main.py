# social_music_api/main.py
from fastapi import FastAPI
from routes.api import api_router
from utils.db import ping_db
from utils.seed import seed_instruments

# CORS
from fastapi.middleware.cors import CORSMiddleware
from decouple import config

app = FastAPI(title="Social Music API - Full")

# ✅ CORS: listas explícitas (NO usar "*" si allow_credentials=True)
#    Puedes agregar orígenes extra con FRONTEND_ORIGINS="https://mi-frontend.com,https://otro.com"
_default_origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]
_extra = [o.strip() for o in config("FRONTEND_ORIGINS", default="").split(",") if o.strip()]
ALLOWED_ORIGINS = _default_origins + _extra

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["*"],  # Authorization, Content-Type, etc.
)

# Routers
app.include_router(api_router)

@app.on_event("startup")
def startup():
    ok = ping_db()
    if not ok:
        print("⚠️  No se pudo hacer ping a MongoDB (verifica MONGODB_URI).")
    seed_instruments()
