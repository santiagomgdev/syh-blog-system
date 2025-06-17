from fastapi import APIRouter
from app.modules.apis.v1.auth import router as auth_router
from app.modules.apis.v1.user import router as user_router

router = APIRouter()

router.include_router(
    auth_router, 
    prefix="/auth", 
    tags=["Authentication"],
    responses={
        201: {"description": "Usuario registrado exitosamente"},
        422: {"description": "Datos de registro inválidos"}
    },
)

router.include_router(
    user_router, 
    prefix="/users", 
    tags=["Users"],
    responses={
        200: {"description": "Usuario encontrado"},
        401: {"description": "Token inválido o usuario no encontrado"},
        404: {"description": "Usuario no encontrado"}
    },
)
