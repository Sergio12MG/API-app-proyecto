from fastapi import HTTPException, status
from sqlmodel import Session, select

from src.models.BaseModels import Usuario
from src.models.UsuarioDTO import UsuarioDTO, ActualizarUsuarioDTO
from src.utils.auth import hash_password

# ================== REGISTRAR USUARIO ==================
def registrar_usuario(formulario: UsuarioDTO, session: Session) -> Usuario:
    # 1. Verificar si el correo ya está registrado
    correo_existente = session.exec(select(Usuario).where(Usuario.correo == formulario.correo)).first()
    if correo_existente:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Este correo ya está en uso."
        )
    
    # 2. Encriptar la contraseña
    clave_encriptada = hash_password(formulario.contrasena)

    # 3. Objeto para registrar el usuario en la base de datos
    usuario_db = Usuario(
        nombre=formulario.nombre,
        correo=formulario.correo,
        contrasena=clave_encriptada
    )

    session.add(usuario_db) # Añadir objeto a la sesión
    session.commit() # Insertar en la tabla
    session.refresh(usuario_db) # Actualizar el objeto

    return usuario_db

# ================== OBTENER POR ID ==================
def obtener_usuario(id: int, session: Session) -> Usuario:
    # 1. Buscar en la base de datos
    objetivo = session.exec(select(Usuario).where(Usuario.id == id)).first()

    # 2. Verificar que el usuario existe
    if objetivo is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Usuario no encontrado con ID {id}"
        )
    
    return objetivo

# ================== ACTUALIZAR USUARIO ==================
def actualizar_usuario(id: int, formulario: ActualizarUsuarioDTO, session: Session) -> Usuario:
    # 1. Buscar en la base de datos
    usuario_db = obtener_usuario(id, session)

    # 2. Obtener los datos del formulario que no son nulos
    update_data = formulario.model_dump(exclude_unset=True)

    # 3. Validar si se proporcionó un correo nuevo
    if "correo" in update_data and update_data["correo"] is not None:
        # Verificar que el correo no esté en uso por otro usuario
        if update_data["correo"] != usuario_db.correo:
            correo_existente = session.exec(select(Usuario).where(Usuario.correo == update_data["correo"])).first()
            if correo_existente:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Este correo ya está en uso."
                )

    # 4. Encriptar la contraseña si se está actualizando
    if "contrasena" in update_data and update_data["contrasena"] is not None:
        clave_encriptada = hash_password(update_data["contrasena"])
        update_data["contrasena"] = clave_encriptada

    # 5. Actualizar los campos del objeto de usuario
    for key, value in update_data.items():
        if value is not None:
            setattr(usuario_db, key, value)

    # 6. Guardar los cambios en la base de datos
    session.add(usuario_db)
    session.commit()
    session.refresh(usuario_db)

    return usuario_db

# ================== ELIMINAR USUARIO ==================
def eliminar_usuario(id: int, session: Session):
    # 1. Buscar en la base de datos
    usuario_db = obtener_usuario(id, session)

    # 2. Eliminar de la base de datos
    session.delete(usuario_db)
    session.commit()
