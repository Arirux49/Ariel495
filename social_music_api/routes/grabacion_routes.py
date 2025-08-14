from fastapi import APIRouter, Body, Depends, HTTPException
from typing import Dict, Any, List
from controllers.grabacion_controller import GrabacionController
from utils.security import get_current_user

router = APIRouter(prefix="/grabaciones", tags=["Grabaciones"])

@router.post("/")
async def crear_grabacion(
    body: Dict[str, Any] = Body(...),
    _user=Depends(get_current_user)
):
    nombre = body.get("nombre") or body.get("titulo")
    if not nombre or len(nombre) < 2:
        raise HTTPException(422, "nombre/titulo es requerido y debe tener al menos 2 caracteres.")
    data = {"nombre": nombre, "descripcion": body.get("descripcion", "")}
    return GrabacionController.crear(data)

@router.patch("/{grabacion_id}/samples")
async def agregar_samples(
    grabacion_id: str,
    body: Dict[str, Any] = Body(...),
    _user=Depends(get_current_user)
):
    sample_ids: List[str] = body.get("sample_ids") or body.get("samples") or []
    if not isinstance(sample_ids, list):
        raise HTTPException(400, "sample_ids/samples debe ser una lista de IDs.")
    return GrabacionController.agregar_samples(grabacion_id, sample_ids)
