from sqlmodel import Session, select

from src.models.BaseModels import Usuario
from src.utils.auth import verify_password

# Autenticar un usuario
def authenticate_user(session: Session, username: str, password: str):
    # 1. Obtener al usuario desde la base de datos
    consulta = select(Usuario).where(Usuario.correo == username)
    user = session.exec(consulta).first()

    # 2. Verificar que se obtuvo el usuario
    if not user:
        return None
    
    # 3. Verificar que la contraseña coincide
    if not verify_password(password, user.contrasena):
        return None
    
    return user
