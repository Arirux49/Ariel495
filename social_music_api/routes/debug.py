from fastapi import APIRouter, Request

router = APIRouter(tags=["Debug"])

@router.get("/health")
async def health():
    return {"status": "ok"}

@router.get("/echo-headers")
async def echo_headers(request: Request):
    return {"headers": dict(request.headers)}

@router.get("/whoami")
async def whoami(request: Request):
    auth = request.headers.get("authorization", "")
    masked = "Bearer ****" + auth[-6:] if auth.lower().startswith("bearer ") else (auth or "(none)")
    return {"authorization": masked}
