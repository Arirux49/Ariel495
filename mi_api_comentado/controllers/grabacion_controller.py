# Importamos los tipos necesarios para declarar parámetros y estructuras de datos
from typing import Dict, List, Any

# Importamos las colecciones necesarias de la base de datos
from utils.db import recordings_collection, recording_samples, samples_collection

# ObjectId nos permite trabajar con los identificadores únicos de MongoDB
from bson import ObjectId

# Importamos HTTPException para lanzar errores controlados en FastAPI
from fastapi import HTTPException

# Definimos la clase controladora para las grabaciones
class GrabacionController:
    @staticmethod
    def create_with_samples(grabacion_data: Dict[str, Any], samples_ids: List[str]) -> Dict[str, Any]:
        """
        Crea una nueva grabación y enlaza los samples utilizados.

        Args:
            grabacion_data: Diccionario con los datos de la grabación (nombre, usuario_id, archivo, duracion).
            samples_ids: Lista de IDs de samples utilizados (strings que representan ObjectId).

        Returns:
            Un diccionario con los datos de la grabación creada y los IDs de los samples utilizados.
        """

        # Validamos que todos los IDs de los samples existan en la base de datos
        for sid in samples_ids:
            if not samples_collection.find_one({"_id": ObjectId(sid)}):
                raise HTTPException(404, f"Sample {sid} no existe")

        # Creamos el documento de la grabación con los datos proporcionados
        grabacion = {
            "nombre": grabacion_data["nombre"],  # Nombre de la grabación
            "usuario_creador": ObjectId(grabacion_data["usuario_id"]),  # Referencia al usuario que la creó
            "archivo": grabacion_data["archivo"],  # URL o nombre del archivo
            "duracion": grabacion_data.get("duracion")  # Duración opcional
        }

        # Insertamos la grabación en la colección de grabaciones
        result = recordings_collection.insert_one(grabacion)

        # Por cada sample relacionado, insertamos una relación en la tabla intermedia recording_samples
        for sid in samples_ids:
            recording_samples.insert_one({
                "grabacion_id": result.inserted_id,  # Referencia a la grabación
                "sample_id": ObjectId(sid)  # Referencia al sample
            })

        # Preparamos la respuesta incluyendo el ID de la grabación y los samples utilizados
        grabacion["_id"] = str(result.inserted_id)
        grabacion["samples_utilizados"] = samples_ids

        return grabacion