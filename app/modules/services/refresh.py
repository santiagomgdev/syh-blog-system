from datetime import datetime, timedelta
from typing import Optional
from fastapi import HTTPException, status

from app.core.models.auth.token import Token
from app.modules.repository.adapter.token_repository_interface import TokenRepositoryInterface
from app.modules.repository.adapter.user_repository_interface import UsuarioRepositoryInterface
from app.utils.security import create_access_token, verify_token
from app.core.config import settings


class RefreshTokenService:
    def __init__(self, 
                 token_repository: TokenRepositoryInterface, 
                 user_repository: UsuarioRepositoryInterface):
        self.token_repository = token_repository
        self.user_repository = user_repository

    def refresh_access_token(self, refresh_token: str) -> dict:
        """
        Genera un nuevo access token usando un refresh token válido
        """
        # Verificar que el token existe en la base de datos y es válido
        if not self.token_repository.is_token_valid(refresh_token):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Refresh token inválido o expirado"
            )
        
        # Verificar el JWT del refresh token
        payload = verify_token(refresh_token)
        if not payload: # or payload.get("type") != "refresh": (Pendiente por implementar)
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Refresh token inválido"
            )
        
        # Obtener el usuario
        user_id = payload.get("sub")
        user = self.user_repository.get_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuario no encontrado"
            )
        
        # Crear nuevo access token
        token_data = {
            "sub": str(user.id),
            "email": user.correo,
            "username": user.nombre_usuario
        }
        
        new_access_token = create_access_token(token_data)
        
        return {
            "access_token": new_access_token,
            "token_type": "bearer"
        }
