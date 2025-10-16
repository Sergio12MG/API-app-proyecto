from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session

from src.utils.database import get_session
from src.models.Token import Token
from src.services.auth_service import authenticate_user
from src.utils.auth import create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES

# Objeto para definir endpoints
router = APIRouter(prefix="/api/v1/auth", tags=["auth"])

# Endpoint para iniciar sesión
@router.post("/token", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(get_session)) -> Token:
    # 1. Obtener el nombre de usuario y contraseña del formulario
    user = authenticate_user(session, form_data.username, form_data.password)

    # 2. Verificar que el usuario existe
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Correo o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # 3. Generar el token
    access_token = create_access_token(data={"sub": user.correo}, expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))

    return Token(
        access_token=access_token,
        token_type="bearer",
        expires_in=ACCESS_TOKEN_EXPIRE_MINUTES * 60
    )
