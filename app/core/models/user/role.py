from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from ..base import CustomBase

class RolUsuario(CustomBase):
    __tablename__ = "roles_usuario"
    
    usuario_id = Column(Integer, ForeignKey("usuarios.id", ondelete="CASCADE"), nullable=False)
    nombre_rol = Column(String(50), nullable=False)
    
    usuario = relationship("Usuario", back_populates="roles")