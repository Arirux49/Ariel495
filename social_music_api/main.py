from fastapi import FastAPI
from routes.api import api_router
from utils.db import ping_db
from utils.seed import seed_instruments
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Social Music API - Full")
app.include_router(api_router)

# 🚨 Permite cualquier origen (solo para pruebas)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],       # Acepta cualquier origen
    allow_credentials=True,    # Cuidado: inseguro en producción
    allow_methods=["*"],       # Acepta todos los métodos
    allow_headers=["*"],       # Acepta todos los headers
)

@app.on_event("startup")
def startup():
    ok = ping_db()
    if not ok:
        print("⚠️  No se pudo hacer ping a MongoDB (verifica MONGODB_URI).")
    seed_instruments()
