# routes/debug_routes.py
from fastapi import APIRouter, HTTPException
from utils.firebase_utils import init_firebase, debug_firebase

router = APIRouter(prefix="/auth/debug", tags=["Debug"])

@router.get("/firebase")
def firebase_debug():
    try:
        init_firebase()
        return debug_firebase()
    except Exception as e:
        raise HTTPException(500, f"Debug error: {e}")
