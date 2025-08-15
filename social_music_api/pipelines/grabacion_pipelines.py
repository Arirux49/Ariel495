from typing import List, Dict, Any
from bson import ObjectId

def pipeline_grabaciones_populares(min_samples: int = 3) -> List[Dict[str, Any]]:
    return [
        {
            "$lookup": {
                "from": "recording_samples",
                "localField": "_id",
                "foreignField": "grabacion_id",
                "as": "samples_utilizados"
            }
        },
        {
            "$addFields": {
                "total_samples": {"$size": "$samples_utilizados"}
            }
        },
        {
            "$match": {
                "total_samples": {"$gte": min_samples}
            }
        },
        {
            "$sort": {"total_samples": -1}
        },
        {
            "$limit": 10
        },
        {
            "$project": {
                "nombre": 1,
                "duracion": 1,
                "total_samples": 1,
                "usuario_creador": 1
            }
        }
    ]