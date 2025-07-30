from fastapi import HTTPException, UploadFile
from typing import Dict, Any, List
from utils.db import samples_collection, sample_instruments, instruments_collection
from utils.storage import upload_audio
from bson import ObjectId

class SampleController:
    @staticmethod
    async def upload_sample(file: UploadFile, metadata: Dict[str, Any]) -> Dict[str, Any]:
        url_archivo = await upload_audio(file)
        sample = {
            "nombre": metadata["nombre"],
            "usuario_creador": ObjectId(metadata["usuario_id"]),
            "archivo": url_archivo,
            "duracion": metadata.get("duracion")
        }
        result = samples_collection.insert_one(sample)
        sample_id = result.inserted_id
        for instr_id in metadata.get("instrumentos_ids", []):
            if not instruments_collection.find_one({"_id": ObjectId(instr_id)}):
                raise HTTPException(404, f"Instrumento {instr_id} no existe")
            sample_instruments.insert_one({
                "sample_id": sample_id,
                "instrumento_id": ObjectId(instr_id)
            })
        sample["_id"] = str(sample_id)
        return sample

    @staticmethod
    def get_by_instrumento(instrumento_id: str) -> List[Dict[str, Any]]:
        return list(samples_collection.aggregate([
            {
                "$lookup": {
                    "from": "sample_instruments",
                    "localField": "_id",
                    "foreignField": "sample_id",
                    "as": "relaciones"
                }
            },
            { "$unwind": "$relaciones" },
            {
                "$match": {
                    "relaciones.instrumento_id": ObjectId(instrumento_id)
                }
            },
            {
                "$project": {
                    "_id": { "$toString": "$_id" },
                    "nombre": 1,
                    "archivo": 1,
                    "duracion": 1
                }
            }
        ]))
