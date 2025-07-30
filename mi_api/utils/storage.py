import os
from datetime import datetime
from fastapi import HTTPException, UploadFile
from utils.firebase import firebase

storage = firebase.storage()

async def upload_audio(file: UploadFile, user_id: str) -> str:
    try:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_path = f"audios/{user_id}/{timestamp}_{file.filename}"
        storage.child(file_path).put(file.file)
        return storage.child(file_path).get_url(None)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al subir archivo: {str(e)}")