# Importa la librería 'jwt' para codificar y decodificar tokens JWT
import jwt

# Importa módulos para manejar fechas y tiempos
from datetime import datetime, timedelta

# Importa clases de FastAPI para lanzar errores HTTP y manejar dependencias
from fastapi import HTTPException, Depends

# Importa clases de seguridad para autenticar peticiones HTTP
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

# Clave secreta que se utiliza para firmar y verificar los tokens JWT
# IMPORTANTE: En producción debe estar oculta (por ejemplo, en variables de entorno)
SECRET_KEY = "quesoconmusica123"

# Algoritmo que se usará para firmar el JWT. HS256 es un algoritmo simétrico seguro
ALGORITHM = "HS256"

# Función que crea un token JWT a partir del UID (identificador del usuario)
def create_access_token(uid: str) -> str:
    # Crea el "payload" del token, que contiene:
    # - "sub": Subject o identificador del usuario
    # - "exp": Fecha de expiración (30 minutos desde la creación)
    payload = {
        "sub": uid,
        "exp": datetime.utcnow() + timedelta(minutes=30)
    }
    # Codifica el token JWT usando la clave secreta y el algoritmo especificado
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

# Función que decodifica un token JWT y retorna el contenido del payload
def decode_token(token: str) -> dict:
    try:
        # Intenta decodificar el token, verificando firma y expiración
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except jwt.ExpiredSignatureError:
        # Si el token ha expirado, se lanza un error HTTP 401 (no autorizado)
        raise HTTPException(status_code=401, detail="Token expirado")
    except jwt.InvalidTokenError:
        # Si el token es inválido, también se lanza error 401
        raise HTTPException(status_code=401, detail="Token inválido")

# Middleware de seguridad que espera un token en la cabecera Authorization (formato Bearer)
security = HTTPBearer()

# Dependencia que se usa en las rutas protegidas para obtener el usuario autenticado
def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> dict:
    # Extrae el token desde las credenciales HTTP
    token = credentials.credentials

    # Decodifica el token y devuelve el payload (con el UID del usuario autenticado)
    return decode_token(token)
