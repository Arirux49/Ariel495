from fastapi import APIRouter, Depends
from controllers.grabacion_controller import GrabacionController
from models.grabacion import GrabacionCreate, GrabacionResponse
from typing import List
from utils.security import get_current_user

router = APIRouter(prefix="/grabaciones", tags=["Grabaciones"])

@router.get("/populares", response_model=List[dict])
async def grabaciones_populares():
    return GrabacionController.get_popular_recordings()

@router.post("/", response_model=GrabacionResponse)
async def crear_grabacion(
    grabacion_data: GrabacionCreate,
    current_user: dict = Depends(get_current_user)
):
    return GrabacionController.create_grabacion(grabacion_data, current_user["_id"])