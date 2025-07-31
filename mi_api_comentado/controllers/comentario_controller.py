
from fastapi import HTTPException, status  # Importamos clases para manejar excepciones HTTP y códigos de estado
from datetime import datetime              # Para registrar la fecha y hora de los comentarios
from typing import List, Dict, Any, Optional  # Tipos de datos para anotaciones de funciones
from bson import ObjectId                  # Para trabajar con ObjectId de MongoDB
from pymongo import DESCENDING             # Constante para ordenar resultados descendentes
from utils.db import comments_collection   # Colección de comentarios en la base de datos

# Definimos la clase controlador de comentarios
class ComentarioController:
    @staticmethod
    def crear_comentario(
        contenido_id: str,     # ID del contenido (grabación o sample)
        es_sample: bool,       # Booleano que indica si es sample (True) o grabación (False)
        usuario_id: str,       # ID del usuario que comenta
        texto: str             # Texto del comentario
    ) -> Dict[str, Any]:       # Retorna un diccionario con el comentario creado
        """
        Crea un comentario en MongoDB.
        """
        try:
            # Validación: asegurarse que el comentario no esté vacío
            if not texto.strip():
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="El texto no puede estar vacío"
                )

            # Diccionario con los datos del comentario
            comentario = {
                "texto": texto,
                "usuario_id": ObjectId(usuario_id),       # Convertimos a ObjectId para almacenar en Mongo
                "fecha": datetime.utcnow(),               # Fecha actual en formato UTC
                "es_sample": es_sample,                   # Indica si es sample o grabación
                "contenido_id": ObjectId(contenido_id)    # ID del contenido relacionado
            }

            # Insertar el comentario en la colección
            result = comments_collection.insert_one(comentario)

            # Agregar el ID insertado y convertir a string para respuesta
            comentario["_id"] = str(result.inserted_id)
            comentario["usuario_id"] = usuario_id         # Convertimos de nuevo a string para la respuesta
            comentario["contenido_id"] = contenido_id

            return comentario  # Devolvemos el comentario con IDs como strings

        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error al crear comentario: {str(e)}"
            )

    @staticmethod
    def obtener_comentarios(
        contenido_id: str,
        es_sample: bool,
        skip: int = 0,
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Consulta comentarios desde MongoDB con paginación.
        """
        try:
            # Consulta Mongo filtrando por ID de contenido y si es sample
            cursor = comments_collection.find({
                "contenido_id": ObjectId(contenido_id),
                "es_sample": es_sample
            }).sort("fecha", DESCENDING).skip(skip).limit(limit)

            # Convertimos los resultados a listas de diccionarios con IDs como strings
            return [
                {
                    **comentario,
                    "_id": str(comentario["_id"]),
                    "usuario_id": str(comentario["usuario_id"]),
                    "contenido_id": contenido_id
                }
                for comentario in cursor
            ]

        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error al obtener comentarios: {str(e)}"
            )

    @staticmethod
    def eliminar_comentario(
        comentario_id: str,
        usuario_id: str
    ) -> Dict[str, str]:
        """
        Elimina un comentario de MongoDB si pertenece al usuario.
        """
        try:
            # Verifica que el usuario sea el autor y elimina el comentario
            result = comments_collection.delete_one({
                "_id": ObjectId(comentario_id),
                "usuario_id": ObjectId(usuario_id)
            })

            if result.deleted_count == 0:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Comentario no encontrado o no autorizado"
                )

            return {"message": "Comentario eliminado correctamente"}

        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error al eliminar comentario: {str(e)}"
            )
