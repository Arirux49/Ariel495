from fastapi import APIRouter, Depends
from controllers.comentario_controller import ComentarioController
from models.comentario import ComentarioCreate, ComentarioResponse
from typing import List
from utils.security import get_current_user

router = APIRouter(prefix="/comentarios", tags=["Comentarios"])

@router.post("/", response_model=ComentarioResponse)
async def crear_comentario(
    contenido_id: str,
    es_sample: bool,
    texto: str,
    current_user: dict = Depends(get_current_user)
):
    return ComentarioController.crear_comentario(
        contenido_id=contenido_id,
        es_sample=es_sample,
        usuario_id=current_user["_id"],
        texto=texto
    )

@router.get("/", response_model=List[ComentarioResponse])
async def obtener_comentarios(contenido_id: str, es_sample: bool):
    return ComentarioController.obtener_comentarios(contenido_id, es_sample)