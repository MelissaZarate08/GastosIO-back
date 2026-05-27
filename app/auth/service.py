from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta
import os
from app.database import get_connection

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)

def create_token(user_id: int) -> str:
    expire = datetime.utcnow() + timedelta(
        minutes=int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 1440))
    )
    return jwt.encode(
        {"sub": str(user_id), "exp": expire},
        os.getenv("SECRET_KEY"),
        algorithm=os.getenv("ALGORITHM"),
    )

def register_user(nombre: str, email: str, password: str) -> dict:
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT id FROM usuarios WHERE email = %s", (email,))
        if cursor.fetchone():
            raise ValueError("El email ya está registrado")
        hashed = hash_password(password)
        cursor.execute(
            "INSERT INTO usuarios (nombre, email, password_hash) VALUES (%s, %s, %s)",
            (nombre, email, hashed),
        )
        conn.commit()
        return {"mensaje": "Usuario registrado correctamente"}
    finally:
        cursor.close()
        conn.close()

def login_user(email: str, password: str) -> dict:
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute(
            "SELECT id, nombre, password_hash FROM usuarios WHERE email = %s", (email,)
        )
        user = cursor.fetchone()
        if not user or not verify_password(password, user["password_hash"]):
            raise ValueError("Credenciales incorrectas")
        token = create_token(user["id"])
        return {"token": token, "usuario_id": user["id"], "nombre": user["nombre"]}
    finally:
        cursor.close()
        conn.close()