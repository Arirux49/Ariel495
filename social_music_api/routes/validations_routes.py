
from fastapi import APIRouter
from typing import List, Dict
from bson import ObjectId
from utils.db import samples_collection

router = APIRouter(prefix="/validations", tags=["Validations"])

@router.post("/recording-add-samples")
async def validate_recording_add_samples(payload: Dict[str, List[str]]):
    sample_ids = payload.get("sample_ids", [])
    oids, rechazados = [], []
    for s in sample_ids:
        try:
            oids.append(ObjectId(s))
        except Exception:
            rechazados.append(s)
    encontrados = list(samples_collection.find({"_id": {"$in": oids}, "deleted": {"$ne": True}}, {"_id": 1}))
    validos = set(str(d["_id"]) for d in encontrados)
    for s in sample_ids:
        if s not in validos and s not in rechazados:
            rechazados.append(s)
    return {"ok": len(rechazados) == 0, "validos": list(validos), "rechazados": rechazados}
