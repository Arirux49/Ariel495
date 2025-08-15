from fastapi import APIRouter, HTTPException, Query
from typing import Optional, List, Dict, Any
from utils.db import get_db
from utils.ids import parse_object_id

router = APIRouter(prefix="/instrumentos", tags=["Instrumentos"])

def _col():
    return get_db()["instrumentos"]

def _samples():
    return get_db()["samples"]

@router.get("")
async def list_instrumentos(q: Optional[str] = Query(None)):
    filtro = {}
    if q:
        filtro = {"$or": [
            {"nombre": {"$regex": q, "$options": "i"}},
            {"descripcion": {"$regex": q, "$options": "i"}},
        ]}
    items = await _col().find(filtro).to_list(length=1000)
    for it in items:
        it["_id"] = str(it["_id"])
    return items

@router.post("")
async def create_instrumento(payload: Dict[str, Any]):
    nombre = (payload or {}).get("nombre")
    if not nombre:
        raise HTTPException(status_code=400, detail="nombre es requerido")
    doc = {"nombre": nombre, "descripcion": (payload or {}).get("descripcion", "")}
    res = await _col().insert_one(doc)
    doc["_id"] = str(res.inserted_id)
    return doc

@router.put("/{instrumento_id}")
async def update_instrumento(instrumento_id: str, payload: Dict[str, Any]):
    oid = parse_object_id(instrumento_id)
    if not oid:
        raise HTTPException(status_code=400, detail="id inválido")
    await _col().update_one({"_id": oid}, {"$set": payload or {}})
    doc = await _col().find_one({"_id": oid})
    if not doc:
        raise HTTPException(status_code=404, detail="no encontrado")
    doc["_id"] = str(doc["_id"])
    return doc

@router.delete("/{instrumento_id}")
async def delete_instrumento(instrumento_id: str):
    oid = parse_object_id(instrumento_id)
    if not oid:
        raise HTTPException(status_code=400, detail="id inválido")
    ref = await _samples().find_one({"instrumento_ids": oid})
    if ref:
        raise HTTPException(status_code=409, detail="No se puede eliminar: el instrumento está en uso por samples.")
    res = await _col().delete_one({"_id": oid})
    if res.deleted_count == 0:
        raise HTTPException(status_code=404, detail="no encontrado")
    return {"deleted": True}
