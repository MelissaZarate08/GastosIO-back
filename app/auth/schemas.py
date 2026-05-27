from pydantic import BaseModel, EmailStr

class RegisterRequest(BaseModel):
    nombre: str
    email: EmailStr
    password: str

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    token: str
    usuario_id: int
    nombre: str