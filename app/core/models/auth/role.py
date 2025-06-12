from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from ..base import Base

class RolUsuario(Base):
    __tablename__ = "roles_usuario"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id", ondelete="CASCADE"), nullable=False)
    nombre_rol = Column(String(50), nullable=False)
    
    usuario = relationship("Usuario", back_populates="roles")
