from motor.motor_asyncio import AsyncIOMotorClient
from .settings import MONGODB_URI, DB_NAME

_client = None
_db = None

def get_client():
    global _client
    if _client is None:
        if not MONGODB_URI:
            raise RuntimeError("MONGODB_URI no está definido en el .env")
        _client = AsyncIOMotorClient(MONGODB_URI)
    return _client

def get_db():
    global _db
    if _db is None:
        _db = get_client()[DB_NAME]
    return _db

async def ping_db() -> bool:
    try:
        await get_client().admin.command("ping")
        return True
    except Exception as e:
        print("Ping MongoDB falló:", e)
        return False
