# Importamos APIRouter para definir rutas específicas para autenticación
from fastapi import APIRouter

# Importamos el controlador de autenticación y los modelos de entrada
from controllers.auth_controller import AuthController, UserRegister, UserLogin

# Creamos un router con prefijo "/auth" y lo agrupamos bajo la etiqueta "Autenticación"
router = APIRouter(
    prefix="/auth",             # Todas las rutas comenzarán con /auth (por ejemplo, /auth/registro)
    tags=["Autenticación"]      # Categoría para documentación (Swagger)
)

# Ruta POST para registrar un nuevo usuario
@router.post("/registro", status_code=201)
async def register(user: UserRegister):
    """
    Registro de usuario nuevo.

    Recibe un objeto tipo UserRegister que incluye:
    - email: correo electrónico del usuario
    - password: contraseña
    - nombre: nombre del usuario
    - perfil_artista (opcional): descripción artística
    
    Devuelve un diccionario con los datos registrados.
    """
    return await AuthController.register_user(user.dict())

# Ruta POST para iniciar sesión
@router.post("/login")
async def login(user: UserLogin):
    """
    Inicio de sesión de usuario.

    Recibe un objeto tipo UserLogin que incluye:
    - email: correo electrónico
    - password: contraseña
    
    Devuelve un token de acceso JWT válido y el UID del usuario si las credenciales son correctas.
    """
    return await AuthController.login_user(user.dict())
