from .base import ModeloBase, PyObjectId
from pydantic import Field
from datetime import datetime

class ComentarioBase(ModeloBase):
    texto: str = Field(..., min_length=1, max_length=300)
    fecha: datetime = Field(default_factory=datetime.utcnow)

class ComentarioCreate(ComentarioBase):
    usuario_id: PyObjectId
    contenido_id: PyObjectId
    es_sample: bool

class ComentarioDB(ComentarioBase):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    usuario_id: PyObjectId
    contenido_id: PyObjectId
    es_sample: bool

class ComentarioResponse(ComentarioBase):
    id: str = Field(..., alias="_id")
    usuario_id: str
    contenido_id: str