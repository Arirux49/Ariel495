# Importa la biblioteca Pyrebase, que permite interactuar con Firebase desde Python
import pyrebase

# Importa HTTPException para manejar errores HTTP personalizados en FastAPI
from fastapi import HTTPException

# Diccionario de configuración con las credenciales y endpoints necesarios para conectar a Firebase
# Estas credenciales fueron generadas en la consola de Firebase para el proyecto
config = {
    "apiKey": "AIzaSyD3Qq_MJn7W-Gs5K-nBTlRnnU90rPSGbuU",  # Clave API pública para autenticar peticiones
    "authDomain": "cluster0.vcs8lnn.firebaseapp.com",     # Dominio de autenticación del proyecto
    "projectId": "cluster0",                              # ID del proyecto en Firebase
    "storageBucket": "cluster0.vcs8lnn.appspot.com",      # URL del bucket de almacenamiento
    "databaseURL": ""                                     # (Vacío porque no se usa Realtime Database)
}

# Inicializa la conexión con Firebase usando la configuración anterior
firebase = pyrebase.initialize_app(config)

# Obtiene el módulo de autenticación de Firebase, que se usará para registrar e iniciar sesión usuarios
auth = firebase.auth()

# Función que verifica si un token de autenticación (id_token) es válido y extrae el UID del usuario
def verify_firebase_token(id_token: str) -> str:
    try:
        # Intenta obtener la información de la cuenta usando el token proporcionado
        user = auth.get_account_info(id_token)
        
        # Devuelve el UID (identificador único del usuario en Firebase) del primer usuario encontrado
        return user["users"][0]["localId"]
    except Exception as e:
        # Si el token no es válido, lanza una excepción HTTP con código 401 (no autorizado)
        raise HTTPException(status_code=401, detail=f"Token inválido: {str(e)}")
