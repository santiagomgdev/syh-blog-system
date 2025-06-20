from app.core.exceptions.user import UserAlreadyExistsError
from app.core.models.auth.role import RolUsuario
from app.core.models.auth.user import Usuario
from app.modules.repository.adapter.role_repository_interface import RolUsuarioRepositoryInterface
from app.modules.repository.adapter.user_repository_interface import UsuarioRepositoryInterface
from app.utils.security import generate_salt, hash_password


class RegisterService:
    def __init__(self, user_repository: UsuarioRepositoryInterface, role_repository: RolUsuarioRepositoryInterface):
        self.usuario_repository = user_repository
        self.role_repository = role_repository

    def register(self, username: str, email: str, psw: str) -> Usuario:
        """Registra un nuevo usuario en el sistema."""
        
        existing_user = self.usuario_repository.get_by_nombre_usuario(username)
        if existing_user:
            raise UserAlreadyExistsError("El nombre de usuario ya está en uso")
        
        existing_email = self.usuario_repository.get_by_correo(email)
        if existing_email:
            raise UserAlreadyExistsError("El correo electrónico ya está en uso")
        
        salt = generate_salt()
        hashed_password = hash_password(psw, salt)

        new_user = Usuario(
            nombre_usuario=username,
            correo=email,
            contrasena_hash=hashed_password,
            sal=salt
        )

        user = self.usuario_repository.create(new_user)
        return user
    
    def assign_default_role(self, user_id: int) -> RolUsuario:
        """Asigna el rol por defecto al usuario recién registrado."""

        return self.role_repository.assign_role_to_user(user_id, 'USER')
        