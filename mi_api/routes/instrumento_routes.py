from fastapi import APIRouter
from controllers.instrumento_controller import InstrumentoController
from models.instrumento import InstrumentoCreate, InstrumentoResponse
from typing import List

router = APIRouter(prefix="/instrumentos", tags=["Instrumentos"])

@router.get("/", response_model=List[InstrumentoResponse])
async def listar_instrumentos():
    return InstrumentoController.get_all_instrumentos()

@router.post("/", response_model=InstrumentoResponse)
async def crear_instrumento(instrumento: InstrumentoCreate):
    return InstrumentoController.create_instrumento(instrumento)

@router.get("/{instrumento_id}", response_model=InstrumentoResponse)
async def obtener_instrumento(instrumento_id: str):
    return InstrumentoController.get_instrumento(instrumento_id)