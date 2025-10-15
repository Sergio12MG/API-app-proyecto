from dotenv import load_dotenv
import os

from sqlalchemy import create_engine
from sqlmodel import SQLModel, Session

# Cargar las variables de entorno
load_dotenv()

# ================================ REFERENCIAR LAS VARIABLES DE ENTORNO ================================
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

# ================================ DEFINICIÓN DE LA URL DE CONEXIÓN ================================
DATABASE_URL = (
    f"mysql+pymysql://{DB_USER}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

# ================================ CONSTRUCCIÓN DEL MOTOR DE CONEXIÓN ================================
engine = create_engine(DATABASE_URL, echo=False, pool_recycle=3600)
with engine.connect() as conn:
    print("Conexión exitosa")

def crear_tablas():
    SQLModel.metadata.create_all(engine)

# Función para obtener la sesión de la base de datos
def get_session():
    with Session(engine) as session:
        yield session
