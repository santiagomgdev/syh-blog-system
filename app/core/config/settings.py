from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # Configuracion BD
    DATABASE_URL: str
    DATABASE_HOST: str
    DATABASE_PORT: int
    DATABASE_USER: str
    DATABASE_PASSWORD: str
    DATABASE_NAME: str
    
    # Configuracion Seguridad
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    REFRESH_TOKEN_EXPIRE_MINUTES: int
    
    # Configuracion Aplicacion
    APP_NAME: str
    DEBUG: bool
    VERSION: str
    
    # Configuracion CORS
    ALLOWED_ORIGINS: list
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()