from typing import Optional
from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from app.core.database.connection import get_db
from app.utils.security import security
from app.modules.repository.adapter.mysql.role import MysqlRolUsuarioRepository
from app.modules.repository.adapter.mysql.token import MysqlTokenRepository
from app.modules.repository.adapter.mysql.user import MysqlUsuarioRepository
from app.modules.services.refresh import RefreshTokenService
from app.modules.services.register import RegisterService
from app.modules.services.login import LoginService
from app.modules.services.user import UserService


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

def get_user_service(
    user_repository: MysqlUsuarioRepository = Depends(get_user_repository)
) -> UserService:
    return UserService(user_repository)

def get_current_user(
    user_service: UserService = Depends(get_user_service),
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security)
):
    """
    Dependencia para obtener el usuario actual a partir del token de acceso.
    """
    access_token = None

    if credentials:
        access_token = credentials.credentials

    if not access_token:
        raise HTTPException(
            status_code=401,
            detail="Token de acceso no proporcionado",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return user_service.get_user_from_token(access_token)