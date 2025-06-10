from abc import abstractmethod
from typing import Optional

from app.core.models.auth.user import Usuario
from app.modules.repository.repository_interface import RepositoryInterface

class UsuarioRepositoryInterface(RepositoryInterface[Usuario]):
    """
    Interface para el repositorio de Usuario con metodos especificos para el modelo Usuario
    """
    @abstractmethod
    def get_by_nombre_usuario(self, nombre_usuario: str) -> Optional[Usuario]:
        """Obtiene un usuario por su nombre de usuario"""
        pass

    @abstractmethod
    def get_by_correo(self, correo: str) -> Optional[Usuario]:
        """Obtiene un usuario por su correo electronico"""
        pass