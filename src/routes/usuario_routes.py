from fastapi import APIRouter, Depends
from sqlmodel import Session

from src.models.BaseModels import Usuario
from src.models.UsuarioDTO import *
from src.services import usuario_service as usv
from src.utils.database import get_session
from src.utils.respuesta import RespuestaGenerica

# Objeto para definir endpoints
router = APIRouter(prefix="/api/v1/usuarios", tags=["Usuarios"])

# ======================= REGISTRAR USUARIO =======================
@router.post("/registrar", response_model=RespuestaGenerica[Usuario])
def registrar_usuario(formulario: UsuarioDTO = Depends(default_user_form), session: Session = Depends(get_session)):
    # 1. Llamado al servicio
    usuario = usv.registrar_usuario(formulario, session)

    # 2. Responder
    return RespuestaGenerica(
        exito = True,
        mensaje = "Usuario registrado exitosamente",
        datos = usuario
    )

# ======================= OBTENER POR ID =======================
@router.get("/{id}", response_model=RespuestaGenerica[Usuario])
def obtener_usuario(id: int, session: Session = Depends(get_session)):
    usuario = usv.obtener_usuario(id, session)

    return RespuestaGenerica(
        exito = True,
        mensaje = "Usuario encontrado",
        datos = usuario
    )

# ======================= ACTUALIZAR USUARIO =======================
@router.put("/{id}", response_model=RespuestaGenerica[Usuario])
def actualizar_usuario(id: int, formulario: ActualizarUsuarioDTO = Depends(update_user_form), session: Session = Depends(get_session)):
    usuario = usv.actualizar_usuario(id, formulario, session)

    return RespuestaGenerica(
        exito = True,
        mensaje = "Usuario actualizado exitosamente",
        datos = usuario
    )

# ======================= ELIMINAR USUARIO =======================
@router.delete("/{id}", response_model=RespuestaGenerica[None])
def eliminar_usuario(id: int, session: Session = Depends(get_session)):
    usv.eliminar_usuario(id, session)

    return RespuestaGenerica(
        exito = True,
        mensaje = "Usuario eliminado exitosamente",
        datos = None
    )
