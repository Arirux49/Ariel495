from .db import get_db
from bson import ObjectId

async def seed_instruments():
    col = get_db()["instrumentos"]
    count = await col.count_documents({})
    if count == 0:
        await col.insert_many([
            {"nombre": "Guitarra", "descripcion": "Cuerdas"},
            {"nombre": "Batería", "descripcion": "Percusión"},
            {"nombre": "Piano", "descripcion": "Teclas"},
        ])
        print("✅ Seed: instrumentos insertados")
