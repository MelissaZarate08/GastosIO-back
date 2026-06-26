from fastapi import FastAPI
from app.auth.router import router as auth_router
from app.transacciones.router import router as transacciones_router
from app.notifications.router import router as notifications_router

app = FastAPI(
    title="GastosIO API",
    description="Backend para la app de control de finanzas personales",
    version="1.0.0",
)

app.include_router(auth_router)
app.include_router(transacciones_router)
app.include_router(notifications_router)

@app.get("/")
def root():
    return {"status": "GastosIO API corriendo"}