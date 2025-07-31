# Importamos la clase base del modelo y el validador personalizado para ObjectId
from .base import ModeloBase, PyObjectId

# Field para definir validaciones y metadatos; HttpUrl para URLs válidas
from pydantic import Field, HttpUrl

# List se usa para definir listas tipadas
from typing import List

# timedelta representa duración de tiempo (usada para duración del audio)
from datetime import timedelta


# Clase base para todos los modelos relacionados con samples
class SampleBase(ModeloBase):
    nombre: str = Field(..., max_length=100)
    # Nombre del sample, obligatorio, máximo 100 caracteres

    descripcion: str = Field(default="", max_length=500)
    # Descripción del sample, por defecto una cadena vacía, máximo 500 caracteres

    duracion: timedelta
    # Duración del sample (en tiempo), es un campo obligatorio

    instrumentos: List[PyObjectId] = Field(default_factory=list)
    # Lista de IDs de instrumentos asociados al sample (relación muchos a muchos)


# Modelo utilizado al crear un nuevo sample (entrada del usuario)
class SampleCreate(SampleBase):
    usuario_creador: PyObjectId
    # ID del usuario que creó el sample


# Modelo para representar un sample almacenado en la base de datos
class SampleDB(SampleBase):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    # ID único del documento en MongoDB

    usuario_creador: PyObjectId
    # ID del creador, tipo ObjectId (relación con usuario)

    archivo_url: HttpUrl
    # URL del archivo de audio almacenado (en Firebase u otro servicio)


# Modelo que se devuelve al cliente como respuesta, con IDs como strings
class SampleResponse(SampleBase):
    id: str = Field(..., alias="_id")
    # ID convertido a string para facilitar su uso en el frontend

    usuario_creador: str
    # ID del creador como string
