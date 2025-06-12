from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.core.models.auth.role import RolUsuario
from app.modules.repository.adapter.role_repository_interface import RolUsuarioRepositoryInterface

class MysqlRolUsuarioRepository(RolUsuarioRepositoryInterface):
    def __init__(self, db: Session):
        self.db = db

    def get_all(self, skip: int = 0, limit: int = 100) -> List[RolUsuario]:
        stmt = select(RolUsuario).offset(skip).limit(limit)
        result = self.db.execute(stmt).scalars().all()
        return list(result)

    def get_by_id(self, id: int) -> Optional[RolUsuario]:
        stmt = select(RolUsuario).where(RolUsuario.id == id)
        result = self.db.execute(stmt).scalar_one_or_none()
        return result

    def create(self, rol_usuario: RolUsuario) -> RolUsuario:
        self.db.add(rol_usuario)
        self.db.commit()
        self.db.refresh(rol_usuario)
        return rol_usuario

    def update(self, id: int, rol_usuario_data: dict) -> Optional[RolUsuario]:
        return 'No implementado'

    def delete(self, id: int) -> bool:
        stmt = select(RolUsuario).where(RolUsuario.id == id)
        rol_usuario = self.db.execute(stmt).scalar_one_or_none()

        if rol_usuario:
            self.db.delete(rol_usuario)
            self.db.commit()
            return True

        return False

    def assign_role_to_user(self, usuario_id: int, nombre_rol: str) -> RolUsuario:
        new_role = RolUsuario(usuario_id=usuario_id, nombre_rol=nombre_rol)
        return self.create(new_role)
