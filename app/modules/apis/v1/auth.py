from fastapi import APIRouter, Depends, HTTPException
from pydantic import ValidationError
from sqlalchemy.orm import Session

from app.core.database.connection import get_db
from app.modules.repository.adapter.mysql.role import MysqlRolUsuarioRepository
from app.modules.repository.adapter.mysql.user import MysqlUsuarioRepository
from app.modules.schemas.v1.user import UsuarioCreate, UsuarioResponse
from app.modules.services.register import RegisterService


router = APIRouter()

def get_user_repository(db: Session = Depends(get_db)) -> MysqlUsuarioRepository:
    return MysqlUsuarioRepository(db)

def get_role_repository(db: Session = Depends(get_db)) -> MysqlRolUsuarioRepository:
    return MysqlRolUsuarioRepository(db)

def get_register_service(
    user_repository: MysqlUsuarioRepository = Depends(get_user_repository),
    role_repository: MysqlRolUsuarioRepository = Depends(get_role_repository)
) -> RegisterService:
    return RegisterService(user_repository, role_repository)

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
