from datetime import datetime, timedelta, timezone

from app.core.exceptions.auth import InvalidCredentialsError, TokenGenerationError
from app.core.models.auth.token import Token
from app.core.models.auth.user import Usuario
from app.modules.repository.adapter.user_repository_interface import UsuarioRepositoryInterface
from app.modules.repository.adapter.role_repository_interface import RolUsuarioRepositoryInterface
from app.modules.repository.adapter.token_repository_interface import TokenRepositoryInterface
from app.utils.security import verify_password, create_refresh_token
from app.core.config import settings


class LoginService:
    def __init__(self, 
                 usuario_repository: UsuarioRepositoryInterface, 
                 role_repository: RolUsuarioRepositoryInterface,
                 token_repository: TokenRepositoryInterface):
        self.usuario_repository = usuario_repository
        self.role_repository = role_repository
        self.token_repository = token_repository

    def authenticate_user(self, username: str, password: str) -> Usuario:
        # Obtiene usuario por nombre de usuario
        user = self.usuario_repository.get_by_nombre_usuario(username)
        if not user:
            raise InvalidCredentialsError("Credenciales inválidas")
        
        # Verifica contraseña
        if not verify_password(password, user.contrasena_hash):
            raise InvalidCredentialsError("Credenciales inválidas")
        
        # Actualiza último login
        self.usuario_repository.update(user.id, {"ultimo_login": datetime.now()})
        
        return user
    
    def create_refresh_token_for_user(self, user: Usuario) -> Token:
        # Revoca cualquier token existente del usuario
        self.token_repository.revoke_user_token(user.id)  # Revoca cualquier token existente
        
        # Genera token de refresco
        refresh_token = create_refresh_token({"sub": str(user.id)})

        if not refresh_token:
            raise TokenGenerationError("Error al generar token de refresco")

        new_token = Token(
            usuario_id=user.id,
            token_refresco=refresh_token,
            expira_en=datetime.now(timezone.utc) + timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES)
        )

        created_token = self.token_repository.create(new_token)
        return created_token
