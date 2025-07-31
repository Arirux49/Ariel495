# Importamos la clase base y el validador personalizado de ObjectId para MongoDB
from .base import ModeloBase, PyObjectId

# Importamos Field para definir metadatos y restricciones en los campos
# HttpUrl para validar URLs
from pydantic import Field, HttpUrl

# Importamos List para campos de listas
from typing import List

# timedelta se usa para representar la duración de la grabación
from datetime import timedelta

# Clase base que contiene los campos comunes a todos los modelos de grabaciones
class GrabacionBase(ModeloBase):
    nombre: str = Field(..., max_length=100)  # Nombre de la grabación (obligatorio, máx. 100 caracteres)
    descripcion: str = Field(default="", max_length=500)  # Descripción opcional (máx. 500 caracteres)
    duracion: timedelta  # Duración total de la grabación (formato timedelta)
    samples_utilizados: List[PyObjectId] = Field(default_factory=list)
    # Lista de IDs de samples que se usaron para crear la grabación

# Modelo usado para crear una nueva grabación (input del usuario)
class GrabacionCreate(GrabacionBase):
    usuario_creador: PyObjectId  # ID del usuario que creó la grabación

# Modelo que representa cómo se guarda una grabación en la base de datos
class GrabacionDB(GrabacionBase):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")  # ID de MongoDB
    usuario_creador: PyObjectId  # ID del usuario creador (referencia a la colección usuarios)
    archivo_url: HttpUrl  # URL del archivo de audio (válido como URL)

# Modelo de salida (respuesta al cliente), con IDs convertidos a string para mejor legibilidad
class GrabacionResponse(GrabacionBase):
    id: str = Field(..., alias="_id")  # ID como string
    usuario_creador: str  # ID del creador como string
