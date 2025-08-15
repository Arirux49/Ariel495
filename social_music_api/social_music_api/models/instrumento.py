
from pydantic import BaseModel, Field
from typing import Optional

class InstrumentoCreate(BaseModel):
    nombre: str = Field(..., min_length=2, max_length=80)
    descripcion: Optional[str] = None

class InstrumentoResponse(BaseModel):
    _id: str = Field(..., alias="_id")
    nombre: str
    descripcion: Optional[str] = None
    class Config:
        allow_population_by_field_name = True
