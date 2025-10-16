from pydantic import BaseModel
from fastapi import Form
from typing import Optional

# ========= MODELOS =========
# Para registrar
class DispositivoDTO(BaseModel):
    nombre: str
    imagen: Optional[str] = None

# Para actualizar
class ActualizarDTO(BaseModel):
    nombre: Optional[str] = None
    imagen: Optional[str] = None

# ========= DEPENDENCIAS =========
# Para crear
def create_device_form(
        nombre: str = Form(..., max_length=100),
        imagen: str = Form("", max_length=255)
):
    return DispositivoDTO(nombre=nombre, imagen=imagen or None)

# Para actualizar
def update_device_form(
        nombre: str = Form(..., max_length=100),
        imagen: str = Form("", max_length=255)
):
    return ActualizarDTO(nombre=nombre or None, imagen=imagen or None)
