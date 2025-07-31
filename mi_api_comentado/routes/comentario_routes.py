# Importamos APIRouter para definir rutas
from fastapi import APIRouter, Depends

# Importamos el controlador de comentarios y los modelos necesarios
from controllers.comentario_controller import ComentarioController
from models.comentario import ComentarioCreate, ComentarioResponse

# Importamos tipos y función de autenticación
from typing import List
from utils.security import get_current_user

# Creamos el router con prefijo /comentarios y etiqueta "Comentarios" para Swagger
router = APIRouter(
    prefix="/comentarios",
    tags=["Comentarios"]
)

# Ruta POST para crear un nuevo comentario
@router.post("/", response_model=ComentarioResponse)
async def crear_comentario(
    contenido_id: str,               # ID del sample o grabación comentada
    es_sample: bool,                 # Indica si el contenido es un sample (True) o grabación (False)
    texto: str,                      # Contenido del comentario
    current_user: dict = Depends(get_current_user)  # Usuario autenticado (inyectado automáticamente)
):
    """
    Crea un nuevo comentario para un sample o una grabación.

    - `contenido_id`: ID del recurso comentado (sample o grabación)
    - `es_sample`: True si el contenido es un sample, False si es una grabación
    - `texto`: texto del comentario
    - `current_user`: obtenido automáticamente mediante token JWT

    Retorna el comentario creado con su ID.
    """
    return ComentarioController.crear_comentario(
        contenido_id=contenido_id,
        es_sample=es_sample,
        usuario_id=current_user["_id"],
        texto=texto
    )

# Ruta GET para obtener comentarios asociados a un contenido
@router.get("/", response_model=List[ComentarioResponse])
async def obtener_comentarios(contenido_id: str, es_sample: bool):
    """
    Obtiene todos los comentarios para un sample o grabación específico.

    - `contenido_id`: ID del contenido
    - `es_sample`: True si el contenido es un sample, False si es una grabación

    Devuelve una lista de comentarios ordenados por fecha (más recientes primero).
    """
    return ComentarioController.obtener_comentarios(contenido_id, es_sample)
