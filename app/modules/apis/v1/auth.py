from fastapi import APIRouter, Depends, HTTPException, Request, Response

from app.core.exceptions.auth import TokenGenerationError
from app.modules.schemas.v1.token import TokenBase
from app.modules.schemas.v1.user import UsuarioCreate, UsuarioResponse, TokenResponse, UsuarioLogin
from app.modules.services.refresh import RefreshTokenService
from app.modules.services.register import RegisterService
from app.modules.services.login import LoginService
from app.modules.apis.dependencies import (
    get_register_service,
    get_login_service,
    get_refresh_token_service
)
from app.utils.security import create_access_token


router = APIRouter()

@router.post("/register", response_model=UsuarioResponse, status_code=201)
def register_user(
    user_data: UsuarioCreate,
    register_service: RegisterService = Depends(get_register_service)
) -> UsuarioResponse:
    """Endpoint para registrar un nuevo usuario"""

    user = register_service.register(
        username=user_data.nombre_usuario,
        email=user_data.correo,
        psw=user_data.contrasena
    )

    register_service.assign_default_role(user.id)

    return UsuarioResponse.model_validate(user)
    
    
@router.post("/login", response_model=TokenResponse, status_code=200)
def auth_user(
    form_data: UsuarioLogin,
    response: Response,
    login_service: LoginService = Depends(get_login_service)
) -> TokenResponse:
    """Endpoint para autenticar un usuario y generar tokens"""

    user = login_service.authenticate_user(form_data.nombre_usuario, form_data.contrasena)

    # Crear el payload del token
    token_data = {
        "sub": str(user.id),  # subject (user_id)
        "email": user.correo,
        "username": user.nombre_usuario
    }
    
    # Genera token de acceso
    access_token = create_access_token(token_data)

    if not access_token:
        raise TokenGenerationError("Error al generar token de acceso")

    result = login_service.create_refresh_token_for_user(user)

    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        # max_age=REFRESH_TOKEN_EXPIRE_MINUTES * 60,
        httponly=True,
        secure=False,  # Establecer en False en desarrollo si no se utiliza HTTPS
        samesite="lax"
    )

    return TokenResponse(
        access_token=access_token,
        refresh_token=result.token_refresco,
        user=UsuarioResponse.model_validate(user),
    )
    
@router.post("/refresh", response_model=TokenBase, status_code=200)
def refresh_token(
    request: Request,
    response: Response,
    refresh_service: RefreshTokenService = Depends(get_refresh_token_service)
) -> TokenBase:
    """Endpoint para refrescar el access token usando un refresh token válido"""

    refresh_token = request.cookies.get("refresh_token")
    if not refresh_token:
        raise HTTPException(
        status_code=401,
        detail="No se encontró refresh token en las cookies"
    )

    access_token = refresh_service.refresh_access_token(refresh_token)

    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=False,  # Establecer en False en desarrollo si no se utiliza HTTPS
        samesite="lax"
    )

    return TokenBase(
        access_token=access_token,
        refresh_token=refresh_token,
    )
