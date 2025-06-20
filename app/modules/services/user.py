from app.core.exceptions.auth import InvalidCredentialsError
from app.core.models.auth.user import Usuario
from app.modules.repository.adapter.user_repository_interface import UsuarioRepositoryInterface
from app.utils.security import verify_token, verify_token


class UserService:
    def __init__(self, usuario_repository: UsuarioRepositoryInterface):
        self.usuario_repository = usuario_repository
    
    def get_user_from_token(self, access_token: str) -> Usuario:
        """
        Obtiene el usuario a partir del token de acceso.
        """
        
        # Verifica Token
        payload = verify_token(access_token)
        if not payload:
            raise InvalidCredentialsError("Token inválido o expirado")
        
        # Obtiene usuario por BD
        user_id = payload.get("sub")
        if user_id is None:
            raise InvalidCredentialsError("Token inválido, no se encontró el ID de usuario")
        
        user = self.usuario_repository.get_by_id(user_id)
        if user is None or not user.activo:
            raise InvalidCredentialsError("Usuario no encontrado o inactivo")
        
        return user