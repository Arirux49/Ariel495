
from fastapi import HTTPException
from typing import Dict, Any, List
from bson import ObjectId
from utils.db import recordings_collection, recording_samples, samples_collection

class GrabacionController:
    @staticmethod
    def crear(data: Dict[str, Any], usuario_id: str) -> Dict[str, Any]:
        if not data.get("nombre"):
            raise HTTPException(400, "nombre es requerido")
        doc = {
            "nombre": data["nombre"],
            "descripcion": data.get("descripcion"),
            "usuario_creador": ObjectId(usuario_id),
            "archivo": data.get("archivo"),
            "duracion": data.get("duracion")
        }
        res = recordings_collection.insert_one(doc)
        doc["_id"] = str(res.inserted_id)
        doc["usuario_creador"] = str(doc["usuario_creador"])
        return doc

    @staticmethod
    def agregar_samples(grabacion_id: str, sample_ids: List[str]) -> Dict[str, int]:
        gid = ObjectId(grabacion_id)
        if not recordings_collection.find_one({"_id": gid}):
            raise HTTPException(404, "grabación no existe")
        inserted = 0
        for sid in sample_ids:
            oid = ObjectId(sid)
            if not samples_collection.find_one({"_id": oid}):
                continue
            recording_samples.insert_one({"grabacion_id": gid, "sample_id": oid})
            inserted += 1
        return {"samples_agregados": inserted}
