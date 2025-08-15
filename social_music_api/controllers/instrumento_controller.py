
from fastapi import HTTPException, status
from typing import List, Dict, Any, Optional
from bson import ObjectId
from utils.db import instruments_collection, sample_instruments

class InstrumentoController:
    @staticmethod
    def _to_response(doc: Dict[str, Any]) -> Dict[str, Any]:
        if not doc: return None
        doc["_id"] = str(doc["_id"])
        return doc

    @staticmethod
    def create_instrumento(data: Dict[str, Any]) -> Dict[str, Any]:
        nombre = (data.get("nombre") or "").strip()
        if not nombre:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, "El campo 'nombre' es obligatorio")
        instrumento = {"nombre": nombre, "descripcion": data.get("descripcion")}
        res = instruments_collection.insert_one(instrumento)
        instrumento["_id"] = str(res.inserted_id)
        return instrumento

    @staticmethod
    def get_all_instrumentos() -> List[Dict[str, Any]]:
        return [InstrumentoController._to_response(d) for d in instruments_collection.find({})]

    @staticmethod
    def get_instrumento(instrumento_id: str) -> Optional[Dict[str, Any]]:
        try:
            doc = instruments_collection.find_one({"_id": ObjectId(instrumento_id)})
            return InstrumentoController._to_response(doc)
        except Exception:
            raise HTTPException(400, "ID inválido")

    @staticmethod
    def update_instrumento(instrumento_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        try:
            upd = {}
            if "nombre" in data:
                if not data["nombre"]:
                    raise HTTPException(400, "nombre no puede ser vacío")
                upd["nombre"] = data["nombre"]
            if "descripcion" in data:
                upd["descripcion"] = data["descripcion"]
            if not upd:
                raise HTTPException(400, "Nada que actualizar")
            res = instruments_collection.find_one_and_update(
                {"_id": ObjectId(instrumento_id)},
                {"$set": upd},
                return_document=True
            )
            if not res:
                raise HTTPException(404, "Instrumento no encontrado")
            res["_id"] = str(res["_id"])
            return res
        except HTTPException:
            raise
        except Exception:
            raise HTTPException(400, "ID inválido")

    @staticmethod
    def delete_instrumento(instrumento_id: str) -> None:
        try:
            oid = ObjectId(instrumento_id)
        except Exception:
            raise HTTPException(400, "ID inválido")
        ref = sample_instruments.find_one({"instrumento_id": oid})
        if ref:
            raise HTTPException(409, "No se puede eliminar: instrumento referenciado en samples")
        res = instruments_collection.delete_one({"_id": oid})
        if res.deleted_count == 0:
            raise HTTPException(404, "Instrumento no encontrado")

    @staticmethod
    def search_instrumentos(query: Optional[str]) -> List[Dict[str, Any]]:
        filtro = {"nombre": {"$regex": query, "$options": "i"}} if query else {}
        return [InstrumentoController._to_response(d) for d in instruments_collection.find(filtro)]
