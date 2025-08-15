from fastapi import HTTPException
from typing import List, Dict, Any
from bson import ObjectId
from utils.db import users_collection, user_instruments, instruments_collection

import os
import json
import base64
import logging

import firebase_admin
from firebase_admin import credentials

from dotenv import load_dotenv  # para leer variables desde .env

# Cargar variables de entorno si existe .env
load_dotenv()

# Logger del módulo
logger = logging.getLogger(__name__)


class UsuarioController:
    @staticmethod
    def get_usuario(usuario_id: str) -> Dict[str, Any]:
        try:
            u = users_collection.find_one({"_id": ObjectId(usuario_id)})
            if not u:
                raise HTTPException(404, "Usuario no encontrado")
            u["_id"] = str(u["_id"])
            return u
        except Exception:
            raise HTTPException(400, "ID inválido")

    @staticmethod
    def update_usuario(usuario_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        try:
            res = users_collection.find_one_and_update(
                {"_id": ObjectId(usuario_id)},
                {"$set": data},
                return_document=True
            )
            if not res:
                raise HTTPException(404, "Usuario no encontrado")
            res["_id"] = str(res["_id"])
            return res
        except HTTPException:
            raise
        except Exception:
            raise HTTPException(400, "ID inválido")

    @staticmethod
    def add_instrumentos(usuario_id: str, instrumentos_ids: List[str]) -> Dict[str, int]:
        try:
            uid = ObjectId(usuario_id)
        except Exception:
            raise HTTPException(400, "usuario_id inválido")

        rels = []
        for sid in instrumentos_ids:
            try:
                oid = ObjectId(sid)
            except Exception:
                raise HTTPException(400, f"instrumento_id inválido: {sid}")

            if not instruments_collection.find_one({"_id": oid}):
                raise HTTPException(404, f"Instrumento {sid} no existe")

            rels.append({"usuario_id": uid, "instrumento_id": oid})

        if rels:
            user_instruments.insert_many(rels)

        return {"instrumentos_agregados": len(rels)}


def initialize_firebase():
    """
    Igual a la del maestro:
      - Usa FIREBASE_CREDENTIALS_BASE64 si está definida.
      - Si no, fallback a archivo local secrets/firebase_credentials.json.
      - Idempotente: si ya está inicializado, retorna.
      - Lanza HTTPException 500 con mensaje claro si falla.
    """
    if firebase_admin._apps:
        return

    try:
        firebase_creds_base64 = os.getenv("FIREBASE_CREDENTIALS_BASE64")

        if firebase_creds_base64:
            firebase_creds_json = base64.b64decode(firebase_creds_base64).decode("utf-8")
            firebase_creds = json.loads(firebase_creds_json)
            cred = credentials.Certificate(firebase_creds)
            firebase_admin.initialize_app(cred)
            logger.info("Firebase initialized with environment variable credentials")
        else:
            # Fallback a archivo local (ajusta el nombre si usas otro)
            cred = credentials.Certificate("secrets/firebase_credentials.json")
            firebase_admin.initialize_app(cred)
            logger.info("Firebase initialized with JSON file")

    except Exception as e:
        logger.error(f"Failed to initialize Firebase: {e}")
        raise HTTPException(status_code=500, detail=f"Firebase configuration error: {str(e)}")
