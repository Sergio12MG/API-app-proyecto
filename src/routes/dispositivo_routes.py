from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session

from src.models.BaseModels import Dispositivo, Usuario
from src.models.DispositivoDTO import *
from src.services import dispositivo_service as dsv
from src.utils.database import get_session
from src.utils.respuesta import RespuestaGenerica
from src.utils.auth import get_current_user

# Objeto para definir endpoints
router = APIRouter(prefix="/api/v1/dispositivos", tags=["Dispositivos"])

# ======================= REGISTRAR DISPOSITIVO =======================
@router.post("/registrar", response_model=RespuestaGenerica[Dispositivo])
def registrar_dispositivo(
    formulario: DispositivoDTO = Depends(create_device_form),
    session: Session = Depends(get_session),
    usuario_autenticado: Usuario = Depends(get_current_user)
    ):
    # 1. Obtener el ID del usuario con la sesión activa
    usuario_id = usuario_autenticado.id # El tipo es Optional[int]

    # 2. Verificar que el ID del usuario no sea nulo
    if usuario_id is None:
        # Esto satisface al analizador de tipos y añade una capa extra de seguridad
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No se pudo verificar la identidad del usuario."
        )

    # 3. Llamado al servicio
    dispositivo = dsv.registrar_dispositivo(formulario, usuario_id, session)

    # 4. Responder
    return RespuestaGenerica(
        exito = True,
        mensaje = "Dispositivo creado exitosamente.",
        datos = dispositivo
    )

# ======================= OBTENER DISPOSITIVO =======================
@router.get("/{id}", response_model=RespuestaGenerica[Dispositivo])
def obtener_dispositivo(
    id: int,
    session: Session = Depends(get_session),
    usuario_autenticado: Usuario = Depends(get_current_user)
    ):
    # 1. Obtener el ID del usuario
    usuario_id = usuario_autenticado.id

    if usuario_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No se pudo verificar la identidad del usuario."
        )
    
    # 2. Llamado al servicio
    dispositivo = dsv.obtener_dispositivo(id, usuario_id, session)

    return RespuestaGenerica(
        exito = True,
        mensaje = "Dispositivo encontrado",
        datos = dispositivo
    )

# ======================= OBTENER TODOS =======================
@router.get("/", response_model=RespuestaGenerica[list])
def obtener_todos(
    usuario_autenticado: Usuario = Depends(get_current_user),
    session: Session = Depends(get_session)
    ):
    # 1. Obtener el ID del usuario
    usuario_id = usuario_autenticado.id

    if usuario_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No se pudo verificar la identidad del usuario."
        )
    
    # 2. Llamado al servicio
    dispositivos = dsv.obtener_todos(usuario_id, session)

    return RespuestaGenerica(
        exito = True,
        mensaje = "Dispositivos obtenidos exitosamente",
        datos = dispositivos
    )

# ======================= ACTUALIZAR DISPOSITIVO =======================
@router.put("/{id}", response_model=RespuestaGenerica[Dispositivo])
def actualizar_dispositivo(
    id: int,
    formulario: ActualizarDTO = Depends(update_device_form),
    session: Session = Depends(get_session),
    usuario_autenticado: Usuario = Depends(get_current_user)
    ):
    # 1. Obtener el ID del usuario
    usuario_id = usuario_autenticado.id

    if usuario_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No se pudo verificar la identidad del usuario."
        )
    
    # 2. Llamado al servicio
    dispositivo = dsv.actualizar_dispositivo(id, formulario, usuario_id, session)

    return RespuestaGenerica(
        exito = True,
        mensaje = "Dispositivo actualizado exitosamente",
        datos = dispositivo
    )

# ======================= ELIMINAR DISPOSITIVO =======================
@router.delete("/{id}", response_model=RespuestaGenerica[None])
def eliminar_dispositivo(
    id: int,
    session: Session = Depends(get_session),
    usuario_autenticado: Usuario = Depends(get_current_user)
    ):
    # 1. Obtener el ID del usuario
    usuario_id = usuario_autenticado.id

    if usuario_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No se pudo verificar la identidad del usuario."
        )
    
    # 2. Llamado al servicio
    dsv.eliminar_dispositivo(id, usuario_id, session)

    return RespuestaGenerica(
        exito = True,
        mensaje = "Dispositivo eliminado exitosamente",
        datos = None
    )
