from fastapi import APIRouter, HTTPException, status
from .schemas import RegisterRequest, LoginRequest, TokenResponse
from . import service

router = APIRouter(prefix="/api/auth", tags=["Autenticación"])

@router.post("/register", status_code=status.HTTP_201_CREATED)
def register(body: RegisterRequest):
    try:
        return service.register_user(body.nombre, body.email, body.password)
    except ValueError as e:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, str(e))

@router.post("/login", response_model=TokenResponse)
def login(body: LoginRequest):
    try:
        return service.login_user(body.email, body.password)
    except ValueError as e:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, str(e))