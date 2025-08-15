
from fastapi import APIRouter, Depends
from models.comentario import ComentarioCreate
from controllers.comentario_controller import ComentarioController
from utils.security import get_current_user
from typing import List, Dict

router = APIRouter(prefix="/comentarios", tags=["Comentarios"])

@router.post("/", status_code=201)
async def crear_comentario(payload: ComentarioCreate, current_user: dict = Depends(get_current_user)):
    return ComentarioController.crear(payload.texto, current_user["sub"], payload.target_type, payload.target_id)

@router.get("/")
async def listar_comentarios(target_type: str, target_id: str):
    return ComentarioController.listar(target_type, target_id)
