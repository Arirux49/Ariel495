from typing import List, Dict, Any  # Importa tipos de datos para anotaciones de tipo.
from bson import ObjectId  # Para manejar identificadores de MongoDB.

# Función que retorna un pipeline de agregación para encontrar las grabaciones más populares.
def pipeline_grabaciones_populares(min_samples: int = 3) -> List[Dict[str, Any]]:
    return [
        {
            "$lookup": {
                "from": "recording_samples",          # Se hace un JOIN virtual con la colección recording_samples
                "localField": "_id",                  # Campo en la colección base (grabaciones)
                "foreignField": "grabacion_id",       # Campo en recording_samples que debe coincidir
                "as": "samples_utilizados"            # El resultado se almacenará en este nuevo campo
            }
        },
        {
            "$addFields": {
                "total_samples": {"$size": "$samples_utilizados"}  # Agrega un nuevo campo 'total_samples' contando los samples
            }
        },
        {
            "$match": {
                "total_samples": {"$gte": min_samples}  # Filtra solo aquellas grabaciones con al menos 'min_samples' asociados
            }
        },
        {
            "$sort": {"total_samples": -1}  # Ordena las grabaciones por cantidad de samples en orden descendente
        },
        {
            "$limit": 10  # Limita el resultado a los 10 primeros documentos
        },
        {
            "$project": {
                "nombre": 1,            # Solo incluye el nombre de la grabación
                "duracion": 1,          # Incluye la duración
                "total_samples": 1,     # Incluye la cantidad total de samples asociados
                "usuario_creador": 1    # Incluye el ID del usuario creador
            }
        }
    ]
