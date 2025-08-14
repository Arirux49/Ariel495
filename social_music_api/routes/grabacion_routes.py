from fastapi import APIRouter, HTTPException, Path, Depends, status
from typing import List, Any, Dict
from controllers.grabacion_controller import (
    create_grabacion as controller_create_grabacion,
    add_samples_to_grabacion as controller_add_samples_to_grabacion,
    list_grabaciones as controller_list_grabaciones,
    get_grabacion as controller_get_grabacion,
    delete_grabacion as controller_delete_grabacion,
)
from utils.auth_dependency import validate_user

router = APIRouter(prefix="/grabaciones", tags=["Grabaciones"])

@router.post("/", summary="Crear Grabacion")
@validate_user
async def create_grabacion(payload: Dict[str, Any]):
    return await controller_create_grabacion(payload)

@router.patch("/{grabacion_id}/samples", summary="Agregar Samples")
@validate_user
async def add_samples(grabacion_id: str, payload: Dict[str, Any]):
    sample_ids = payload.get("sample_ids", [])
    return await controller_add_samples_to_grabacion(grabacion_id, sample_ids)

@router.get("/", summary="Listar Grabaciones")
@validate_user
async def list_grabaciones():
    return await controller_list_grabaciones()

@router.get("/{grabacion_id}", summary="Obtener Grabacion")
@validate_user
async def get_grabacion(grabacion_id: str):
    result = await controller_get_grabacion(grabacion_id)
    if not result:
        raise HTTPException(status_code=404, detail="Grabación no encontrada")
    return result

@router.delete("/{grabacion_id}", summary="Eliminar Grabacion", status_code=status.HTTP_204_NO_CONTENT)
@validate_user
async def delete_grabacion(grabacion_id: str):
    await controller_delete_grabacion(grabacion_id)
    return None
