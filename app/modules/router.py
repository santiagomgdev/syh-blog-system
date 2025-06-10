from fastapi import APIRouter
from app.modules.apis.v1.auth import router as auth_router

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
