from abc import abstractmethod
from typing import List, Optional

from app.core.models.auth.token import Token
from app.modules.repository.repository_interface import RepositoryInterface


class TokenRepositoryInterface(RepositoryInterface[Token]):
    """
    Interface específica para el repositorio de tokens.
    Extiende la interface base con métodos específicos para tokens de refresh.
    """
    
    @abstractmethod
    def get_by_token(self, token_refresco: str) -> Optional[Token]:
        """Obtiene un token por su valor de refresh token"""
        pass
    
    @abstractmethod
    def get_by_usuario_id(self, usuario_id: int) -> List[Token]:
        """Obtiene todos los tokens de un usuario específico"""
        pass

    @abstractmethod
    def is_token_valid(self, token_refresco: str) -> bool:
        """Verifica si un token es válido (existe, no está revocado y no ha expirado)"""
        pass

    @abstractmethod
    def revoke_user_token(self, token_refresco: str) -> bool:
        """Revoca un token específico"""
        pass