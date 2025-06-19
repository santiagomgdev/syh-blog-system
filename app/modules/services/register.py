from app.core.exceptions.user import UserAlreadyExistsError
from app.core.models.auth.user import Usuario
from app.modules.repository.adapter.role_repository_interface import RolUsuarioRepositoryInterface
from app.modules.repository.adapter.user_repository_interface import UsuarioRepositoryInterface
from app.modules.schemas.v1.user import UsuarioCreate, UsuarioResponse
from app.utils.security import generate_salt, hash_password


class RegisterService:
    def __init__(self, user_repository: UsuarioRepositoryInterface, role_repository: RolUsuarioRepositoryInterface):
        self.usuario_repository = user_repository
        self.role_repository = role_repository

    def register(self, datos_usuario: UsuarioCreate) -> UsuarioResponse:
        existing_user = self.usuario_repository.get_by_nombre_usuario(datos_usuario.nombre_usuario)
        if existing_user:
            raise UserAlreadyExistsError("El nombre de usuario ya está en uso")
        
        existing_email = self.usuario_repository.get_by_correo(datos_usuario.correo)
        if existing_email:
            raise UserAlreadyExistsError("El correo electrónico ya está en uso")
        
        salt = generate_salt()
        hashed_password = hash_password(datos_usuario.contrasena, salt)

        new_user = Usuario(
            nombre_usuario=datos_usuario.nombre_usuario,
            correo=datos_usuario.correo,
            contrasena_hash=hashed_password,
            sal=salt
        )

        user = self.usuario_repository.create(new_user)

        self.role_repository.assign_role_to_user(user.id, "USER")

        return UsuarioResponse.model_validate(user)
        