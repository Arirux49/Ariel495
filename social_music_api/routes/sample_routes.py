
from fastapi import APIRouter, HTTPException, Depends
from typing import List
from controllers.sample_controller import SampleController
from models.sample import SampleCreate, SampleUpdate, SampleResponse
from utils.security import get_current_user

router = APIRouter(prefix="/samples", tags=["Samples"])

@router.post("/", response_model=SampleResponse, status_code=201)
async def crear_sample(data: SampleCreate, user: dict = Depends(get_current_user)):
    return SampleController.create(data.dict(), user["sub"])

@router.get("/", response_model=List[SampleResponse])
async def listar_samples():
    return SampleController.list_all()

@router.get("/{sample_id}", response_model=SampleResponse)
async def obtener_sample(sample_id: str):
    s = SampleController.get_one(sample_id)
    if not s:
        raise HTTPException(404, "Sample no encontrado")
    return s

@router.patch("/{sample_id}", response_model=SampleResponse)
async def actualizar_sample(sample_id: str, data: SampleUpdate, user: dict = Depends(get_current_user)):
    return SampleController.patch(sample_id, data.dict(exclude_unset=True))

@router.delete("/{sample_id}", status_code=204)
async def eliminar_sample(sample_id: str, user: dict = Depends(get_current_user)):
    SampleController.delete(sample_id)
    return None

@router.post("/{sample_id}/instrumentos")
async def agregar_instrumentos_sample(sample_id: str, body: dict, user: dict = Depends(get_current_user)):
    return SampleController.add_instruments(sample_id, body.get("instrumento_ids", []))
