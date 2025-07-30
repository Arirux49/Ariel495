from .base import ModeloBase, PyObjectId
from pydantic import Field
from typing import Optional

class InstrumentoBase(ModeloBase):
    nombre: str = Field(..., min_length=2, max_length=50)
    descripcion: Optional[str] = Field(default=None)

class InstrumentoCreate(InstrumentoBase):
    pass

class InstrumentoDB(InstrumentoBase):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")

class InstrumentoResponse(InstrumentoBase):
    id: str = Field(..., alias="_id")