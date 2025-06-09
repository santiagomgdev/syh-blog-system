from sqlalchemy.orm import Session
from app.core.models.base import Base
# from app.core.models.blog.post import Post
# from app.core.models.blog.comment import Comentario
# from app.core.models.user.user import Usuario
# from app.core.models.user.token import Token
# from app.core.models.user.role import RolUsuario

from app.core.database.connection import engine
import logging

logger = logging.getLogger(__name__)

def create_tables():
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("Tablas de base de datos creadas exitosamente.")
    except Exception as e:
        logger.error(f"Error en creacion de tablas: {e}")
        raise
