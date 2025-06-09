from fastapi import HTTPException
from app.core.models.user.user import Usuario
from app.modules.repository.adapter.user_repository_interface import UsuarioRepositoryInterface
from app.modules.schemas.v1.user import UsuarioCreate


class AuthService():
    def __init__(self, usuario_repository: UsuarioRepositoryInterface):
        self.usuario_repository = usuario_repository

    async def register(self, datos_usuario: UsuarioCreate) -> Usuario:
        # Verifiy if username and psw are not empty
        if not datos_usuario.nombre_usuario or not datos_usuario.contrasena:
            raise HTTPException(status_code=400, detail="Usuario y contraseña son obligatorios")
        
        # Check if user already exists
        existing_user = await self.usuario_repository.get_by_nombre_usuario(datos_usuario.nombre_usuario)
        if existing_user:
            raise HTTPException(status_code=409, detail="Usuario ya existe")
        
        # Create new user
        nuevo_usuario = Usuario(
            nombre_usuario=datos_usuario.nombre_usuario,
            correo=datos_usuario.correo,
            contrasena=datos_usuario.contrasena  # Assuming contrasena is hashed in the model or service
        )
        created_user = await self.usuario_repository.create(nuevo_usuario)
        if not created_user:
            raise HTTPException(status_code=500, detail="Error al crear el usuario")
        return created_user
    
        # Note: The contrasena should be hashed before storing it in the database.
        # This should be handled in the Usuario model or a separate hashing service.
        # Ensure that the contrasena is hashed before saving it to the database.
        