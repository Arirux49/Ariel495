# routes/modelo_routes.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from bson import ObjectId
from utils.mongodb import get_collection

router = APIRouter(prefix="/modelo", tags=["Modelo principal"])

sample_coll = get_collection("samples")
inst_coll = get_collection("instruments")

class SampleIn(BaseModel):
    title: str = Field(..., min_length=2, max_length=80)
    instrument_id: str  # referencia a instruments._id

class SampleUpdate(BaseModel):
    title: Optional[str] = None
    instrument_id: Optional[str] = None

def _obj_id_ok(s: str) -> bool:
    return ObjectId.is_valid(s)

def _doc_to_out(d: Dict[str, Any]) -> Dict[str, Any]:
    d["id"] = str(d["_id"]); d.pop("_id", None)
    return d

def _exists_instrument(inst_id: str) -> bool:
    try:
        return inst_coll.count_documents({"_id": ObjectId(inst_id)}) > 0
    except Exception:
        return False

@router.get("/")
async def list_modelo() -> List[Dict[str, Any]]:
    items = []
    for d in sample_coll.find({}, {"title": 1, "instrument_id": 1}):
        items.append(_doc_to_out(d))
    return items

@router.post("/")
async def create_modelo(body: SampleIn):
    if not _obj_id_ok(body.instrument_id) or not _exists_instrument(body.instrument_id):
        raise HTTPException(400, "instrument_id no válido")
    doc = {"title": body.title.strip(), "instrument_id": body.instrument_id}
    res = sample_coll.insert_one(doc)
    doc["_id"] = res.inserted_id
    return _doc_to_out(doc)

@router.put("/{id}")
async def update_modelo(id: str, body: SampleUpdate):
    if not ObjectId.is_valid(id):
        raise HTTPException(400, "id inválido")
    update = {}
    if body.title: update["title"] = body.title.strip()
    if body.instrument_id:
        if not _obj_id_ok(body.instrument_id) or not _exists_instrument(body.instrument_id):
            raise HTTPException(400, "instrument_id no válido")
        update["instrument_id"] = body.instrument_id
    if not update:
        return {"updated": 0}
    res = sample_coll.update_one({"_id": ObjectId(id)}, {"$set": update})
    return {"updated": res.modified_count}

@router.delete("/{id}")
async def delete_modelo(id: str):
    if not ObjectId.is_valid(id):
        raise HTTPException(400, "id inválido")
    res = sample_coll.delete_one({"_id": ObjectId(id)})
    return {"deleted": res.deleted_count == 1}
