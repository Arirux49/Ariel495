# Importamos la clase base común y el validador personalizado de ObjectId
from .base import ModeloBase, PyObjectId

# Field permite definir validaciones y metadatos para los campos de Pydantic
from pydantic import Field

# Optional permite declarar campos que pueden ser None (opcional)
from typing import Optional

# Clase base para todos los modelos relacionados a Instrumentos
class InstrumentoBase(ModeloBase):
    nombre: str = Field(..., min_length=2, max_length=50)
    # Nombre del instrumento (obligatorio, mínimo 2 y máximo 50 caracteres)

    descripcion: Optional[str] = Field(default=None)
    # Descripción del instrumento (opcional, puede ser None)

# Modelo usado para crear un nuevo instrumento (input del usuario)
class InstrumentoCreate(InstrumentoBase):
    pass  # Hereda todo de InstrumentoBase, no necesita cambios adicionales

# Modelo que representa un instrumento guardado en la base de datos
class InstrumentoDB(InstrumentoBase):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    # ID del instrumento (generado por MongoDB)

# Modelo que se utiliza para enviar respuestas al cliente
# Convierte el ID de ObjectId a string para legibilidad
class InstrumentoResponse(InstrumentoBase):
    id: str = Field(..., alias="_id")
