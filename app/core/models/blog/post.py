from sqlalchemy import Column, String, Text, Integer, ForeignKey, Enum
from sqlalchemy.orm import relationship
import enum
from ..base import CustomBase, TimestampMixin, SoftDeleteMixin

class PostEstado(enum.Enum):
    borrador = "borrador"
    publicado = "publicado"
    archivado = "archivado"

class Post(CustomBase, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "posts"
    
    usuario_id = Column(Integer, ForeignKey("usuarios.id", ondelete="CASCADE"), nullable=False)
    titulo = Column(String(255), nullable=False)
    enlace = Column(String(255), nullable=False, unique=True)
    contenido = Column(Text, nullable=False)
    resumen = Column(Text, nullable=True)
    estado = Column(Enum(PostEstado), default=PostEstado.borrador, nullable=False)
    
    usuario = relationship("Usuario", back_populates="posts")
    comentarios = relationship("Comentario", back_populates="post", cascade="all, delete-orphan")