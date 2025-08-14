from fastapi import APIRouter
from controllers.sample_controller import (
    list_samples, create_sample, update_sample, delete_sample
)

router = APIRouter(prefix="/samples", tags=["Samples"])

@router.get("")
async def list_all():
    return await list_samples()

@router.post("")
async def create(payload: dict):
    return await create_sample(payload)

@router.put("/{sample_id}")
async def update(sample_id: str, payload: dict):
    return await update_sample(sample_id, payload)

@router.delete("/{sample_id}")
async def remove(sample_id: str):
    return await delete_sample(sample_id)
