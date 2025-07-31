# Importación de herramientas de FastAPI necesarias para rutas, validaciones y autenticación
from fastapi import APIRouter, Depends, HTTPException

# Importación del controlador que gestiona la lógica de usuario
from controllers.usuario_controller import UsuarioController

# Importación de modelos para validación de entrada y respuesta de usuario
from models.usuario import UsuarioResponse, UsuarioUpdate

# Función para obtener los datos del usuario autenticado (extraídos del token JWT)
from utils.security import get_current_user

# Definición del enrutador para el módulo de usuarios
router = APIRouter(prefix="/usuarios", tags=["Usuarios"])

# Ruta GET para obtener la información de un usuario específico
@router.get("/{usuario_id}", response_model=UsuarioResponse)
async def obtener_usuario(usuario_id: str):
    """
    Recupera los datos de un usuario a partir de su ID.

    - `usuario_id`: ID del usuario a consultar.

    Retorna los datos del usuario si existe.
    """
    return UsuarioController.get_usuario(usuario_id)

# Ruta PUT para actualizar los datos del usuario autenticado
@router.put("/{usuario_id}", response_model=UsuarioResponse)
async def actualizar_usuario(
    usuario_id: str,
    usuario_data: UsuarioUpdate,                      # Datos a actualizar (nombre y/o perfil artístico)
    current_user: dict = Depends(get_current_user)    # Usuario autenticado a través del token JWT
):
    """
    Actualiza los datos de un usuario, validando que el usuario autenticado coincida con el solicitado.

    - `usuario_id`: ID del usuario a actualizar.
    - `usuario_data`: información que se desea modificar.
    - `current_user`: usuario autenticado (extraído del token JWT).

    Lanza un error 403 si un usuario intenta modificar datos de otro.
    """
    if current_user["_id"] != usuario_id:
        raise HTTPException(403, "No autorizado")  # Solo el propio usuario puede modificar su información

    return UsuarioController.update_usuario(usuario_id, usuario_data)

# Ruta POST para agregar instrumentos al perfil de un usuario
@router.post("/{usuario_id}/instrumentos", response_model=dict)
async def agregar_instrumentos_usuario(
    usuario_id: str,
    instrumentos_ids: list[str],                      # Lista de IDs de instrumentos a vincular al usuario
    current_user: dict = Depends(get_current_user)    # Usuario autenticado
):
    """
    Asocia uno o varios instrumentos musicales a un usuario.

    - `usuario_id`: ID del usuario al cual se asociarán los instrumentos.
    - `instrumentos_ids`: lista de IDs de instrumentos a vincular.
    - `current_user`: usuario autenticado.

    Lanza un error 403 si un usuario intenta modificar la información de otro.
    """
    if current_user["_id"] != usuario_id:
        raise HTTPException(403, "No autorizado")  # Restringe acceso a modificación de datos propios

    return UsuarioController.add_instrumentos_usuario(usuario_id, instrumentos_ids)
