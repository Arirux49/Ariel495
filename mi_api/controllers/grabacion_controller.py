from typing import Dict, List, Any
from utils.db import recordings_collection, recording_samples, samples_collection
from bson import ObjectId
from fastapi import HTTPException

class GrabacionController:
    @staticmethod
    def create_with_samples(grabacion_data: Dict[str, Any], samples_ids: List[str]) -> Dict[str, Any]:
        for sid in samples_ids:
            if not samples_collection.find_one({"_id": ObjectId(sid)}):
                raise HTTPException(404, f"Sample {sid} no existe")
        grabacion = {
            "nombre": grabacion_data["nombre"],
            "usuario_creador": ObjectId(grabacion_data["usuario_id"]),
            "archivo": grabacion_data["archivo"],
            "duracion": grabacion_data.get("duracion")
        }
        result = recordings_collection.insert_one(grabacion)
        for sid in samples_ids:
            recording_samples.insert_one({
                "grabacion_id": result.inserted_id,
                "sample_id": ObjectId(sid)
            })
        grabacion["_id"] = str(result.inserted_id)
        grabacion["samples_utilizados"] = samples_ids
        return grabacion