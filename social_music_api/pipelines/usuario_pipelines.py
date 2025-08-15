from typing import List, Dict, Any
from bson import ObjectId

def pipeline_instrumentos_por_usuario(usuario_id: str) -> List[Dict[str, Any]]:
    return [
        {
            "$match": {
                "_id": ObjectId(usuario_id)
            }
        },
        {
            "$lookup": {
                "from": "user_instruments",
                "localField": "_id",
                "foreignField": "usuario_id",
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
            "$unwind": "$instrumentos"
        },
        {
            "$group": {
                "_id": "$_id",
                "nombre_usuario": {"$first": "$nombre"},
                "instrumentos": {"$push": "$instrumentos.nombre"}
            }
        }
    ]