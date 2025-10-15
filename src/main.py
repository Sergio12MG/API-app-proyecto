from fastapi import FastAPI

from src.middleware.main_middleware import MainMiddleware
from src.routes.auth_routes import router as auth_router
from src.routes.usuario_routes import router as users_router

# ================== Creación del objeto de FastAPI ==================
app = FastAPI(
    title="API de app con arduino",
    version="1.0.0"
)

# Registro del middleware
app.add_middleware(MainMiddleware)

# Registro de las rutas
app.include_router(router=auth_router)
app.include_router(router=users_router)
