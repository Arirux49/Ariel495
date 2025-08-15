from .base import ModeloBase, PyObjectId
from pydantic import Field, HttpUrl
from typing import List
from datetime import timedelta

class GrabacionBase(ModeloBase):
    nombre: str = Field(..., max_length=100)
    descripcion: str = Field(default="", max_length=500)
    duracion: timedelta
    samples_utilizados: List[PyObjectId] = Field(default_factory=list)

class GrabacionCreate(GrabacionBase):
    usuario_creador: PyObjectId

class GrabacionDB(GrabacionBase):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    usuario_creador: PyObjectId
    archivo_url: HttpUrl

class GrabacionResponse(GrabacionBase):
    id: str = Field(..., alias="_id")
    usuario_creador: str