from datetime import datetime, timedelta
from typing import Optional
import bcrypt
# from passlib.context import CryptContext
from jose import JWTError, jwt
from app.core.config import settings

def hash_password(password: str, salt: str) -> str:
    """Hashea una contraseña usando bcrypt."""
    bytes = password.encode('utf-8')
    hash = bcrypt.hashpw(bytes, salt)
    return hash

def generate_salt() -> str:
    """Genera una sal aleatoria para mayor seguridad."""
    salt = bcrypt.gensalt()
    return salt

def verify_password(plain_password: str, hashed_password: bytes) -> bool:
    """Verify a password against its bcrypt hash."""
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create JWT access token."""
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.now + expires_delta
    else:
        expire = datetime.now + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire, "type": "access"})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

def create_refresh_token(data: dict) -> str:
    """Create JWT refresh token."""
    to_encode = data.copy()
    expire = datetime.now + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire, "type": "refresh"})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

def verify_token(token: str) -> Optional[dict]:
    """Verify JWT token and return payload."""
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except JWTError:
        return None