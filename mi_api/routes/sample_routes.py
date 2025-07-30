from fastapi import APIRouter, UploadFile, Depends
from controllers.sample_controller import SampleController
from models.sample import SampleCreate, SampleResponse
from typing import List
from utils.security import get_current_user

router = APIRouter(prefix="/samples", tags=["Samples"])

@router.post("/", response_model=SampleResponse)
async def crear_sample(
    sample_data: SampleCreate,
    audio_file: UploadFile,
    current_user: dict = Depends(get_current_user)
):
    return await SampleController.create_sample(sample_data, audio_file, current_user["_id"])

@router.get("/por-instrumento/{instrumento_id}", response_model=List[SampleResponse])
async def samples_por_instrumento(instrumento_id: str):
    return SampleController.get_samples_by_instrument(instrumento_id)