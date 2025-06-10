from datetime import datetime, timedelta
from typing import Optional
import bcrypt
# from passlib.context import CryptContext
# from jose import JWTError, jwt
# from app.core.config import settings

def hash_password(password: str, salt: str) -> str:
    """Hashea una contraseña usando bcrypt."""
    bytes = password.encode('utf-8')
    hash = bcrypt.hashpw(bytes, salt)
    return hash

def generate_salt() -> str:
    """Genera una sal aleatoria para mayor seguridad."""
    salt = bcrypt.gensalt()
    return salt