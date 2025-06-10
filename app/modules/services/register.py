from fastapi import HTTPException

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
            raise HTTPException(status_code=409, detail={
                "message": "El nombre de usuario ya está en uso",
                "error_code": "USERNAME_IN_USE",
                "field": "nombre_usuario",
                "value": datos_usuario.nombre_usuario
            })
        
        existing_email = self.usuario_repository.get_by_correo(datos_usuario.correo)
        if existing_email:
            raise HTTPException(status_code=409, detail={
                "message": "El correo electrónico ya está en uso",
                "error_code": "EMAIL_IN_USE",
                "field": "correo",
                "value": datos_usuario.correo
            })
        
        salt = generate_salt()
        hashed_password = hash_password(datos_usuario.contrasena, salt)

        new_user = Usuario(
            nombre_usuario=datos_usuario.nombre_usuario,
            correo=datos_usuario.correo,
            contrasena_hash=hashed_password,
            sal=salt
        )

        user = self.usuario_repository.create(new_user)
        if not user:
            raise HTTPException(status_code=500, detail="Error al crear el usuario")
        
        self.role_repository.assign_role_to_user(user.id, "USER")

        return UsuarioResponse.model_validate(user)
        