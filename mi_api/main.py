from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.api import api_router
from utils.db import ping_db
import uvicorn

app = FastAPI(
    title="Social Music API",
    description="API social para musicos",
    version="1.0.0",
    openapi_url="/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)

@app.on_event("startup")
async def startup_event():
    if not ping_db():
        raise RuntimeError("Error al conectar con MongoDB")

@app.get("/health", tags=["System"])
async def health_check():
    return {
        "status": "active",
        "database": "MongoDB" if ping_db() else "offline",
        "services": ["Firebase Auth", "Firebase Storage"]
    }

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True, log_level="debug")