from fastapi import APIRouter, Depends, HTTPException, Request, Response
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import ValidationError

from app.modules.schemas.v1.token import TokenBase, TokenRefresh
from app.modules.schemas.v1.user import UsuarioCreate, UsuarioResponse, TokenResponse, UsuarioLogin
from app.modules.services.refresh import RefreshTokenService
from app.modules.services.register import RegisterService
from app.modules.services.login import LoginService
from app.modules.apis.dependencies import (
    get_register_service,
    get_login_service,
    get_refresh_token_service
)


router = APIRouter()

@router.post("/register", response_model=UsuarioResponse, status_code=201)
def register_user(
    user_data: UsuarioCreate,
    register_service: RegisterService = Depends(get_register_service)
) -> UsuarioResponse:
    try:
        return register_service.register(user_data)
    
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
    
@router.post("/oauth/login", response_model=TokenResponse, status_code=200)
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
    
@router.post("/login", response_model=TokenResponse, status_code=200)
def auth_user(
    form_data: UsuarioLogin,
    response: Response,
    login_service: LoginService = Depends(get_login_service)
) -> TokenResponse:
    try:
        result = login_service.login(form_data)

        response.set_cookie(
            key="refresh_token",
            value=result.refresh_token,
            # max_age=REFRESH_TOKEN_EXPIRE_MINUTES * 60,
            httponly=True,
            secure=False,  # Establecer en False en desarrollo si no se utiliza HTTPS
            samesite="lax"
        )

        return result
    
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

@router.post("/oauth/refresh", response_model=TokenBase, status_code=200)
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
    
@router.post("/refresh", response_model=TokenBase, status_code=200)
def refresh_token(
    request: Request,
    response: Response,
    refresh_service: RefreshTokenService = Depends(get_refresh_token_service)
) -> TokenBase:
    """
    Endpoint para refrescar el access token usando un refresh token válido
    """
    credentials_exception = HTTPException(
        status_code=401,
        detail="No se pudo validar el refresh token"
    )

    refresh_token = request.cookies.get("refresh_token")
    if not refresh_token:
        raise credentials_exception

    try:
        result = refresh_service.refresh_access_token(refresh_token)

        response.set_cookie(
            key="refresh_token",
            value=result.refresh_token,
            httponly=True,
            secure=False,  # Establecer en False en desarrollo si no se utiliza HTTPS
            samesite="lax"
        )

        return result
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error interno del servidor: {str(e)}"
        )