from typing import TypeVar, Generic, Optional
from pydantic import BaseModel

T = TypeVar('T')

class RespuestaGenerica(BaseModel, Generic[T]):
    exito: bool
    mensaje: str
    datos: Optional[T] | None
