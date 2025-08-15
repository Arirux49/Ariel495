
from fastapi import APIRouter, HTTPException, Depends, Query
from typing import List, Optional
from controllers.instrumento_controller import InstrumentoController
from models.instrumento import InstrumentoCreate, InstrumentoResponse
from utils.security import get_current_user

router = APIRouter(prefix="/instrumentos", tags=["Instrumentos"])

@router.post("/", response_model=InstrumentoResponse, status_code=201)
async def crear_instrumento(data: InstrumentoCreate, user: dict = Depends(get_current_user)):
    return InstrumentoController.create_instrumento(data.dict())

@router.get("/", response_model=List[InstrumentoResponse])
async def listar_instrumentos():
    return InstrumentoController.get_all_instrumentos()

@router.get("/search", response_model=List[InstrumentoResponse])
async def buscar_instrumentos(q: Optional[str] = Query(default=None, min_length=1)):
    return InstrumentoController.search_instrumentos(q)

@router.get("/{instrumento_id}", response_model=InstrumentoResponse)
async def obtener_instrumento(instrumento_id: str):
    inst = InstrumentoController.get_instrumento(instrumento_id)
    if not inst:
        raise HTTPException(404, "Instrumento no encontrado")
    return inst

@router.put("/{instrumento_id}", response_model=InstrumentoResponse)
async def actualizar_instrumento(instrumento_id: str, data: InstrumentoCreate, user: dict = Depends(get_current_user)):
    return InstrumentoController.update_instrumento(instrumento_id, data.dict())

@router.delete("/{instrumento_id}", status_code=204)
async def eliminar_instrumento(instrumento_id: str, user: dict = Depends(get_current_user)):
    InstrumentoController.delete_instrumento(instrumento_id)
    return None
