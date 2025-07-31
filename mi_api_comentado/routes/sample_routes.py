# Importación de herramientas de FastAPI necesarias para rutas, subida de archivos y autenticación
from fastapi import APIRouter, UploadFile, Depends

# Importación del controlador que contiene la lógica de negocio para los samples
from controllers.sample_controller import SampleController

# Importación de modelos de entrada y salida para validación y respuesta
from models.sample import SampleCreate, SampleResponse

# Importación para definir tipos de respuesta como listas
from typing import List

# Función que recupera el usuario autenticado a través del token JWT
from utils.security import get_current_user

# Definición del enrutador con prefijo y etiqueta para organización en Swagger
router = APIRouter(prefix="/samples", tags=["Samples"])

# Ruta POST para crear un nuevo sample (archivo de audio)
@router.post("/", response_model=SampleResponse)
async def crear_sample(
    sample_data: SampleCreate,              # Datos del sample (nombre, duración, instrumentos, etc.)
    audio_file: UploadFile,                 # Archivo de audio enviado por el usuario
    current_user: dict = Depends(get_current_user)  # Usuario autenticado (se obtiene desde el JWT)
):
    """
    Crea un nuevo sample y lo asocia a uno o más instrumentos musicales.

    - `sample_data`: información básica del sample, como nombre, duración e instrumentos asociados.
    - `audio_file`: archivo de audio que se subirá y almacenará en el servidor o nube.
    - `current_user`: usuario autenticado que está creando el sample.

    Retorna el sample creado con su ID y metadatos.
    """
    return await SampleController.create_sample(sample_data, audio_file, current_user["_id"])

# Ruta GET para obtener todos los samples asociados a un instrumento específico
@router.get("/por-instrumento/{instrumento_id}", response_model=List[SampleResponse])
async def samples_por_instrumento(instrumento_id: str):
    """
    Recupera todos los samples que están asociados a un instrumento musical específico.

    - `instrumento_id`: ID del instrumento del cual se quieren consultar los samples relacionados.

    Retorna una lista de samples que utilizan ese instrumento.
    """
    return SampleController.get_samples_by_instrument(instrumento_id)
