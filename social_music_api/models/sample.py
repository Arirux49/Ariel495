
from pydantic import BaseModel, Field
from typing import Optional

class SampleCreate(BaseModel):
    nombre: str = Field(..., min_length=2, max_length=80)
    descripcion: Optional[str] = None
    archivo: Optional[str] = None
    duracion: Optional[int] = Field(default=None, ge=0)

class SampleUpdate(BaseModel):
    nombre: Optional[str] = Field(default=None, min_length=2, max_length=80)
    descripcion: Optional[str] = None
    archivo: Optional[str] = None
    duracion: Optional[int] = Field(default=None, ge=0)

class SampleResponse(BaseModel):
    _id: str = Field(..., alias="_id")
    nombre: str
    descripcion: Optional[str] = None
    archivo: Optional[str] = None
    duracion: Optional[int] = None
    usuario_creador: Optional[str] = None
    class Config:
        allow_population_by_field_name = True
