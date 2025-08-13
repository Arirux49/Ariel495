
from fastapi import APIRouter, Depends
from typing import List, Dict
from controllers.grabacion_controller import GrabacionController
from utils.security import get_current_user

router = APIRouter(prefix="/grabaciones", tags=["Grabaciones"])

@router.post("/", status_code=201)
async def crear_grabacion(data: Dict, user: dict = Depends(get_current_user)):
    return GrabacionController.crear(data, user["sub"])

@router.patch("/{grabacion_id}/samples")
async def agregar_samples(grabacion_id: str, body: Dict[str, List[str]], user: dict = Depends(get_current_user)):
    return GrabacionController.agregar_samples(grabacion_id, body.get("sample_ids", []))
