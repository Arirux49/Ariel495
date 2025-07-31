# Módulo del sistema operativo (OS), en este caso no se usa directamente, pero común en contextos de rutas y entornos
import os

# Importamos datetime para generar marcas de tiempo únicas
from datetime import datetime

# Importamos herramientas de FastAPI para manejo de archivos y errores HTTP
from fastapi import HTTPException, UploadFile

# Importamos la instancia de Firebase previamente configurada
from utils.firebase import firebase

# Inicializamos el acceso al servicio de almacenamiento de Firebase
storage = firebase.storage()

# Función asincrónica que sube un archivo de audio a Firebase Storage
async def upload_audio(file: UploadFile, user_id: str) -> str:
    """
    Sube un archivo de audio a Firebase Storage con un nombre único y devuelve la URL pública.

    Args:
        file (UploadFile): El archivo a subir.
        user_id (str): ID del usuario que sube el archivo, usado para organizar carpetas.

    Returns:
        str: URL pública del archivo subido.

    Raises:
        HTTPException: Si ocurre un error durante la subida del archivo.
    """
    try:
        # Generamos un timestamp para asegurarnos de que el nombre del archivo sea único
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        # Construimos la ruta del archivo en Firebase: audios/{user_id}/YYYYMMDD_HHMMSS_nombre.ext
        file_path = f"audios/{user_id}/{timestamp}_{file.filename}"

        # Subimos el archivo a Firebase Storage usando el path generado
        storage.child(file_path).put(file.file)

        # Obtenemos la URL pública del archivo subido y la retornamos
        return storage.child(file_path).get_url(None)

    except Exception as e:
        # Si ocurre cualquier error, lo capturamos y lanzamos una excepción HTTP 500
        raise HTTPException(status_code=500, detail=f"Error al subir archivo: {str(e)}")
