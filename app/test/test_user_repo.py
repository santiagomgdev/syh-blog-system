# tests/test_user_crud.py
import pytest
from unittest.mock import Mock, patch
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.core.models.auth.user import Usuario
from app.modules.repository.adapter.mysql.user import MysqlUsuarioRepository
from app.modules.schemas.v1.user import UsuarioCreate
from app.utils.security import hash_password, generate_salt, verify_password


class TestUserCRUD:
    """Unit tests for user CRUD operations"""
    
    def setup_method(self):
        """Setup test fixtures"""
        self.mock_db = Mock(spec=Session)
        self.repository = MysqlUsuarioRepository(self.mock_db)
    
    def test_create_user_success(self):
        """Test creating user with password hashing"""
        # Arrange
        user_data = UsuarioCreate(
            nombre_usuario="testuser",
            correo="test@example.com",
            contrasena="password123"
        )
        
        # Mock database operations
        self.mock_db.add.return_value = None
        self.mock_db.commit.return_value = None
        self.mock_db.refresh.return_value = None
        
        # Act - Create user with hash
        salt = generate_salt()
        hashed_password = hash_password(user_data.contrasena, salt)
        
        usuario = Usuario(
            nombre_usuario=user_data.nombre_usuario,
            correo=user_data.correo,
            contrasena_hash=hashed_password.decode('utf-8'),
            sal=salt.decode('utf-8')
        )
        
        result = self.repository.create(usuario)
        
        # Assert
        self.mock_db.add.assert_called_once_with(usuario)
        self.mock_db.commit.assert_called_once()
        self.mock_db.refresh.assert_called_once_with(usuario)
        
        # Verify hash integration
        assert verify_password(user_data.contrasena, hashed_password)
        assert not verify_password("wrong_password", hashed_password)
    
    def test_get_user_by_email_found(self):
        """Test get user by email when exists"""
        # Arrange
        email = "test@example.com"
        expected_user = Usuario(
            id=1,
            nombre_usuario="testuser",
            correo=email,
            contrasena_hash="hashed_password",
            sal="test_salt"
        )
        
        mock_result = Mock()
        mock_result.scalar_one_or_none.return_value = expected_user
        self.mock_db.execute.return_value = mock_result
        
        # Act
        result = self.repository.get_by_correo(email)
        
        # Assert
        assert result == expected_user
        self.mock_db.execute.assert_called_once()
    
    def test_get_user_by_email_not_found(self):
        """Test get user by email when doesn't exist"""
        # Arrange
        mock_result = Mock()
        mock_result.scalar_one_or_none.return_value = None
        self.mock_db.execute.return_value = mock_result
        
        # Act
        result = self.repository.get_by_correo("nonexistent@example.com")
        
        # Assert
        assert result is None
    
    def test_get_user_by_id_found(self):
        """Test get user by ID when exists"""
        # Arrange
        user_id = 1
        expected_user = Usuario(
            id=user_id,
            nombre_usuario="testuser",
            correo="test@example.com",
            contrasena_hash="hashed_password",
            sal="test_salt"
        )
        
        mock_result = Mock()
        mock_result.scalar_one_or_none.return_value = expected_user
        self.mock_db.execute.return_value = mock_result
        
        # Act
        result = self.repository.get_by_id(user_id)
        
        # Assert
        assert result == expected_user
        self.mock_db.execute.assert_called_once()
    
    def test_get_user_by_id_not_found(self):
        """Test get user by ID when doesn't exist"""
        # Arrange
        mock_result = Mock()
        mock_result.scalar_one_or_none.return_value = None
        self.mock_db.execute.return_value = mock_result
        
        # Act
        result = self.repository.get_by_id(999)
        
        # Assert
        assert result is None
    
    def test_create_user_duplicate_email_error(self):
        """Test handling duplicate email constraint"""
        # Arrange
        self.mock_db.commit.side_effect = IntegrityError("duplicate key", None, None)
        
        salt = generate_salt()
        hashed_password = hash_password("password123", salt)
        
        usuario = Usuario(
            nombre_usuario="testuser",
            correo="duplicate@example.com",
            contrasena_hash=hashed_password.decode('utf-8'),
            sal=salt.decode('utf-8')
        )
        
        # Act & Assert
        with pytest.raises(IntegrityError):
            self.repository.create(usuario)


class TestPasswordHashing:
    """Test password hashing functions"""
    
    def test_generate_salt(self):
        """Test salt generation"""
        salt1 = generate_salt()
        salt2 = generate_salt()
        
        assert salt1 != salt2
        assert isinstance(salt1, bytes)
        assert len(salt1) > 0
    
    def test_hash_password(self):
        """Test password hashing"""
        password = "test_password"
        salt = generate_salt()
        
        hash1 = hash_password(password, salt)
        hash2 = hash_password(password, salt)
        
        assert hash1 == hash2
        assert isinstance(hash1, bytes)
        assert hash1 != password.encode('utf-8')
    
    def test_verify_password_correct(self):
        """Test password verification with correct password"""
        password = "correct_password"
        salt = generate_salt()
        hashed = hash_password(password, salt)
        
        assert verify_password(password, hashed) is True
    
    def test_verify_password_incorrect(self):
        """Test password verification with incorrect password"""
        password = "correct_password"
        wrong_password = "wrong_password"
        salt = generate_salt()
        hashed = hash_password(password, salt)
        
        assert verify_password(wrong_password, hashed) is False


class TestHashIntegration:
    """Test CRUD integration with password hashing"""
    
    def test_create_and_verify_user_password(self):
        """Test complete flow: create user and verify password"""
        # Arrange
        mock_db = Mock(spec=Session)
        repository = MysqlUsuarioRepository(mock_db)
        
        user_data = UsuarioCreate(
            nombre_usuario="hashtest",
            correo="hash@example.com",
            contrasena="secure_password"
        )
        
        mock_db.add.return_value = None
        mock_db.commit.return_value = None
        mock_db.refresh.return_value = None
        
        # Act - Create user with hashed password
        salt = generate_salt()
        hashed_password = hash_password(user_data.contrasena, salt)
        
        usuario = Usuario(
            nombre_usuario=user_data.nombre_usuario,
            correo=user_data.correo,
            contrasena_hash=hashed_password.decode('utf-8'),
            sal=salt.decode('utf-8')
        )
        
        repository.create(usuario)
        
        # Assert - Verify password verification works
        assert verify_password(user_data.contrasena, hashed_password)
        assert not verify_password("wrong_password", hashed_password)
        
        # Verify database operations called
        mock_db.add.assert_called_once_with(usuario)
        mock_db.commit.assert_called_once()
        mock_db.refresh.assert_called_once_with(usuario)
    
    def test_login_simulation(self):
        """Test simulated login flow with hash verification"""
        # Arrange - Simulate existing user
        original_password = "login_password"
        salt = generate_salt()
        stored_hash = hash_password(original_password, salt)
        
        existing_user = Usuario(
            id=1,
            nombre_usuario="loginuser",
            correo="login@example.com",
            contrasena_hash=stored_hash.decode('utf-8'),
            sal=salt.decode('utf-8')
        )
        
        mock_db = Mock(spec=Session)
        repository = MysqlUsuarioRepository(mock_db)
        
        mock_result = Mock()
        mock_result.scalar_one_or_none.return_value = existing_user
        mock_db.execute.return_value = mock_result
        
        # Act - Simulate login
        user = repository.get_by_correo("login@example.com")
        
        # Verify correct password
        correct_login = verify_password(
            original_password, 
            user.contrasena_hash.encode('utf-8')
        )
        
        # Verify wrong password
        wrong_login = verify_password(
            "wrong_password", 
            user.contrasena_hash.encode('utf-8')
        )
        
        # Assert
        assert user is not None
        assert correct_login is True
        assert wrong_login is False