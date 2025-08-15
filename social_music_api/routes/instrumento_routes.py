from fastapi import APIRouter, Query
from typing import Optional, Dict, Any
from controllers.instrumento_controller import (
    list_instrumentos, create_instrumento, update_instrumento, delete_instrumento
)

router = APIRouter(prefix="/instrumentos", tags=["Instrumentos"])

@router.get("")
async def list_all(q: Optional[str] = Query(None)):
    return await list_instrumentos(q)

@router.post("")
async def create(payload: Dict[str, Any]):
    return await create_instrumento(payload)

@router.put("/{instrumento_id}")
async def update(instrumento_id: str, payload: Dict[str, Any]):
    return await update_instrumento(instrumento_id, payload)

@router.delete("/{instrumento_id}")
async def remove(instrumento_id: str):
    return await delete_instrumento(instrumento_id)
