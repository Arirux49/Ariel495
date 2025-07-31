# Importamos HTTPException y status para manejar errores y códigos HTTP estándar
from fastapi import HTTPException, status

# Tipos utilizados para tipado de datos
from typing import List, Dict, Any

# ObjectId se utiliza para trabajar con IDs de MongoDB
from bson import ObjectId

# Conexión a la colección de instrumentos en la base de datos
from utils.db import instruments_collection

# Definimos la clase del controlador de instrumentos
class InstrumentoController:
    @staticmethod
    def create_instrumento(instrumento_data: Dict[str, Any]) -> Dict[str, Any]:
        # Validamos que el campo nombre esté presente
        if not instrumento_data.get("nombre"):
            raise HTTPException(
                status.HTTP_400_BAD_REQUEST,
                "El campo 'nombre' es obligatorio"
            )

        # Creamos el diccionario del instrumento
        instrumento = {
            "nombre": instrumento_data["nombre"],
            "descripción": instrumento_data.get("descripción", "")  # Valor por defecto: cadena vacía
        }

        # Insertamos el instrumento en la colección
        result = instruments_collection.insert_one(instrumento)

        # Convertimos el ObjectId a string para retornarlo
        instrumento["_id"] = str(result.inserted_id)

        return instrumento

    @staticmethod
    def search_instrumentos(query: str = None) -> List[Dict[str, Any]]:
        # Si se proporciona query, se hace búsqueda por nombre (insensible a mayúsculas/minúsculas)
        filtro = {"nombre": {"$regex": query, "$options": "i"}} if query else {}

        # Ejecutamos la búsqueda en MongoDB
        instrumentos = instruments_collection.find(filtro)

        # Convertimos los ObjectId a string para que sean compatibles con JSON
        return [{**instr, "_id": str(instr["_id"])} for instr in instrumentos]
