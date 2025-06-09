from sqlalchemy import Column, Text, Integer, ForeignKey, Enum
from sqlalchemy.orm import relationship
import enum
from ..base import CustomBase, TimestampMixin

class ComentarioEstado(enum.Enum):
    pendiente = "pendiente"
    aprobado = "aprobado"
    spam = "spam"
    rechazado = "rechazado"

class Comentario(CustomBase, TimestampMixin):
    __tablename__ = "comentarios"
    
    post_id = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"), nullable=False)
    usuario_id = Column(Integer, ForeignKey("usuarios.id", ondelete="CASCADE"), nullable=False)
    padre_id = Column(Integer, ForeignKey("comentarios.id", ondelete="CASCADE"), nullable=True)
    contenido = Column(Text, nullable=False)
    estado = Column(Enum(ComentarioEstado), default=ComentarioEstado.pendiente, nullable=False)
    
    post = relationship("Post", back_populates="comentarios")
    usuario = relationship("Usuario", back_populates="comentarios")
    padre = relationship("Comentario", remote_side=[CustomBase.id], backref="respuestas")