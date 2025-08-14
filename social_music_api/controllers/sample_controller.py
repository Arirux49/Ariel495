from fastapi import HTTPException
from typing import List, Optional
from utils.ids import parse_object_id
from utils.db import get_db
from bson import ObjectId

def _collection():
    return get_db()['samples']

def _instrumentos():
    return get_db()['instrumentos']

async def list_samples() -> List[dict]:
    items = await _collection().aggregate([
        {"$lookup": {
            "from": "instrumentos",
            "localField": "instrumento_ids",
            "foreignField": "_id",
            "as": "instrumentos"
        }}
    ]).to_list(length=1000)
    # stringify ids
    out = []
    for it in items:
        it["_id"] = str(it["_id"])
        for ins in it.get("instrumentos", []):
            ins["_id"] = str(ins["_id"])
        out.append(it)
    return out

async def create_sample(payload: dict) -> dict:
    if not payload:
        raise HTTPException(status_code=400, detail="payload vacío")
    nombre = payload.get("nombre") or ""
    instrumento_ids = payload.get("instrumento_ids") or []
    oids = []
    for rid in instrumento_ids:
        oid = parse_object_id(rid)
        if oid:
            oids.append(oid)
    doc = {
        "nombre": nombre,
        "descripcion": payload.get("descripcion", ""),
        "instrumento_ids": oids,
    }
    res = await _collection().insert_one(doc)
    doc["_id"] = str(res.inserted_id)
    doc["instrumento_ids"] = [str(x) for x in oids]
    return doc

async def update_sample(sample_id: str, payload: dict) -> dict:
    oid = parse_object_id(sample_id)
    if not oid:
        raise HTTPException(status_code=400, detail="id inválido")
    update = {}
    if "nombre" in payload: update["nombre"] = payload["nombre"]
    if "descripcion" in payload: update["descripcion"] = payload["descripcion"]
    if "instrumento_ids" in payload:
        ids = []
        for rid in payload.get("instrumento_ids", []):
            o = parse_object_id(rid)
            if o: ids.append(o)
        update["instrumento_ids"] = ids
    await _collection().update_one({"_id": oid}, {"$set": update})
    doc = await _collection().find_one({"_id": oid})
    if not doc:
        raise HTTPException(status_code=404, detail="no encontrado")
    doc["_id"] = str(doc["_id"])
    return doc

async def delete_sample(sample_id: str) -> dict:
    oid = parse_object_id(sample_id)
    if not oid:
        raise HTTPException(status_code=400, detail="id inválido")
    res = await _collection().delete_one({"_id": oid})
    if res.deleted_count == 0:
        raise HTTPException(status_code=404, detail="no encontrado")
    return {"deleted": True}
