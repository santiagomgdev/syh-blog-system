from fastapi import APIRouter, Depends, HTTPException

from app.modules.schemas.v1.user import UsuarioResponse
from app.modules.apis.dependencies import get_current_user


router = APIRouter()

@router.get("/me", response_model=UsuarioResponse, status_code=200)
def get_me(
    current_user: UsuarioResponse = Depends(get_current_user)
) -> UsuarioResponse:
    """
    Devuelve la información del usuario autenticado.
    """
    if current_user is None:
        raise HTTPException(
            status_code=401,
            detail="Token de acceso no proporcionado",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return current_user
