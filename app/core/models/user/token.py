from sqlalchemy import Column, String, DateTime, Integer, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from ..base import CustomBase

class Token(CustomBase):
    __tablename__ = "tokens"
    
    usuario_id = Column(Integer, ForeignKey("usuarios.id", ondelete="CASCADE"), nullable=False)
    token_refresco = Column(String(255), nullable=False)
    emitido_en = Column(DateTime, default=datetime.now, nullable=False)
    expira_en = Column(DateTime, nullable=False)
    revocado = Column(Boolean, default=False, nullable=False)
    
    usuario = relationship("Usuario", back_populates="tokens")