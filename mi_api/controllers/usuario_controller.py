from fastapi import HTTPException
from typing import List, Dict, Any
from bson import ObjectId
from utils.db import users_collection, user_instruments, instruments_collection

class UsuarioController:
    @staticmethod
    def get_usuario(usuario_id: str) -> Dict[str, Any]:
        try:
            usuario = users_collection.find_one({"_id": ObjectId(usuario_id)})
            if not usuario:
                raise HTTPException(404, "Usuario no encontrado")
            usuario["_id"] = str(usuario["_id"])
            return usuario
        except Exception as e:
            raise HTTPException(400, f"ID inválido: {str(e)}")

    @staticmethod
    def add_instrumentos(usuario_id: str, instrumentos_ids: List[str]) -> Dict[str, int]:
        relaciones = []
        for instr_id in instrumentos_ids:
            if not instruments_collection.find_one({"_id": ObjectId(instr_id)}):
                raise HTTPException(404, f"Instrumento {instr_id} no existe")
            relaciones.append({
                "usuario_id": ObjectId(usuario_id),
                "instrumento_id": ObjectId(instr_id)
            })
        if relaciones:
            user_instruments.insert_many(relaciones)
        return {"instrumentos_agregados": len(relaciones)}