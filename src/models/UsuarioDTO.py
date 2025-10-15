from pydantic import BaseModel
from fastapi import Form
from typing import Optional

# ========= MODELO ESTÁNDAR DE USUARIO =========
class UsuarioDTO(BaseModel):
    nombre: str
    correo: str
    contrasena: str

# MODELO PARA ACTUALIZAR
class ActualizarUsuarioDTO(BaseModel):
    nombre: Optional[str] = None
    correo: Optional[str] = None
    contrasena: Optional[str] = None

# ========= FORMULARIO PARA REGISTRAR USUARIOS =========
def default_user_form(
        nombre: str = Form(..., max_length=30),
        correo: str = Form(..., max_length=50),
        contrasena: str = Form(..., min_length=5, max_length=64)
):
    return UsuarioDTO(nombre=nombre, correo=correo, contrasena=contrasena)

# ========= FORMULARIO PARA ACTUALIZAR USUARIOS =========
def update_user_form(
        nombre: str = Form("", max_length=30),
        correo: str = Form("", max_length=50),
        contrasena: str = Form("", min_length=5, max_length=64)
):
    return ActualizarUsuarioDTO(nombre=nombre or None, correo=correo or None, contrasena=contrasena or None)
