from fastapi import APIRouter
from app.modules.apis.oauth.auth import router as auth_router
from app.modules.apis.oauth.user import router as user_router


router = APIRouter()

router.include_router(
    auth_router, 
    prefix="/oauth", 
    tags=["Authentication Oauth"],
    responses={
        201: {"description": "Usuario registrado exitosamente"},
        422: {"description": "Datos de registro inválidos"}
    },
)

router.include_router(
    user_router, 
    prefix="/oauth/users", 
    tags=["Users OAuth"],
    responses={
        200: {"description": "Usuario encontrado"},
        401: {"description": "Token inválido o usuario no encontrado"},
        404: {"description": "Usuario no encontrado"}
    },
)