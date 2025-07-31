# Importa la clase base y PyObjectId personalizada para manejo de IDs de MongoDB
from .base import ModeloBase, PyObjectId

# Importa Field para definir restricciones y metadatos en los campos de los modelos
from pydantic import Field

# Importa datetime para manejar fechas
from datetime import datetime

# Clase base para modelos de comentario
class ComentarioBase(ModeloBase):
    # Campo obligatorio de texto, con longitud mínima 1 y máxima 300 caracteres
    texto: str = Field(..., min_length=1, max_length=300)

    # Campo de fecha con valor por defecto: la fecha y hora actual (UTC)
    fecha: datetime = Field(default_factory=datetime.utcnow)

# Modelo usado al crear un nuevo comentario (desde el cliente)
class ComentarioCreate(ComentarioBase):
    usuario_id: PyObjectId  # ID del usuario que hace el comentario (ObjectId)
    contenido_id: PyObjectId  # ID del recurso comentado (sample o grabación)
    es_sample: bool  # Indica si el comentario es sobre un sample (True) o una grabación (False)

# Modelo que representa un comentario tal como se guarda en la base de datos
class ComentarioDB(ComentarioBase):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")  # ID de MongoDB, mapeado al campo _id
    usuario_id: PyObjectId  # Referencia al usuario que lo creó
    contenido_id: PyObjectId  # Referencia al sample o grabación comentado
    es_sample: bool  # Tipo de contenido (sample o grabación)

# Modelo para devolver al cliente (con IDs convertidos a string para facilitar la lectura)
class ComentarioResponse(ComentarioBase):
    id: str = Field(..., alias="_id")  # El campo _id se muestra como id (tipo string)
    usuario_id: str  # ID del usuario en formato string
    contenido_id: str  # ID del contenido en formato string
