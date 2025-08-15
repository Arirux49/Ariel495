# routes/tipo_routes.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from bson import ObjectId
from utils.mongodb import get_collection

router = APIRouter(prefix="/tipo", tags=["Tipo"])

inst_coll = get_collection("instruments")
sample_coll = get_collection("samples")

class TipoIn(BaseModel):
    name: str = Field(..., min_length=2, max_length=60)
    estado: Optional[str] = "activo"  # activo | inactivo

class TipoUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=60)
    estado: Optional[str] = None

def _doc_to_out(d: Dict[str, Any]) -> Dict[str, Any]:
    d["id"] = str(d["_id"]); d.pop("_id", None)
    return d

@router.get("/")
async def list_tipos() -> List[Dict[str, Any]]:
    items = []
    for d in inst_coll.find({}, {"name": 1, "estado": 1}):
        items.append(_doc_to_out(d))
    return items

@router.post("/")
async def create_tipo(body: TipoIn):
    try:
        inst_coll.create_index("name", unique=True)
    except Exception:
        pass
    doc = {"name": body.name.strip(), "estado": body.estado or "activo"}
    res = inst_coll.insert_one(doc)
    doc["_id"] = res.inserted_id
    return _doc_to_out(doc)

@router.put("/{id}")
async def update_tipo(id: str, body: TipoUpdate):
    if not ObjectId.is_valid(id):
        raise HTTPException(400, "id inválido")
    update = {}
    if body.name: update["name"] = body.name.strip()
    if body.estado: update["estado"] = body.estado
    if not update:
        return {"updated": 0}
    res = inst_coll.update_one({"_id": ObjectId(id)}, {"$set": update})
    return {"updated": res.modified_count}

@router.delete("/{id}")
async def delete_tipo(id: str):
    if not ObjectId.is_valid(id):
        raise HTTPException(400, "id inválido")
    refs = sample_coll.count_documents({
        "$or": [
            {"instrument_id": id},
            {"instrument_id": str(ObjectId(id))},
            {"instrument_id": ObjectId(id)},
        ]
    })
    if refs > 0:
        inst_coll.update_one({"_id": ObjectId(id)}, {"$set": {"estado": "inactivo"}})
        return {"safe_deleted": True, "logical": True, "reason": "en_uso", "referencias": refs}
    res = inst_coll.delete_one({"_id": ObjectId(id)})
    return {"deleted": res.deleted_count == 1}
