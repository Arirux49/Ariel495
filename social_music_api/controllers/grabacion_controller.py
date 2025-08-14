from bson import ObjectId
from utils.mongodb import get_collection
from fastapi import HTTPException, status
import traceback

def _to_dict(doc):
    if not doc:
        return None
    d = dict(doc)
    d["id"] = str(d.pop("_id"))
    return d

async def create_grabacion(payload: dict) -> dict:
    try:
        coll = get_collection("grabaciones")
        doc = {
            "titulo": payload.get("titulo", "Sin título"),
            "descripcion": payload.get("descripcion", ""),
            "sample_ids": [ObjectId(x) for x in payload.get("sample_ids", [])],
        }
        res = await coll.insert_one(doc)
        created = await coll.find_one({"_id": res.inserted_id})
        return _to_dict(created)
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail="Error al crear grabación")

async def add_samples_to_grabacion(grabacion_id: str, sample_ids: list) -> dict:
    try:
        coll = get_collection("grabaciones")
        ids = [ObjectId(x) for x in sample_ids]
        await coll.update_one({"_id": ObjectId(grabacion_id)}, {"$addToSet": {"sample_ids": {"$each": ids}}})
        updated = await coll.find_one({"_id": ObjectId(grabacion_id)})
        return _to_dict(updated)
    except Exception:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail="Error al agregar samples")

async def list_grabaciones() -> list:
    try:
        coll = get_collection("grabaciones")
        cursor = coll.find({}).sort("_id", -1)
        out = []
        async for d in cursor:
            out.append(_to_dict(d))
        return out
    except Exception:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail="Error al listar grabaciones")

async def get_grabacion(grabacion_id: str) -> dict | None:
    coll = get_collection("grabaciones")
    d = await coll.find_one({"_id": ObjectId(grabacion_id)})
    return _to_dict(d) if d else None

async def delete_grabacion(grabacion_id: str) -> None:
    try:
        coll = get_collection("grabaciones")
        res = await coll.delete_one({"_id": ObjectId(grabacion_id)})
        if res.deleted_count == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Grabación no encontrada")
    except HTTPException:
        raise
    except Exception:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail="Error al eliminar grabación")
