
from fastapi import APIRouter, Depends, HTTPException
from controllers.usuario_controller import UsuarioController
from models.usuario import UsuarioResponse, UsuarioUpdate
from utils.security import get_current_user
from typing import List

router = APIRouter(prefix="/usuarios", tags=["Usuarios"])

@router.get("/{usuario_id}", response_model=UsuarioResponse)
async def obtener_usuario(usuario_id: str):
    return UsuarioController.get_usuario(usuario_id)

@router.put("/{usuario_id}", response_model=UsuarioResponse)
async def actualizar_usuario(usuario_id: str, usuario_data: UsuarioUpdate, current_user: dict = Depends(get_current_user)):
    if current_user["sub"] != usuario_id:
        raise HTTPException(403, "No autorizado")
    return UsuarioController.update_usuario(usuario_id, usuario_data.dict(exclude_unset=True))

@router.post("/{usuario_id}/instrumentos", response_model=dict)
async def agregar_instrumentos_usuario(usuario_id: str, instrumentos_ids: List[str], current_user: dict = Depends(get_current_user)):
    if current_user["sub"] != usuario_id:
        raise HTTPException(403, "No autorizado")
    return UsuarioController.add_instrumentos(usuario_id, instrumentos_ids)
