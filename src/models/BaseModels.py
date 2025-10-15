from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List

# ============= MODELO DE USUARIO =============
class Usuario(SQLModel, table=True):
    __tablename__ = "usuarios" # type: ignore
    id: Optional[int] = Field(primary_key=True, unique=True, default=None, index=True)
    nombre: str = Field(max_length=30, nullable=False)
    correo: str = Field(max_length=50, unique=True, nullable=False)
    contrasena: str = Field(min_length=5, max_length=64, nullable=False)
    # Mapeo uno a muchos (un usuario tiene varios dispositivos)
    dispositivos: List["Dispositivo"] = Relationship(back_populates="usuario")

class Dispositivo(SQLModel, table=True):
    __tablename__ = "dispositivos" # type: ignore
    id: Optional[int] = Field(primary_key=True, unique=True, default=None, index=True)
    nombre: str = Field(max_length=100, nullable=False)
    imagen: Optional[str] = Field(max_length=255, nullable=True)
    usuario_id: Optional[int] = Field(default=None, foreign_key="usuarios.id") # FK
    # Mapeo uno a uno (un dispositivo pertenece a un usuario)
    usuario: Optional[Usuario] = Relationship(back_populates="dispositivos")
