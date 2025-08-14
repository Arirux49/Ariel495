# social_music_api/main.py
from fastapi import FastAPI
from routes.api import api_router
from utils.db import ping_db
from utils.seed import seed_instruments

# ⬇️ NUEVO
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Social Music API - Full")
app.include_router(api_router)

# ⬇️ NUEVO: permite peticiones desde tu UI (Vite)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173", "*"], 
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
