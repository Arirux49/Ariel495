
from fastapi import HTTPException
from typing import Dict, Any, List
from bson import ObjectId
from datetime import datetime
from utils.db import comments_collection, users_collection, samples_collection, recordings_collection

class ComentarioController:
    @staticmethod
    def crear(texto: str, user_id: str, target_type: str, target_id: str) -> Dict[str, Any]:
        if not users_collection.find_one({"_id": ObjectId(user_id)}):
            raise HTTPException(404, "Usuario no existe")
        if target_type == "sample":
            if not samples_collection.find_one({"_id": ObjectId(target_id)}):
                raise HTTPException(404, "Sample no existe")
        elif target_type == "recording":
            if not recordings_collection.find_one({"_id": ObjectId(target_id)}):
                raise HTTPException(404, "Grabación no existe")
        else:
            raise HTTPException(400, "target_type inválido")
        doc = {
            "texto": texto,
            "user_id": ObjectId(user_id),
            "target_type": target_type,
            "target_id": ObjectId(target_id),
            "fecha": datetime.utcnow().isoformat()
        }
        res = comments_collection.insert_one(doc)
        doc["_id"] = str(res.inserted_id)
        doc["user_id"] = str(doc["user_id"])
        doc["target_id"] = str(doc["target_id"])
        return doc

    @staticmethod
    def listar(target_type: str, target_id: str) -> List[Dict[str, Any]]:
        cur = comments_collection.find({"target_type": target_type, "target_id": ObjectId(target_id)})
        out = []
        for d in cur:
            d["_id"] = str(d["_id"]); d["user_id"] = str(d["user_id"]); d["target_id"] = str(d["target_id"])
            out.append(d)
        return out
