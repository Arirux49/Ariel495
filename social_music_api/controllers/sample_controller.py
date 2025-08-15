# controllers/sample_controller.py
from fastapi import HTTPException
from typing import Dict, Any, List, Optional
from bson import ObjectId
from uuid import uuid4
import random

from pymongo import ReturnDocument

from utils.db import (
    samples_collection,
    sample_instruments,
    instruments_collection,
)

_EXTS = ["mp3", "wav", "ogg", "flac"]


def _rand_file() -> str:
    """Genera un nombre de archivo 'fake' con extensión válida."""
    return f"sample_{uuid4().hex}.{random.choice(_EXTS)}"


class SampleController:

    @staticmethod
    def list_comments(sample_id: str) -> List[Dict[str, Any]]:
        try:
            sid = ObjectId(sample_id)
        except Exception:
            raise HTTPException(400, "sample_id inválido")
        out = []
        for c in comments_collection.find({"target_type": "sample", "target_id": sid}).sort("fecha", 1):
            c["_id"] = str(c["_id"])
            c["target_id"] = str(c["target_id"])
            if c.get("user_id"):
                c["user_id"] = str(c["user_id"])
            out.append(c)
        return out

    @staticmethod
    def add_comment(sample_id: str, texto: str, user_id: str) -> Dict[str, Any]:
        if not texto or not texto.strip():
            raise HTTPException(422, "texto es requerido")
        try:
            sid = ObjectId(sample_id)
        except Exception:
            raise HTTPException(400, "sample_id inválido")
        if not samples_collection.find_one({"_id": sid}):
            raise HTTPException(404, "Sample no encontrado")
        doc = {
            "texto": texto.strip(),
            "user_id": ObjectId(user_id) if ObjectId.is_valid(user_id) else None,
            "target_type": "sample",
            "target_id": sid,
            "fecha": datetime.utcnow(),
        }
        res = comments_collection.insert_one(doc)
        doc["_id"] = str(res.inserted_id)
        doc["target_id"] = str(sid)
        if doc["user_id"]:
            doc["user_id"] = str(doc["user_id"])
        return doc

    @staticmethod
    def delete_comment(sample_id: str, comentario_id: str) -> None:
        try:
            cid = ObjectId(comentario_id)
        except Exception:
            raise HTTPException(400, "comentario_id inválido")
        res = comments_collection.delete_one({"_id": cid, "target_type": "sample"})
        if res.deleted_count == 0:
            raise HTTPException(404, "Comentario no encontrado")
    @staticmethod
    def _to_response(doc: Dict[str, Any]) -> Dict[str, Any]:
        if not doc:
            return None
        doc["_id"] = str(doc["_id"])
        if doc.get("usuario_creador"):
            doc["usuario_creador"] = str(doc["usuario_creador"])
        return doc

    @staticmethod
    def create(data: Dict[str, Any], usuario_id: str) -> Dict[str, Any]:
        if not data.get("nombre"):
            raise HTTPException(400, "nombre es requerido")

        # Validar/convertir usuario_id
        try:
            uid = ObjectId(usuario_id)
        except Exception:
            raise HTTPException(400, "usuario_id inválido")

        # Defaults pedidos: archivo aleatorio + duración 15
        archivo = data.get("archivo") or _rand_file()
        duracion = data.get("duracion")
        if duracion is None:
            duracion = 15

        doc = {
            "nombre": data["nombre"],
            "descripcion": data.get("descripcion"),
            "usuario_creador": uid,
            "archivo": archivo,
            "duracion": duracion,
        }

        res = samples_collection.insert_one(doc)
        doc["_id"] = str(res.inserted_id)
        return doc

    @staticmethod
    def list_all() -> List[Dict[str, Any]]:
        return [SampleController._to_response(d) for d in samples_collection.find({})]

    @staticmethod
    def get_one(sample_id: str) -> Optional[Dict[str, Any]]:
        try:
            d = samples_collection.find_one({"_id": ObjectId(sample_id)})
            return SampleController._to_response(d)
        except Exception:
            raise HTTPException(400, "ID inválido")

    @staticmethod
    def patch(sample_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        if not data:
            raise HTTPException(400, "Nada que actualizar")
        try:
            res = samples_collection.find_one_and_update(
                {"_id": ObjectId(sample_id)},
                {"$set": data},
                return_document=ReturnDocument.AFTER,
            )
            if not res:
                raise HTTPException(404, "Sample no encontrado")
            return SampleController._to_response(res)
        except HTTPException:
            raise
        except Exception:
            raise HTTPException(400, "ID inválido")

    @staticmethod
    def delete(sample_id: str) -> None:
        try:
            res = samples_collection.delete_one({"_id": ObjectId(sample_id)})
            if res.deleted_count == 0:
                raise HTTPException(404, "Sample no encontrado")
        except HTTPException:
            raise
        except Exception:
            raise HTTPException(400, "ID inválido")

    @staticmethod
    def add_instruments(sample_id: str, instrumentos_ids: List[str]) -> Dict[str, int]:
        # Validar sample
        try:
            sid = ObjectId(sample_id)
        except Exception:
            raise HTTPException(400, "sample_id inválido")

        if not samples_collection.find_one({"_id": sid}):
            raise HTTPException(404, "Sample no existe")

        inserted = 0
        ya_existian = 0

        for inst in instrumentos_ids:
            try:
                iid = ObjectId(inst)
            except Exception:
                raise HTTPException(400, f"instrumento_id inválido: {inst}")

            if not instruments_collection.find_one({"_id": iid}):
                raise HTTPException(404, f"Instrumento no existe: {inst}")

          
            exists = sample_instruments.find_one(
                {"sample_id": sid, "instrumento_id": iid}
            )
            if exists:
                ya_existian += 1
                continue

            sample_instruments.insert_one({"sample_id": sid, "instrumento_id": iid})
            inserted += 1

        return {"instrumentos_agregados": inserted, "ya_existian": ya_existian}

from typing import Any, Dict, List
from fastapi import HTTPException
from bson import ObjectId
from datetime import datetime
from utils.db import comments_collection, samples_collection
