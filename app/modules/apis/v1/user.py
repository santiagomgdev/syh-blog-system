from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database.connection import get_db
from app.modules.repository.adapter.mysql.user import MysqlUsuarioRepository
from app.modules.schemas.v1.user import UsuarioResponse
from app.modules.services.user import UserService
from app.utils.security import oauth2_scheme

router = APIRouter()

def get_user_repository(db: Session = Depends(get_db)) -> MysqlUsuarioRepository:
    return MysqlUsuarioRepository(db)

def get_user_service(
    user_repository: MysqlUsuarioRepository = Depends(get_user_repository)
) -> UserService:
    return UserService(user_repository)

@router.get("/me", response_model=UsuarioResponse, status_code=200)
def get_current_user(
    user_service: UserService = Depends(get_user_service),
    token: str = Depends(oauth2_scheme)
) -> UsuarioResponse:
    """
    Obtiene el usuario actual a partir del token de autenticación.
    """
    user = user_service.get_current_user(token)
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Token inválido o usuario no encontrado",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user