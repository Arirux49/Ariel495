# social_music_api/main.py
from fastapi import FastAPI
from routes.api import api_router
from utils.db import ping_db
from utils.seed import seed_instruments

# ⬇️ CORS
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Social Music API - Full")
app.include_router(api_router)

# ✅ CORS: listas explícitas (NO usar "*" si allow_credentials=True)
ALLOWED_ORIGINS = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    # Si en algún momento sirves la UI desde otro dominio, agrégalo aquí:
    # "https://tu-frontend.com",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],      # incluye DELETE/POST/PATCH/OPTIONS
    allow_headers=["*"],      # incluye Authorization, Content-Type, etc.
)

@app.on_event("startup")
def startup():
    ok = ping_db()
    if not ok:
        print("⚠️  No se pudo hacer ping a MongoDB (verifica MONGODB_URI).")
    seed_instruments()
