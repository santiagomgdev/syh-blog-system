from datetime import datetime, timedelta, timezone

from app.core.exceptions.auth import InvalidCredentialsError, TokenGenerationError
from app.core.models.auth.token import Token
from app.modules.repository.adapter.user_repository_interface import UsuarioRepositoryInterface
from app.modules.repository.adapter.role_repository_interface import RolUsuarioRepositoryInterface
from app.modules.repository.adapter.token_repository_interface import TokenRepositoryInterface
from app.modules.schemas.v1.user import UsuarioLogin, TokenResponse, UsuarioResponse
from app.utils.security import verify_password, create_access_token, create_refresh_token
from app.core.config import settings


class LoginService:
    def __init__(self, 
                 usuario_repository: UsuarioRepositoryInterface, 
                 role_repository: RolUsuarioRepositoryInterface,
                 token_repository: TokenRepositoryInterface):
        self.usuario_repository = usuario_repository
        self.role_repository = role_repository
        self.token_repository = token_repository

    def authenticate_user(self, login_data: UsuarioLogin) -> UsuarioResponse:
        # Obtiene usuario por nombre de usuario
        user = self.usuario_repository.get_by_nombre_usuario(login_data.nombre_usuario)
        if not user:
            raise InvalidCredentialsError("Credenciales inválidas")
        
        # Verifica contraseña
        if not verify_password(login_data.contrasena, user.contrasena_hash):
            raise InvalidCredentialsError("Credenciales inválidas")
        
        # Actualiza último login
        self.usuario_repository.update(user.id, {"ultimo_login": datetime.now()})
        
        return UsuarioResponse.model_validate(user)
    
    def login(self, login_data: UsuarioLogin) -> TokenResponse:
        # Autentica usuario
        user = self.authenticate_user(login_data)

        self.token_repository.revoke_user_token(user.id)  # Revoca cualquier token existente
        
        # Crear el payload del token
        token_data = {
            "sub": str(user.id),  # subject (user_id)
            "email": user.correo,
            "username": user.nombre_usuario
        }
        
        # Genera tokens
        access_token = create_access_token(token_data)
        refresh_token = create_refresh_token({"sub": str(user.id)})

        if not access_token or not refresh_token:
            raise TokenGenerationError("Error al generar los tokens")

        new_token = Token(
            usuario_id=user.id,
            token_refresco=refresh_token,
            expira_en=datetime.now(timezone.utc) + timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES)
        )

        self.token_repository.create(new_token)
        
        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            user=user
        )
