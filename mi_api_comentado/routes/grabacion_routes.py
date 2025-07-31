# Importaciones necesarias de FastAPI y dependencias
from fastapi import APIRouter, Depends

# Importamos el controlador que maneja la lógica de grabaciones
from controllers.grabacion_controller import GrabacionController

# Importamos los modelos de entrada y salida para grabaciones
from models.grabacion import GrabacionCreate, GrabacionResponse

# Tipado para indicar que se retorna una lista
from typing import List

# Función para obtener el usuario autenticado mediante JWT
from utils.security import get_current_user

# Creamos el router para las rutas relacionadas a grabaciones
router = APIRouter(
    prefix="/grabaciones",
    tags=["Grabaciones"]
)

# Ruta GET para obtener grabaciones populares
@router.get("/populares", response_model=List[dict])
async def grabaciones_populares():
    """
    Devuelve una lista de grabaciones populares.
    Estas grabaciones son aquellas que utilizan un mayor número de samples.

    No requiere autenticación.
    """
    return GrabacionController.get_popular_recordings()

# Ruta POST para crear una nueva grabación
@router.post("/", response_model=GrabacionResponse)
async def crear_grabacion(
    grabacion_data: GrabacionCreate,             # Datos de la grabación (nombre, duración, samples, etc.)
    current_user: dict = Depends(get_current_user)  # Usuario autenticado extraído del token JWT
):
    """
    Crea una nueva grabación asociada al usuario autenticado.

    - `grabacion_data`: contiene los datos necesarios para crear la grabación.
    - `current_user`: información del usuario que realiza la solicitud.

    Retorna los datos de la grabación creada.
    """
    return GrabacionController.create_grabacion(grabacion_data, current_user["_id"])
