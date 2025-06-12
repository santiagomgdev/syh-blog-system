from pydantic import BaseModel, EmailStr, field_validator
from typing import Optional
from datetime import datetime

class UsuarioBase(BaseModel):
    nombre_usuario: str
    correo: EmailStr

class UsuarioCreate(UsuarioBase):
    contrasena: str
    
    @field_validator('nombre_usuario')
    @classmethod
    def validate_nombre_usuario(cls, v):
        if not v or len(v) < 1 or len(v) > 100:
            raise ValueError('Nombre debe tener entre 1 y 100 caracteres')
        return v
    
    @field_validator('contrasena')
    @classmethod
    def validate_contrasena(cls, v):
        if len(v) < 8:
            raise ValueError('Contraseña debe tener mínimo 8 caracteres')
        return v

class UsuarioResponse(UsuarioBase):
    id: int
    created_at: datetime
    ultimo_login: Optional[datetime] = None
    
    model_config = {
        "from_attributes": True
    }

class UsuarioLogin(BaseModel):
    nombre_usuario: str
    contrasena: str

class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    user: UsuarioResponse