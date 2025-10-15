import os
from datetime import datetime, timedelta, timezone
from typing import Optional

from jose import jwt, JWTError
from passlib.context import CryptContext
from sqlmodel import Session, select
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from dotenv import load_dotenv

from src.utils.database import get_session
from src.models.BaseModels import Usuario

# Cargar las variables de entorno
load_dotenv()

# CONFIGURACIÓN BASE
SECRET_KEY = os.getenv("JWT_SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30 # Expira en 30 minutos

# Objeto para encriptar contraseñas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

# ============ Validaciones de JWT ============
# Verificación para que la contraseña en bytes no supere los 72 bytes
def _ensure_bcrypt_safe(password: str) -> None:
    b = password.encode("utf-8")

    if len(b) > 72:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La contraseña es demasiado larga (más de 72 bytes). Usa una contraseña más corta (<= 64 caracteres)."
        )
    
# Encriptado de la contraseña
def hash_password(password: str) -> str:
    _ensure_bcrypt_safe(password) # Evita el encriptado si la contraseña supera los 72 bytes
    return pwd_context.hash(password)

# Comparación de la contraseña ingresada con el hash
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# ============ MANEJO DE TOKENS ============
# Generar un token
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    # 1. Copia de las credenciales
    credenciales = data.copy()

    # 2. Agregar la fecha de expiración
    if expires_delta:
        # Si se definió una duración específica, se usa
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        # Si no, se usa la duración por defecto (30 minutos)
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    # 3. Añadir la fecha de expiración al diccionario de credenciales
    credenciales.update({"exp": expire})

    # 4. Convertir las credenciales en token y firmarlo con la clave secreta
    token = jwt.encode(credenciales, str(SECRET_KEY), algorithm=ALGORITHM)

    return token

# Decodificar el token
def decode_access_token(token: str) -> dict:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token inválido o malformado",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        # Se obtiene la credencial del token, verificando la clave secreta
        payload = jwt.decode(token, str(SECRET_KEY), algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise credentials_exception
    
# Para proteger endpoints
def get_current_user(token: str = Depends(oauth2_scheme), session: Session = Depends(get_session)) -> Usuario:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudieron validar las credenciales",
        headers={"WWW-Authenticate": "Bearer"},
    )

    # 1. Decodificar el token
    payload = decode_access_token(token)
    # 2. Obtener el valor del campo 'sub' (el usuario) de las credenciales
    username: Optional[str] = payload.get("sub")

    # 3. Verificar que sí haya un nombre de usuario
    if username is None:
        raise credentials_exception
    
    # 4. Buscar al usuario en la base de datos por el nombre obtenido
    consulta = select(Usuario).where(Usuario.nombre == username)
    user = session.exec(consulta).first()

    # 5. Verificar que sí exista el usuario
    if user is None:
        raise credentials_exception
    
    return user
