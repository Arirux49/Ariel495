from typing import List, Dict, Any  # Tipos usados para anotaciones
from bson import ObjectId          # Para convertir strings a ObjectId de MongoDB


# Pipeline que obtiene todos los samples relacionados con un instrumento específico
def pipeline_samples_por_instrumento(instrumento_id: str) -> List[Dict[str, Any]]:
    return [
        {
            # Filtro para obtener solo los samples que tienen el ID del instrumento dado
            "$match": {
                "instrumentos": ObjectId(instrumento_id)
            }
        },
        {
            # Lookup: une cada sample con su creador en la colección 'users'
            "$lookup": {
                "from": "users",                          # Colección con la que se hace el join
                "localField": "usuario_creador",          # Campo local en 'samples'
                "foreignField": "_id",                    # Campo en 'users' con el que se relaciona
                "as": "creador"                           # Resultado se guarda en este nuevo campo
            }
        },
        {
            # Unwind: descompone el array 'creador' en un solo documento
            "$unwind": "$creador"
        },
        {
            # Project: selecciona y transforma los campos a retornar
            "$project": {
                "_id": 1,                                 # Devuelve el ID del sample
                "nombre": 1,                              # Devuelve el nombre del sample
                "duracion": 1,                            # Devuelve la duración
                "creador": "$creador.nombre",             # Solo devuelve el nombre del usuario creador
                "fecha_creacion": 1                       # Incluye fecha de creación si está disponible
            }
        }
    ]


# Pipeline que retorna cada sample con los nombres de los instrumentos asociados
def pipeline_samples_con_instrumentos() -> List[Dict[str, Any]]:
    return [
        {
            # Lookup: une con la colección intermedia sample_instruments
            "$lookup": {
                "from": "sample_instruments",             # Tabla relacional
                "localField": "_id",                      # ID del sample actual
                "foreignField": "sample_id",              # Campo en tabla relacional que coincide
                "as": "relaciones_instrumentos"
            }
        },
        {
            # Unwind: descompone el array de relaciones en documentos individuales
            "$unwind": "$relaciones_instrumentos"
        },
        {
            # Lookup: une con la colección de instrumentos usando la relación anterior
            "$lookup": {
                "from": "instruments",                    # Colección de instrumentos
                "localField": "relaciones_instrumentos.instrumento_id",  # ID de instrumento
                "foreignField": "_id",
                "as": "instrumentos"                      # Resultado del join
            }
        },
        {
            # Group: agrupa nuevamente por sample y recolecta los nombres de instrumentos
            "$group": {
                "_id": "$_id",                            # Agrupa por ID de sample
                "nombre": {"$first": "$nombre"},          # Mantiene el nombre original
                "instrumentos": {"$push": "$instrumentos.nombre"}  # Array con los nombres de instrumentos
            }
        }
    ]
