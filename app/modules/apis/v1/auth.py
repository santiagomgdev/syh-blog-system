from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import ValidationError
from sqlalchemy.orm import Session

from app.core.database.connection import get_db
from app.modules.repository.adapter.mysql.role import MysqlRolUsuarioRepository
from app.modules.repository.adapter.mysql.token import MysqlTokenRepository
from app.modules.repository.adapter.mysql.user import MysqlUsuarioRepository
from app.modules.schemas.v1.token import TokenRefresh
from app.modules.schemas.v1.user import UsuarioCreate, UsuarioResponse, TokenResponse, UsuarioLogin
from app.modules.services.refresh import RefreshTokenService
from app.modules.services.register import RegisterService
from app.modules.services.login import LoginService


router = APIRouter()

def get_user_repository(db: Session = Depends(get_db)) -> MysqlUsuarioRepository:
    return MysqlUsuarioRepository(db)

def get_role_repository(db: Session = Depends(get_db)) -> MysqlRolUsuarioRepository:
    return MysqlRolUsuarioRepository(db)

def get_token_repository(db: Session = Depends(get_db)) -> MysqlTokenRepository:
    return MysqlTokenRepository(db)

def get_register_service(
    user_repository: MysqlUsuarioRepository = Depends(get_user_repository),
    role_repository: MysqlRolUsuarioRepository = Depends(get_role_repository)
) -> RegisterService:
    return RegisterService(user_repository, role_repository)

def get_login_service(
    user_repository: MysqlUsuarioRepository = Depends(get_user_repository),
    role_repository: MysqlRolUsuarioRepository = Depends(get_role_repository),
    token_repository: MysqlTokenRepository = Depends(get_token_repository)
) -> LoginService:
    return LoginService(user_repository, role_repository, token_repository)

def get_refresh_token_service(
    token_repository: MysqlTokenRepository = Depends(get_token_repository),
    user_repository: MysqlUsuarioRepository = Depends(get_user_repository)
) -> RefreshTokenService:
    return RefreshTokenService(token_repository, user_repository)

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

@router.post("/refresh", status_code=200)
def refresh_access_token(
    request: TokenRefresh,
    refresh_service: RefreshTokenService = Depends(get_refresh_token_service)
):
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