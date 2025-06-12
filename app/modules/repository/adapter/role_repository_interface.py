from abc import abstractmethod
from typing import List, Optional

from app.core.models.auth.role import RolUsuario
from app.modules.repository.repository_interface import RepositoryInterface

class RolUsuarioRepositoryInterface(RepositoryInterface[RolUsuario]):
    """
    Interface para el repositorio de RolUsuario con metodos especificos para el modelo RolUsuario
    """
    
    @abstractmethod
    def assign_role_to_user(self, usuario_id: int, nombre_rol: str) -> RolUsuario:
        """Asigna un rol a un usuario"""
        pass