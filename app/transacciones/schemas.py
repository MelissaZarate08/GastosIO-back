from pydantic import BaseModel, condecimal
from typing import Optional
from datetime import datetime
from enum import Enum

class TipoEnum(str, Enum):
    ingreso = "ingreso"
    egreso = "egreso"

class TransaccionCreate(BaseModel):
    tipo: TipoEnum
    monto: condecimal(gt=0, decimal_places=2)
    categoria: str
    descripcion: Optional[str] = None

class TransaccionUpdate(BaseModel):
    monto: Optional[condecimal(gt=0, decimal_places=2)] = None
    categoria: Optional[str] = None
    descripcion: Optional[str] = None

class TransaccionResponse(BaseModel):
    id: int
    tipo: str
    monto: float
    categoria: str
    descripcion: Optional[str]
    fecha: datetime