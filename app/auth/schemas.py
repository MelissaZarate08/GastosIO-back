from pydantic import BaseModel, EmailStr, Field

class RegisterRequest(BaseModel):
    nombre: str
    email: EmailStr
    password: str = Field(min_length=6, max_length=72)

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    token: str
    usuario_id: int
    nombre: str