
from fastapi import HTTPException
from typing import Dict, Any, List, Optional
from bson import ObjectId
from utils.db import samples_collection, sample_instruments, instruments_collection

class SampleController:
    @staticmethod
    def _to_response(doc: Dict[str, Any]) -> Dict[str, Any]:
        if not doc: return None
        doc["_id"] = str(doc["_id"])
        if doc.get("usuario_creador"): doc["usuario_creador"] = str(doc["usuario_creador"])
        return doc

    @staticmethod
    def create(data: Dict[str, Any], usuario_id: str) -> Dict[str, Any]:
        if not data.get("nombre"):
            raise HTTPException(400, "nombre es requerido")
        doc = {
            "nombre": data["nombre"],
            "descripcion": data.get("descripcion"),
            "usuario_creador": ObjectId(usuario_id),
            "archivo": data.get("archivo"),
            "duracion": data.get("duracion")
        }
        res = samples_collection.insert_one(doc)
        doc["_id"] = str(res.inserted_id)
        return doc

    @staticmethod
    def list_all() -> List[Dict[str, Any]]:
        return [SampleController._to_response(d) for d in samples_collection.find({})]

    @staticmethod
    def get_one(sample_id: str) -> Optional[Dict[str, Any]]:
        try:
            d = samples_collection.find_one({"_id": ObjectId(sample_id)})
            return SampleController._to_response(d)
        except Exception:
            raise HTTPException(400, "ID inválido")

    @staticmethod
    def patch(sample_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        if not data:
            raise HTTPException(400, "Nada que actualizar")
        try:
            res = samples_collection.find_one_and_update(
                {"_id": ObjectId(sample_id)},
                {"$set": data},
                return_document=True
            )
            if not res:
                raise HTTPException(404, "Sample no encontrado")
            return SampleController._to_response(res)
        except HTTPException:
            raise
        except Exception:
            raise HTTPException(400, "ID inválido")

    @staticmethod
    def delete(sample_id: str) -> None:
        try:
            res = samples_collection.delete_one({"_id": ObjectId(sample_id)})
            if res.deleted_count == 0:
                raise HTTPException(404, "Sample no encontrado")
        except HTTPException:
            raise
        except Exception:
            raise HTTPException(400, "ID inválido")

    @staticmethod
    def add_instruments(sample_id: str, instrumentos_ids: List[str]) -> Dict[str, int]:
        try:
            sid = ObjectId(sample_id)
        except Exception:
            raise HTTPException(400, "sample_id inválido")
        if not samples_collection.find_one({"_id": sid}):
            raise HTTPException(404, "Sample no existe")
        inserted = 0
        for inst in instrumentos_ids:
            try:
                iid = ObjectId(inst)
            except Exception:
                raise HTTPException(400, f"instrumento_id inválido: {inst}")
            if not instruments_collection.find_one({"_id": iid}):
                raise HTTPException(404, f"Instrumento no existe: {inst}")
            sample_instruments.insert_one({"sample_id": sid, "instrumento_id": iid})
            inserted += 1
        return {"instrumentos_agregados": inserted}
