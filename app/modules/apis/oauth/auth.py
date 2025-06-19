from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import ValidationError

from app.modules.schemas.v1.token import TokenBase, TokenRefresh
from app.modules.schemas.v1.user import  TokenResponse, UsuarioLogin
from app.modules.services.refresh import RefreshTokenService
from app.modules.services.login import LoginService
from app.modules.apis.dependencies import (
    get_login_service,
    get_refresh_token_service
)


router = APIRouter()
    
@router.post("/login", response_model=TokenResponse, status_code=200)
def login_user(
    oauth_form_data: OAuth2PasswordRequestForm = Depends(),
    login_service: LoginService = Depends(get_login_service)
) -> TokenResponse:
    try:
        user_data = UsuarioLogin(
            nombre_usuario=oauth_form_data.username,
            contrasena=oauth_form_data.password
        )
        return login_service.login(user_data)
    
    except ValidationError as e:
        raise HTTPException(
            status_code=422,
            detail=f"Error de validación: {str(e)}"
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error interno del servidor: {str(e)}"
        )

@router.post("/refresh", response_model=TokenBase, status_code=200)
def refresh_access_token(
    request: TokenRefresh,
    refresh_service: RefreshTokenService = Depends(get_refresh_token_service)
) -> TokenBase:
    """
    Endpoint para refrescar el access token usando un refresh token válido
    """
    try:
        return refresh_service.refresh_access_token(request.refresh_token)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error interno del servidor: {str(e)}"
        )
