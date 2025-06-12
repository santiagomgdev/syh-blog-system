from datetime import datetime
from fastapi import HTTPException, status

from app.modules.repository.adapter.user_repository_interface import UsuarioRepositoryInterface
from app.modules.repository.adapter.role_repository_interface import RolUsuarioRepositoryInterface
from app.modules.repository.adapter.token_repository_interface import TokenRepositoryInterface
from app.modules.schemas.v1.user import UsuarioLogin, TokenResponse, UsuarioResponse
from app.utils.security import verify_password, create_access_token, create_refresh_token


class LoginService:
    def __init__(self, 
                 usuario_repository: UsuarioRepositoryInterface, 
                 role_repository: RolUsuarioRepositoryInterface,
                 token_repository: TokenRepositoryInterface):
        self.usuario_repository = usuario_repository
        self.role_repository = role_repository
        self.token_repository = token_repository

    def authenticate_user(self, login_data: UsuarioLogin) -> UsuarioResponse:
        # Fetch user by email
        user = self.usuario_repository.get_by_nombre_usuario(login_data.nombre_usuario)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Credenciales inválidas"
            )
        
        # Verify password
        if not verify_password(login_data.contrasena, user.contrasena_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Credenciales inválidas"
            )
        
        # Update last login
        self.usuario_repository.update(user.id, {"ultimo_login": datetime.now()})
        
        return UsuarioResponse.model_validate(user)
    
    def login(self, login_data: UsuarioLogin) -> TokenResponse:
        # Authenticate user
        user = self.authenticate_user(login_data)
        
        # Create token payload
        token_data = {
            "sub": str(user.id),  # subject (user_id)
            "email": user.correo,
            "username": user.nombre_usuario
        }
        
        # Generate tokens
        access_token = create_access_token(token_data)
        refresh_token = create_refresh_token({"sub": str(user.id)})

        self.token_repository.create(
            usuario_id=user.id,
            token_refresco=access_token,
            expiracion=datetime.now() # Example expiration time (Pendiente por ajuste)
        )

        if not access_token or not refresh_token:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error al generar los tokens"
            )
        
        # Return response
        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            user=user
        )
