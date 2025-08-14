# social_music_api/main.py
from fastapi import FastAPI
from routes.api import api_router
from utils.db import ping_db
from utils.seed import seed_instruments

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Social Music API - Full")

app.add_middleware(
    CORSMiddleware,
    allow_origin_regex=".*",   # acepta cualquier origen
    allow_origins=["*"],       # redundante pero ok
    allow_credentials=False,   # <— clave si usas "*"
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)

@app.on_event("startup")
def startup():
    ok = ping_db()
    if not ok:
        print("⚠️  No se pudo hacer ping a MongoDB (verifica MONGODB_URI).")
    seed_instruments()
