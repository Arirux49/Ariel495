from typing import List, Dict, Any  # Tipado para listas y diccionarios
from bson import ObjectId          # Para trabajar con ObjectId de MongoDB


# Pipeline para obtener los nombres de los instrumentos asociados a un usuario específico
def pipeline_instrumentos_por_usuario(usuario_id: str) -> List[Dict[str, Any]]:
    return [
        {
            # Etapa 1: Filtra al usuario específico por su ID
            "$match": {
                "_id": ObjectId(usuario_id)
            }
        },
        {
            # Etapa 2: Hace un join con la colección intermedia 'user_instruments'
            # para obtener los instrumentos que el usuario tiene registrados
            "$lookup": {
                "from": "user_instruments",           # Colección intermedia
                "localField": "_id",                  # Campo en la colección actual ('users')
                "foreignField": "usuario_id",         # Campo con el que se une en 'user_instruments'
                "as": "relaciones_instrumentos"       # Nombre del nuevo campo resultante del join
            }
        },
        {
            # Etapa 3: Descompone el array de relaciones en documentos individuales
            "$unwind": "$relaciones_instrumentos"
        },
        {
            # Etapa 4: Hace un segundo join para traer los datos reales de los instrumentos
            "$lookup": {
                "from": "instruments",                                    # Colección de instrumentos
                "localField": "relaciones_instrumentos.instrumento_id",  # Campo relacional
                "foreignField": "_id",
                "as": "instrumentos"                                      # Resultado del join
            }
        },
        {
            # Etapa 5: Descompone el array 'instrumentos' para acceder a los nombres
            "$unwind": "$instrumentos"
        },
        {
            # Etapa 6: Agrupa por usuario y recolecta todos los nombres de instrumentos
            "$group": {
                "_id": "$_id",                                 # Agrupa por ID del usuario
                "nombre_usuario": {"$first": "$nombre"},       # Guarda el nombre del usuario
                "instrumentos": {"$push": "$instrumentos.nombre"}  # Recolecta nombres en una lista
            }
        }
    ]
