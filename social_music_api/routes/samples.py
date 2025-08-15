from fastapi import APIRouter, HTTPException
from typing import Dict, Any, List
from utils.db import get_db
from utils.ids import parse_object_id

router = APIRouter(prefix="/samples", tags=["Samples"])

def _col():
    return get_db()["samples"]

@router.get("")
async def list_samples():
    # join con instrumentos
    items = await get_db()["samples"].aggregate([
        {"$lookup": {
            "from": "instrumentos",
            "localField": "instrumento_ids",
            "foreignField": "_id",
            "as": "instrumentos"
        }}
    ]).to_list(length=1000)
    for it in items:
        it["_id"] = str(it["_id"])
        for ins in it.get("instrumentos", []):
            ins["_id"] = str(ins["_id"])
    return items

@router.post("")
async def create_sample(payload: Dict[str, Any]):
    if not payload:
        raise HTTPException(status_code=400, detail="payload vacío")
    oids: List = []
    for rid in payload.get("instrumento_ids", []):
        oid = parse_object_id(rid)
        if oid: oids.append(oid)
    doc = {
        "nombre": payload.get("nombre") or "",
        "descripcion": payload.get("descripcion") or "",
        "instrumento_ids": oids,
    }
    res = await _col().insert_one(doc)
    doc["_id"] = str(res.inserted_id)
    doc["instrumento_ids"] = [str(x) for x in oids]
    return doc

@router.put("/{sample_id}")
async def update_sample(sample_id: str, payload: Dict[str, Any]):
    oid = parse_object_id(sample_id)
    if not oid:
        raise HTTPException(status_code=400, detail="id inválido")
    update: Dict[str, Any] = {}
    if "nombre" in payload: update["nombre"] = payload["nombre"]
    if "descripcion" in payload: update["descripcion"] = payload["descripcion"]
    if "instrumento_ids" in payload:
        ids = []
        for rid in payload.get("instrumento_ids", []):
            o = parse_object_id(rid)
            if o: ids.append(o)
        update["instrumento_ids"] = ids
    await _col().update_one({"_id": oid}, {"$set": update})
    doc = await _col().find_one({"_id": oid})
    if not doc:
        raise HTTPException(status_code=404, detail="no encontrado")
    doc["_id"] = str(doc["_id"])
    return doc

@router.delete("/{sample_id}")
async def delete_sample(sample_id: str):
    oid = parse_object_id(sample_id)
    if not oid:
        raise HTTPException(status_code=400, detail="id inválido")
    res = await _col().delete_one({"_id": oid})
    if res.deleted_count == 0:
        raise HTTPException(status_code=404, detail="no encontrado")
    return {"deleted": True}
