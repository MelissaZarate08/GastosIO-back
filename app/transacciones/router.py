from fastapi import APIRouter, HTTPException, Depends, status
from .schemas import TransaccionCreate, TransaccionUpdate, TransaccionResponse
from . import service
from app.dependencies import get_current_user_id
from typing import List

router = APIRouter(
    prefix="/api/transacciones",
    tags=["Transacciones"],
    dependencies=[Depends(get_current_user_id)],
)

@router.get("", response_model=List[TransaccionResponse])
def get_all(usuario_id: int = Depends(get_current_user_id)):
    return service.get_all(usuario_id)

@router.post("", status_code=status.HTTP_201_CREATED, response_model=TransaccionResponse)
def create(body: TransaccionCreate, usuario_id: int = Depends(get_current_user_id)):
    return service.create(
        usuario_id, body.tipo, body.monto, body.categoria, body.descripcion
    )

@router.put("/{transaccion_id}")
def update(
    transaccion_id: int,
    body: TransaccionUpdate,
    usuario_id: int = Depends(get_current_user_id),
):
    fields = {k: v for k, v in body.model_dump().items() if v is not None}
    if not fields:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Sin campos para actualizar")
    try:
        return service.update(transaccion_id, usuario_id, fields)
    except ValueError as e:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(e))

@router.delete("/{transaccion_id}")
def delete(transaccion_id: int, usuario_id: int = Depends(get_current_user_id)):
    try:
        return service.delete(transaccion_id, usuario_id)
    except ValueError as e:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(e))