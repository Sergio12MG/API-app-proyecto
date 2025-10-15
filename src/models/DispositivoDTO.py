from pydantic import BaseModel
from fastapi import Form
from typing import Optional

# ========= MODELOS =========
# Para lectura
class DispositivoDTO(BaseModel):
    id: int
    nombre: str
    imagen: str
    usuario_id: int

# Para registrar
class CrearDispositivoDTO(BaseModel):
    nombre: str
    imagen: Optional[str] = None
    usuario_id: int

# Para actualizar
class ActualizarDTO(BaseModel):
    nombre: Optional[str] = None
    imagen: Optional[str] = None

# ========= DEPENDENCIAS =========
# Para crear
def create_device_form(
        nombre: str = Form(..., max_length=100),
        imagen: str = Form("", max_length=255),
        usuario_id: int = Form(..., gt=0)
):
    return CrearDispositivoDTO(nombre=nombre, imagen=imagen or None, usuario_id=usuario_id)

# Para actualizar
def update_device_form(
        nombre: str = Form(..., max_length=100),
        imagen: str = Form("", max_length=255)
):
    return ActualizarDTO(nombre=nombre or None, imagen=imagen or None)
