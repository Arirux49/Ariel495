# Importamos HTTPException para manejar errores HTTP desde FastAPI
from fastapi import HTTPException

# Tipos para anotaciones de funciones
from typing import List, Dict, Any

# ObjectId permite trabajar con IDs de documentos en MongoDB
from bson import ObjectId

# Importamos las colecciones necesarias desde la utilidad de base de datos
from utils.db import users_collection, user_instruments, instruments_collection

# Controlador para manejar la lógica relacionada con los usuarios
class UsuarioController:

    # Método estático para obtener un usuario por su ID
    @staticmethod
    def get_usuario(usuario_id: str) -> Dict[str, Any]:
        try:
            # Buscar el usuario por su ID en la base de datos
            usuario = users_collection.find_one({"_id": ObjectId(usuario_id)})
            # Si no se encuentra, lanzar error 404
            if not usuario:
                raise HTTPException(404, "Usuario no encontrado")
            # Convertimos el ObjectId a string para que sea serializable por JSON
            usuario["_id"] = str(usuario["_id"])
            return usuario
        except Exception as e:
            # Si hay algún error (como ID malformado), lanzar error 400
            raise HTTPException(400, f"ID inválido: {str(e)}")

    # Método para asociar instrumentos a un usuario
    @staticmethod
    def add_instrumentos(usuario_id: str, instrumentos_ids: List[str]) -> Dict[str, int]:
        relaciones = []  # Lista para almacenar relaciones válidas

        # Iteramos por cada ID de instrumento recibido
        for instr_id in instrumentos_ids:
            # Verificamos que el instrumento exista
            if not instruments_collection.find_one({"_id": ObjectId(instr_id)}):
                raise HTTPException(404, f"Instrumento {instr_id} no existe")

            # Creamos la relación entre usuario e instrumento
            relaciones.append({
                "usuario_id": ObjectId(usuario_id),
                "instrumento_id": ObjectId(instr_id)
            })

        # Insertamos todas las relaciones en la colección intermedia
        if relaciones:
            user_instruments.insert_many(relaciones)

        # Retornamos cuántos instrumentos se asociaron
        return {"instrumentos_agregados": len(relaciones)}
