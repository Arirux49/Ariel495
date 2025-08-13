from typing import List, Dict, Any
from bson import ObjectId

def pipeline_samples_por_instrumento(instrumento_id: str) -> List[Dict[str, Any]]:
    return [
        {
            "$match": {
                "instrumentos": ObjectId(instrumento_id)
            }
        },
        {
            "$lookup": {
                "from": "users",
                "localField": "usuario_creador",
                "foreignField": "_id",
                "as": "creador"
            }
        },
        {
            "$unwind": "$creador"
        },
        {
            "$project": {
                "_id": 1,
                "nombre": 1,
                "duracion": 1,
                "creador": "$creador.nombre",
                "fecha_creacion": 1
            }
        }
    ]

def pipeline_samples_con_instrumentos() -> List[Dict[str, Any]]:
    return [
        {
            "$lookup": {
                "from": "sample_instruments",
                "localField": "_id",
                "foreignField": "sample_id",
                "as": "relaciones_instrumentos"
            }
        },
        {
            "$unwind": "$relaciones_instrumentos"
        },
        {
            "$lookup": {
                "from": "instruments",
                "localField": "relaciones_instrumentos.instrumento_id",
                "foreignField": "_id",
                "as": "instrumentos"
            }
        },
        {
            "$group": {
                "_id": "$_id",
                "nombre": {"$first": "$nombre"},
                "instrumentos": {"$push": "$instrumentos.nombre"}
            }
        }
    ]