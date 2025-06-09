from typing import List
from sqlalchemy import select

from app.core.models.user.user import Usuario
from app.modules.repository.adapter.user_repository_interface import UsuarioRepositoryInterface

class PostgresUsuarioRepository(UsuarioRepositoryInterface):
    def __init__(self, db):
        self.db = db

    def get_all (self, skip: int = 0, limit: int = 100) -> List[Usuario]:
        query = "SELECT * FROM users ORDER BY id OFFSET $1 LIMIT $2"
        result = self.db.fetch_all(query, (skip, limit))
        return result
    
    def get_by_id(self, id: int) -> Usuario:
        stmt = select(Usuario).where(Usuario.id == id)
        # Retorna un solo registro y devuelve error si encuentra multiples registros
        result = self.db.execute(stmt).scalar_one_or_none()
        return result
    
    def create(self, usuario: Usuario) -> Usuario:
        query = "INSERT INTO users (name, email) VALUES ($1, $2) RETURNING id"
        result = self.db.fetch_one(query, (usuario.name, usuario.email))
        usuario.id = result['id']
        return usuario
    
    def update(self, id: int, usuario: Usuario) -> Usuario:
        return 'not implemented'

    def delete(self, id: int) -> bool:
        return 'not implemented'

    # Pueden ser async???
    # def get_user_by_id(self, user_id: str):
    #     query = "SELECT * FROM users WHERE id = $1"
    #     result = self.db.fetch_one(query, (user_id,))
    #     return result
    
    def get_user_by_nombre_usuario(self, nombre_usuario: str):
        query = "SELECT * FROM users WHERE username = $1"
        result = self.db.fetch_one(query, (nombre_usuario,))
        return result

    # def create_user(self, user_data: dict):
    #     query = "INSERT INTO users (name, email) VALUES ($1, $2) RETURNING id"
    #     result = self.db.fetch_one(query, (user_data['name'], user_data['email']))
    #     return result['id']