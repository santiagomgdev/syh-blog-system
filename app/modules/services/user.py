from fastapi import Depends, HTTPException

from app.modules.repository.adapter.user_repository_interface import UsuarioRepositoryInterface
from app.utils.security import verify_token


class UserService:
    def __init__(self, usuario_repository: UsuarioRepositoryInterface):
        self.usuario_repository = usuario_repository

    def get_current_user(self, token: str):
        payload = verify_token(token)
        if payload is None:
            raise HTTPException(
                status_code=401,
                detail="Token inválido",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        user_id = payload.get("sub")
        if user_id is None:
            raise HTTPException(
                status_code=401,
                detail="Token inválido",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        user = self.usuario_repository.get_by_id(user_id)
        if user is None:
            raise HTTPException(
                status_code=404,
                detail="Usuario no encontrado",
            )
        
        return user