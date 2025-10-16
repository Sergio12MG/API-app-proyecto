from typing import List
from fastapi import HTTPException, status
from sqlmodel import Session, select

from src.models.BaseModels import Dispositivo
from src.models.DispositivoDTO import DispositivoDTO, ActualizarDTO

# ================== REGISTRAR DISPOSITIVO ==================
def registrar_dispositivo(formulario: DispositivoDTO, usuario_id: int, session: Session) -> Dispositivo:
    # 1. Objeto para registrar el dispositivo en la base de datos
    dispositivo_db = Dispositivo(
        nombre=formulario.nombre,
        imagen=formulario.imagen,
        usuario_id=usuario_id
    )

    session.add(dispositivo_db) # Añadir el objeto a la sesión
    session.commit() # Insertar en la tabla
    session.refresh(dispositivo_db) # Actualizar el objeto

    return dispositivo_db

# ================== OBTENER POR ID ==================
def obtener_dispositivo(id: int, usuario_id: int, session: Session) -> Dispositivo:
    # 1. Buscar en la base de datos: Solo se obtiene el dispositivo que pertenezca al usuario con la sesión activa
    consulta = select(Dispositivo).where((Dispositivo.id == id) & (Dispositivo.usuario_id == usuario_id))
    objetivo = session.exec(consulta).first()

    # 2. Verificar que el dispositivo existe
    if objetivo is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Dispositivo no encontrado con ID {id}"
        )
    
    return objetivo

# ================== OBTENER TODOS ==================
def obtener_todos(usuario_id: int, session: Session) -> List[Dispositivo]:
    # 1. Obtener los dispositivos que corresponden al usuario con la sesión activa
    consulta = select(Dispositivo).where(Dispositivo.usuario_id == usuario_id)
    resultado = session.exec(consulta).all()

    # 2. Asignar el resultado de la consulta a una lista
    dispositivos = list(resultado)

    # 3. Verificar que el usuario tiene dispositivos
    if len(dispositivos) == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No se han encontrado dispositivos"
        )

    return dispositivos

# ================== ACTUALIZAR DISPOSITIVO ==================
def actualizar_dispositivo(id: int, formulario: ActualizarDTO, usuario_id: int, session: Session) -> Dispositivo:
    # 1. Buscar en la base de datos
    dispositivo_db = obtener_dispositivo(id, usuario_id, session)

    # 2. Obtener los campos del formulario que no son nulos
    update_data = formulario.model_dump(exclude_unset=True)

    # 3. Actualizar los campos del objeto de dispositivo
    for key, value in update_data.items():
        if value is not None:
            setattr(dispositivo_db, key, value)

    # 4. Guardar los cambios en la base de datos
    session.add(dispositivo_db)
    session.commit()
    session.refresh(dispositivo_db)

    return dispositivo_db

# ================== ELIMINAR DISPOSITIVO ==================
def eliminar_dispositivo(id: int, usuario_id: int, session: Session):
    # 1. Buscar en la base de datos
    dispositivo_db = obtener_dispositivo(id, usuario_id, session)

    # 2. Eliminar de la base de datos
    session.delete(dispositivo_db)
    session.commit()
