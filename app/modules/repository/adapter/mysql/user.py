from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.core.models.auth.user import Usuario
from app.modules.repository.adapter.user_repository_interface import UsuarioRepositoryInterface


class MysqlUsuarioRepository(UsuarioRepositoryInterface):
    def __init__(self, db: Session):
        self.db = db

    def get_all(self, skip: int = 0, limit: int = 100) -> List[Usuario]:
        stmt = select(Usuario).offset(skip).limit(limit)
        result = self.db.execute(stmt).scalars().all()
        return list(result)
    
    def get_by_id(self, id: int) -> Optional[Usuario]:
        stmt = select(Usuario).where(Usuario.id == id)
        result = self.db.execute(stmt).scalar_one_or_none()
        return result
    
    def create(self, usuario: Usuario) -> Usuario:
        self.db.add(usuario)
        self.db.commit()
        self.db.refresh(usuario)
        return usuario
    
    def update(self, id: int, usuario_data: dict) -> Optional[Usuario]:
        stmt = select(Usuario).where(Usuario.id == id)
        user = self.db.execute(stmt).scalar_one_or_none()
        
        if user:
            for key, value in usuario_data.items():
                if hasattr(user, key):
                    setattr(user, key, value)
            
            self.db.commit()
            self.db.refresh(user)
        
        return user

    def delete(self, id: int) -> bool:
        stmt = select(Usuario).where(Usuario.id == id)
        user = self.db.execute(stmt).scalar_one_or_none()
        
        if user:
            self.db.delete(user)
            self.db.commit()
            return True
        
        return False

    def get_by_nombre_usuario(self, nombre_usuario: str) -> Optional[Usuario]:
        stmt = select(Usuario).where(
            Usuario.nombre_usuario == nombre_usuario
        )
        result = self.db.execute(stmt).scalar_one_or_none()
        return result
    
    def get_by_correo(self, correo: str) -> Optional[Usuario]:
        stmt = select(Usuario).where(
            Usuario.correo == correo
        )
        result = self.db.execute(stmt).scalar_one_or_none()
        return result