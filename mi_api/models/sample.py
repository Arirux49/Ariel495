from .base import ModeloBase, PyObjectId
from pydantic import Field, HttpUrl
from typing import List
from datetime import timedelta

class SampleBase(ModeloBase):
    nombre: str = Field(..., max_length=100)
    descripcion: str = Field(default="", max_length=500)
    duracion: timedelta
    instrumentos: List[PyObjectId] = Field(default_factory=list)

class SampleCreate(SampleBase):
    usuario_creador: PyObjectId

class SampleDB(SampleBase):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    usuario_creador: PyObjectId
    archivo_url: HttpUrl

class SampleResponse(SampleBase):
    id: str = Field(..., alias="_id")
    usuario_creador: str