from fastapi import APIRouter, Request

router = APIRouter(prefix="", tags=["Debug"])

@router.get("/health")
async def health():
    return {"status": "ok"}

@router.get("/ping")
async def ping():
    return {"pong": True}

@router.get("/echo-headers")
async def echo_headers(request: Request):
    return {"headers": dict(request.headers)}

@router.get("/whoami")
async def whoami(request: Request):
    auth = request.headers.get("authorization", "")
    if auth.lower().startswith("bearer "):
        masked = "Bearer ****" + auth[-6:]
    else:
        masked = auth or "(none)"
    return {"authorization": masked}
