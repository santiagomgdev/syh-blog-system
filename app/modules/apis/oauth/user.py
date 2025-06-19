from fastapi import APIRouter, Depends, HTTPException

from app.modules.schemas.v1.user import UsuarioResponse
from app.modules.services.user import UserService
from app.modules.apis.dependencies import get_user_service
from app.utils.security import oauth2_scheme


router = APIRouter()

@router.get("/me", response_model=UsuarioResponse, status_code=200)
def get_current_user_oauth(
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