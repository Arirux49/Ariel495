import pyrebase
from fastapi import HTTPException

config = {
    "apiKey": "AIzaSyD3Qq_MJn7W-Gs5K-nBTlRnnU90rPSGbuU",
    "authDomain": "cluster0.vcs8lnn.firebaseapp.com",
    "projectId": "cluster0",
    "storageBucket": "cluster0.vcs8lnn.appspot.com",
    "databaseURL": ""
}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()

def verify_firebase_token(id_token: str) -> str:
    try:
        user = auth.get_account_info(id_token)
        return user["users"][0]["localId"]
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Token inválido: {str(e)}")