from fastapi import HTTPException
from typing import List, Optional
from utils.ids import parse_object_id
from utils.db import get_db
from bson import ObjectId

def _collection():
    return get_db()['instrumentos']

def _samples():
    return get_db()['samples']

async def list_instrumentos(q: Optional[str] = None) -> List[dict]:
    col = _collection()
    filtro = {}
    if q:
        filtro = {"$or": [{"nombre": {"$regex": q, "$options": "i"}}, {"descripcion": {"$regex": q, "$options": "i"}}]}
    return [ {**it, "_id": str(it["_id"])} for it in await col.find(filtro).to_list(length=1000) ]

async def create_instrumento(payload: dict) -> dict:
    nombre = (payload or {}).get("nombre")
    if not nombre:
        raise HTTPException(status_code=400, detail="nombre es requerido")
    doc = {"nombre": nombre, "descripcion": (payload or {}).get("descripcion", "")}
    res = await _collection().insert_one(doc)
    doc["_id"] = str(res.inserted_id)
    return doc

async def update_instrumento(instr_id: str, payload: dict) -> dict:
    oid = parse_object_id(instr_id)
    if not oid:
        raise HTTPException(status_code=400, detail="id inválido")
    await _collection().update_one({"_id": oid}, {"$set": payload or {}})
    doc = await _collection().find_one({"_id": oid})
    if not doc:
        raise HTTPException(status_code=404, detail="no encontrado")
    doc["_id"] = str(doc["_id"])
    return doc

async def delete_instrumento(instr_id: str) -> dict:
    oid = parse_object_id(instr_id)
    if not oid:
        raise HTTPException(status_code=400, detail="id inválido")
    # eliminación segura: verificar referencia en samples
    ref = await _samples().find_one({"instrumento_ids": oid})
    if ref:
        raise HTTPException(status_code=409, detail="No se puede eliminar: el instrumento está en uso por samples.")
    res = await _collection().delete_one({"_id": oid})
    if res.deleted_count == 0:
        raise HTTPException(status_code=404, detail="no encontrado")
    return {"deleted": True}
