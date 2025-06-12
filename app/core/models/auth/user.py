from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.orm import relationship
from ..base import Base, TimestampMixin

class Usuario(Base, TimestampMixin):
    __tablename__ = "usuarios"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre_usuario = Column(String(50), nullable=False, unique=True)
    correo = Column(String(100), nullable=False, unique=True, index=True)
    contrasena_hash = Column(String(255), nullable=False)
    sal = Column(String(100), nullable=False)
    activo = Column(Boolean, default=True, nullable=False)
    ultimo_login = Column(DateTime, nullable=True)
    
    tokens = relationship("Token", back_populates="usuario", cascade="all, delete-orphan")
    roles = relationship("RolUsuario", back_populates="usuario", cascade="all, delete-orphan")
    # posts = relationship("Post", back_populates="usuario", cascade="all, delete-orphan")
    # comentarios = relationship("Comentario", back_populates="usuario", cascade="all, delete-orphan")
