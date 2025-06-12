# tests/test_user_crud_integration.py
import pytest
from sqlalchemy.exc import IntegrityError

from app.core.models.auth.user import Usuario
from app.modules.repository.adapter.mysql.user import MysqlUsuarioRepository
from app.modules.schemas.v1.user import UsuarioCreate
from app.utils.security import hash_password, generate_salt, verify_password


class TestUserCRUDIntegration:
    """Integration tests using real database"""
    
    @pytest.fixture
    def db_session(self, client):
        """Get database session from test client"""
        from app.core.database.connection import get_db
        db_gen = client.app.dependency_overrides[get_db]()
        db = next(db_gen)
        yield db
        db.close()
    
    @pytest.fixture
    def user_repository(self, db_session):
        """Create user repository with test database session"""
        return MysqlUsuarioRepository(db_session)
    
    def test_create_user_with_hash_integration(self, user_repository):
        """Test creating user with password hashing in database"""
        # Arrange
        user_data = UsuarioCreate(
            nombre_usuario="testuser_db",
            correo="testdb@example.com",
            contrasena="secure_password_123"
        )
        
        # Act - Create user with hashed password
        salt = generate_salt()
        hashed_password = hash_password(user_data.contrasena, salt)
        
        usuario = Usuario(
            nombre_usuario=user_data.nombre_usuario,
            correo=user_data.correo,
            contrasena_hash=hashed_password.decode('utf-8'),
            sal=salt.decode('utf-8')
        )
        
        created_user = user_repository.create(usuario)
        
        # Assert
        assert created_user.id is not None
        assert created_user.nombre_usuario == user_data.nombre_usuario
        assert created_user.correo == user_data.correo
        
        # Verify password verification works
        assert verify_password(user_data.contrasena, hashed_password)
        assert not verify_password("wrong_password", hashed_password)
    
    def test_get_user_by_email_integration(self, user_repository):
        """Test get user by email from database"""
        # Arrange - Create user first
        salt = generate_salt()
        hashed_password = hash_password("test_password", salt)
        
        usuario = Usuario(
            nombre_usuario="emailtest",
            correo="emailtest@example.com",
            contrasena_hash=hashed_password.decode('utf-8'),
            sal=salt.decode('utf-8')
        )
        
        created_user = user_repository.create(usuario)
        
        # Act
        found_user = user_repository.get_by_correo("emailtest@example.com")
        
        # Assert
        assert found_user is not None
        assert found_user.id == created_user.id
        assert found_user.correo == "emailtest@example.com"
        
        # Verify password is stored correctly
        assert verify_password("test_password", found_user.contrasena_hash.encode('utf-8'))
    
    def test_get_user_by_id_integration(self, user_repository):
        """Test get user by ID from database"""
        # Arrange
        salt = generate_salt()
        hashed_password = hash_password("test_password", salt)
        
        usuario = Usuario(
            nombre_usuario="idtest",
            correo="idtest@example.com",
            contrasena_hash=hashed_password.decode('utf-8'),
            sal=salt.decode('utf-8')
        )
        
        created_user = user_repository.create(usuario)
        
        # Act
        found_user = user_repository.get_by_id(created_user.id)
        
        # Assert
        assert found_user is not None
        assert found_user.id == created_user.id
        assert found_user.nombre_usuario == "idtest"
    
    def test_duplicate_email_error_handling(self, user_repository):
        """Test duplicate email constraint violation"""
        # Arrange - Create first user
        salt1 = generate_salt()
        hashed_password1 = hash_password("password1", salt1)
        
        usuario1 = Usuario(
            nombre_usuario="user1",
            correo="duplicate@example.com",
            contrasena_hash=hashed_password1.decode('utf-8'),
            sal=salt1.decode('utf-8')
        )
        
        user_repository.create(usuario1)
        
        # Act & Assert - Try duplicate email
        salt2 = generate_salt()
        hashed_password2 = hash_password("password2", salt2)
        
        usuario2 = Usuario(
            nombre_usuario="user2",
            correo="duplicate@example.com",  # Same email
            contrasena_hash=hashed_password2.decode('utf-8'),
            sal=salt2.decode('utf-8')
        )
        
        with pytest.raises(IntegrityError):
            user_repository.create(usuario2)
    
    def test_complete_user_flow_integration(self, user_repository):
        """Test complete flow: create, retrieve, verify password"""
        # Arrange
        original_password = "flow_password_123"
        user_data = UsuarioCreate(
            nombre_usuario="flow_user",
            correo="flow@example.com",
            contrasena=original_password
        )
        
        # Act 1 - Create user
        salt = generate_salt()
        hashed_password = hash_password(user_data.contrasena, salt)
        
        usuario = Usuario(
            nombre_usuario=user_data.nombre_usuario,
            correo=user_data.correo,
            contrasena_hash=hashed_password.decode('utf-8'),
            sal=salt.decode('utf-8')
        )
        
        created_user = user_repository.create(usuario)
        
        # Act 2 - Retrieve by email
        retrieved_user = user_repository.get_by_correo(user_data.correo)
        
        # Act 3 - Retrieve by ID
        retrieved_by_id = user_repository.get_by_id(created_user.id)
        
        # Act 4 - Verify password
        password_valid = verify_password(
            original_password, 
            retrieved_user.contrasena_hash.encode('utf-8')
        )
        wrong_password_valid = verify_password(
            "wrong_password", 
            retrieved_user.contrasena_hash.encode('utf-8')
        )
        
        # Assert
        assert created_user.id is not None
        assert retrieved_user is not None
        assert retrieved_by_id is not None
        assert retrieved_user.id == created_user.id
        assert retrieved_by_id.id == created_user.id
        assert password_valid is True
        assert wrong_password_valid is False