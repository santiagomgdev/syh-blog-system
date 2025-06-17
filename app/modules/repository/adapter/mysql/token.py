from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import select
from datetime import datetime

from app.core.models.auth.token import Token
from app.modules.repository.adapter.token_repository_interface import TokenRepositoryInterface


class MysqlTokenRepository(TokenRepositoryInterface):
    def __init__(self, db: Session):
        self.db = db

    def get_all(self, skip: int = 0, limit: int = 100) -> List[Token]:
        stmt = select(Token).offset(skip).limit(limit)
        result = self.db.execute(stmt).scalars().all()
        return list(result)
    
    def get_by_id(self, id: int) -> Optional[Token]:
        stmt = select(Token).where(Token.id == id)
        result = self.db.execute(stmt).scalar_one_or_none()
        return result
    
    def create(self, token: Token) -> Token:
        self.db.add(token)
        self.db.commit()
        self.db.refresh(token)
        return token
    
    def update(self, token: Token) -> Token:
        self.db.commit()
        self.db.refresh(token)
        return token

    def delete(self, id: int) -> bool:
        stmt = select(Token).where(Token.id == id)
        token = self.db.execute(stmt).scalar_one_or_none()
        
        if token:
            self.db.delete(token)
            self.db.commit()
            return True
        
        return False

    def get_by_token(self, token_refresco: str) -> Optional[Token]:
        """Obtiene un token por su valor de refresh token"""
        stmt = select(Token).where(Token.token_refresco == token_refresco)
        result = self.db.execute(stmt).scalar_one_or_none()
        return result
    
    def get_by_usuario_id(self, usuario_id: int) -> List[Token]:
        """Obtiene todos los tokens de un usuario específico"""
        stmt = select(Token).where(Token.usuario_id == usuario_id)
        result = self.db.execute(stmt).scalars().all()
        return list(result)
    
    def is_token_valid(self, token_refresco: str) -> bool:
        """Verifica si un token es válido (existe, no está revocado y no ha expirado)"""
        current_time = datetime.now()
        stmt = select(Token).where(
            Token.token_refresco == token_refresco,
            Token.revocado == False,
            Token.expira_en > current_time
        )
        result = self.db.execute(stmt).scalar_one_or_none()
        return result is not None
    
    def revoke_user_token(self, usuario_id: int) -> bool:
        """Revoca todos los tokens de un usuario específico"""
        stmt = select(Token).where(Token.usuario_id == usuario_id)
        tokens = self.db.execute(stmt).scalars().all()
        
        if not tokens:
            return False
        
        for token in tokens:
            token.revocado = True
        
        self.db.commit()
        return True
        