from fastapi import HTTPException, status
from typing import List, Dict, Any
from bson import ObjectId
from utils.db import instruments_collection

class InstrumentoController:
    @staticmethod
    def create_instrumento(instrumento_data: Dict[str, Any]) -> Dict[str, Any]:
        if not instrumento_data.get("nombre"):
            raise HTTPException(status.HTTP_400_BAD_REQUEST, "El campo 'nombre' es obligatorio")
        instrumento = {
            "nombre": instrumento_data["nombre"],
            "descripción": instrumento_data.get("descripción", "")
        }
        result = instruments_collection.insert_one(instrumento)
        instrumento["_id"] = str(result.inserted_id)
        return instrumento

    @staticmethod
    def search_instrumentos(query: str = None) -> List[Dict[str, Any]]:
        filtro = {"nombre": {"$regex": query, "$options": "i"}} if query else {}
        instrumentos = instruments_collection.find(filtro)
        return [{**instr, "_id": str(instr["_id"])} for instr in instrumentos]