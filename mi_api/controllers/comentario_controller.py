from fastapi import HTTPException, status
from datetime import datetime
from typing import List, Dict, Any, Optional
from bson import ObjectId
from pymongo import DESCENDING
from utils.db import comments_collection

class ComentarioController:
    @staticmethod
    def crear_comentario(
        contenido_id: str,
        es_sample: bool,
        usuario_id: str,
        texto: str
    ) -> Dict[str, Any]:
        """
        Crea un comentario en MongoDB.
        
        Args:
            contenido_id: ID del Sample/Grabación (ObjectId como string).
            es_sample: True para Sample, False para Grabación.
            usuario_id: ID del usuario (ObjectId como string).
            texto: Contenido del comentario.
            
        Returns:
            Dict: Comentario creado con _id convertido a string.
        """
        try:
            # Validación
            if not texto.strip():
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="El texto no puede estar vacío"
                )

            comentario = {
                "texto": texto,
                "usuario_id": ObjectId(usuario_id),
                "fecha": datetime.utcnow(),
                "es_sample": es_sample,
                "contenido_id": ObjectId(contenido_id)
            }
            
            # Insertar en MongoDB
            result = comments_collection.insert_one(comentario)
            comentario["_id"] = str(result.inserted_id)
            comentario["usuario_id"] = usuario_id  # Devolver como string
            comentario["contenido_id"] = contenido_id
            
            return comentario
            
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
        Consulta comentarios paginados desde MongoDB.
        
        Args:
            contenido_id: ID del contenido (string).
            es_sample: True para Sample, False para Grabación.
            skip: Paginación.
            limit: Límite por página.
            
        Returns:
            List[Dict]: Comentarios con _id y usuario_id como strings.
        """
        try:
            # Consulta con paginación y orden
            cursor = comments_collection.find({
                "contenido_id": ObjectId(contenido_id),
                "es_sample": es_sample
            }).sort("fecha", DESCENDING).skip(skip).limit(limit)
            
            # Convertir ObjectId a strings
            return [
                {
                    **comentario,
                    "_id": str(comentario["_id"]),
                    "usuario_id": str(comentario["usuario_id"]),
                    "contenido_id": contenido_id  # Mantener el original
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
        Elimina un comentario solo si el usuario es el autor.
        
        Args:
            comentario_id: ID del comentario (string).
            usuario_id: ID del usuario (string).
            
        Returns:
            Dict: Mensaje de éxito/error.
        """
        try:
            # Verificar autoría y eliminar
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