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

# Operaciones de base de datos para crear, eliminar tablas y verificar conexión
# Utilizar unicamente en entorno de desarrollo o pruebas

def create_tables():
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("Tablas de base de datos creadas exitosamente.")
    except Exception as e:
        logger.error(f"Error en creacion de tablas: {e}")
        raise

def drop_all_tables():
    try:
        Base.metadata.drop_all(bind=engine)
        logger.info("Todas las tablas de la base de datos han sido eliminadas.")
    except Exception as e:
        logger.error(f"Error al eliminar tablas: {e}")
        raise

def check_database_connection():
    try:
        with Session(engine) as session:
            session.execute("SELECT 1")
        logger.info("Conexión a la base de datos exitosa.")
    except Exception as e:
        logger.error(f"Error al conectar a la base de datos: {e}")
        raise
