# Importación del enrutador de FastAPI
from fastapi import APIRouter

# Importación del controlador que maneja la lógica relacionada con instrumentos musicales
from controllers.instrumento_controller import InstrumentoController

# Importación de modelos de entrada y salida para validación y tipado
from models.instrumento import InstrumentoCreate, InstrumentoResponse

# Tipado para indicar que se espera una lista de objetos
from typing import List

# Se define el router con prefijo de ruta y categoría para la documentación
router = APIRouter(
    prefix="/instrumentos",
    tags=["Instrumentos"]
)

# Ruta GET para listar todos los instrumentos
@router.get("/", response_model=List[InstrumentoResponse])
async def listar_instrumentos():
    """
    Obtiene una lista de todos los instrumentos registrados en el sistema.

    Retorna una lista de objetos que contienen el nombre y descripción del instrumento.
    """
    return InstrumentoController.get_all_instrumentos()

# Ruta POST para crear un nuevo instrumento
@router.post("/", response_model=InstrumentoResponse)
async def crear_instrumento(instrumento: InstrumentoCreate):
    """
    Crea un nuevo instrumento musical con los datos proporcionados.

    - `instrumento`: objeto que contiene el nombre y opcionalmente la descripción.

    Retorna el instrumento creado incluyendo su ID.
    """
    return InstrumentoController.create_instrumento(instrumento)

# Ruta GET para obtener un instrumento específico por su ID
@router.get("/{instrumento_id}", response_model=InstrumentoResponse)
async def obtener_instrumento(instrumento_id: str):
    """
    Recupera la información de un instrumento específico a partir de su ID.

    - `instrumento_id`: identificador del instrumento (en formato string).

    Retorna el objeto correspondiente al instrumento encontrado.
    """
    return InstrumentoController.get_instrumento(instrumento_id)
