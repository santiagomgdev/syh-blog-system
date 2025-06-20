from app.core.exceptions.auth import RefreshTokenError, TokenExpiredError, TokenGenerationError
from app.core.exceptions.user import UserNotFoundError
from app.modules.repository.adapter.token_repository_interface import TokenRepositoryInterface
from app.modules.repository.adapter.user_repository_interface import UsuarioRepositoryInterface
from app.utils.security import create_access_token, verify_token


class RefreshTokenService:
    def __init__(self, 
                 token_repository: TokenRepositoryInterface, 
                 user_repository: UsuarioRepositoryInterface):
        self.token_repository = token_repository
        self.user_repository = user_repository

    def refresh_access_token(self, refresh_token: str) -> str:
        """
        Genera un nuevo access token usando un refresh token válido
        """
        # Verificar que el token existe en la base de datos y es válido
        if not self.token_repository.is_token_valid(refresh_token):
            raise TokenExpiredError("Refresh token inválido o expirado")
        
        # Verificar el JWT del refresh token
        payload = verify_token(refresh_token)
        if not payload or payload.get("type") != "refresh":
            raise RefreshTokenError("Refresh token inválido o expirado")
        
        # Obtener el usuario
        user_id = payload.get("sub")
        user = self.user_repository.get_by_id(user_id)
        if not user:
            raise UserNotFoundError("Usuario no encontrado o inactivo")
        
        # Crear nuevo access token
        token_data = {
            "sub": str(user.id),
            "email": user.correo,
            "username": user.nombre_usuario
        }
        
        new_access_token = create_access_token(token_data)
        if not new_access_token:
            raise TokenGenerationError("Error al generar el nuevo access token")
        
        return new_access_token
            
