"""Unit tests for user Pydantic schemas."""

import pytest
from pydantic import ValidationError
from datetime import datetime
from app.modules.schemas.v1.user import (
    UsuarioBase,
    UsuarioCreate, 
    UsuarioResponse, 
    UsuarioLogin, 
    TokenResponse
)


class TestUsuarioBaseSchema:
    """Test UsuarioBase schema."""
    
    def test_valid_usuario_base(self):
        """Test valid UsuarioBase creation."""
        user_data = {
            "nombre_usuario": "testuser",
            "correo": "test@example.com"
        }
        
        user = UsuarioBase(**user_data)
        assert user.nombre_usuario == "testuser"
        assert user.correo == "test@example.com"
    
    def test_invalid_email_format(self):
        """Test invalid email format in UsuarioBase."""
        user_data = {
            "nombre_usuario": "testuser",
            "correo": "invalid-email"
        }
        
        with pytest.raises(ValidationError) as exc_info:
            UsuarioBase(**user_data)
        assert "value is not a valid email address" in str(exc_info.value)


class TestUsuarioCreateSchema:
    """Test UsuarioCreate schema validation."""
    
    def test_valid_usuario_create(self):
        """Test valid UsuarioCreate with all fields."""
        user_data = {
            "nombre_usuario": "test_user123",
            "correo": "test@example.com",
            "contrasena": "password123"
        }
        
        user = UsuarioCreate(**user_data)
        assert user.nombre_usuario == "test_user123"
        assert user.correo == "test@example.com"
        assert user.contrasena == "password123"
    
    def test_username_too_short(self):
        """Test username validation - too short."""
        user_data = {
            "nombre_usuario": "",
            "correo": "test@example.com",
            "contrasena": "password123"
        }
        
        with pytest.raises(ValidationError) as exc_info:
            UsuarioCreate(**user_data)
        assert "entre 1 y 100 caracteres" in str(exc_info.value)
    
    def test_username_too_long(self):
        """Test username validation - too long."""
        user_data = {
            "nombre_usuario": "a" * 101,  # 101 characters
            "correo": "test@example.com",
            "contrasena": "password123"
        }
        
        with pytest.raises(ValidationError) as exc_info:
            UsuarioCreate(**user_data)
        assert "entre 1 y 100 caracteres" in str(exc_info.value)
    
    def test_password_too_short(self):
        """Test password validation - too short."""
        user_data = {
            "nombre_usuario": "testuser",
            "correo": "test@example.com",
            "contrasena": "123"  # Only 3 characters
        }
        
        with pytest.raises(ValidationError) as exc_info:
            UsuarioCreate(**user_data)
        assert "mínimo 8 caracteres" in str(exc_info.value)
    
    def test_valid_minimum_password(self):
        """Test password with exactly 8 characters (minimum)."""
        user_data = {
            "nombre_usuario": "testuser",
            "correo": "test@example.com",
            "contrasena": "12345678"  # Exactly 8 characters
        }
        
        user = UsuarioCreate(**user_data)
        assert user.contrasena == "12345678"
    
    def test_missing_required_fields(self):
        """Test validation with missing required fields."""
        # Missing password
        with pytest.raises(ValidationError) as exc_info:
            UsuarioCreate(nombre_usuario="test", correo="test@example.com")
        assert "field required" in str(exc_info.value).lower()
        
        # Missing email
        with pytest.raises(ValidationError) as exc_info:
            UsuarioCreate(nombre_usuario="test", contrasena="password123")
        assert "field required" in str(exc_info.value).lower()
        
        # Missing username
        with pytest.raises(ValidationError) as exc_info:
            UsuarioCreate(correo="test@example.com", contrasena="password123")
        assert "field required" in str(exc_info.value).lower()
    
    def test_email_format_validation(self):
        """Test various email format validations."""
        base_data = {
            "nombre_usuario": "testuser",
            "contrasena": "password123"
        }
        
        # Valid emails should work
        valid_emails = [
            "test@example.com",
            "user.name@domain.co.uk",
            "test+tag@example.org"
        ]
        
        for email in valid_emails:
            user = UsuarioCreate(correo=email, **base_data)
            assert user.correo == email
        
        # Invalid emails should fail
        invalid_emails = [
            "notanemail",
            "@example.com",
            "test@",
            "test.example.com"
        ]
        
        for email in invalid_emails:
            with pytest.raises(ValidationError):
                UsuarioCreate(correo=email, **base_data)


class TestUsuarioLoginSchema:
    """Test UsuarioLogin schema validation."""
    
    def test_valid_login(self):
        """Test valid login data."""
        login_data = {
            "correo": "test@example.com",
            "contrasena": "password123"
        }
        
        login = UsuarioLogin(**login_data)
        assert login.correo == "test@example.com"
        assert login.contrasena == "password123"
    
    def test_missing_password(self):
        """Test login with missing password."""
        with pytest.raises(ValidationError) as exc_info:
            UsuarioLogin(correo="test@example.com")
        assert "field required" in str(exc_info.value).lower()
    
    def test_missing_email(self):
        """Test login with missing email."""
        with pytest.raises(ValidationError) as exc_info:
            UsuarioLogin(contrasena="password123")
        assert "field required" in str(exc_info.value).lower()
    
    def test_invalid_email_login(self):
        """Test login with invalid email format."""
        login_data = {
            "correo": "invalid-email",
            "contrasena": "password123"
        }
        
        with pytest.raises(ValidationError):
            UsuarioLogin(**login_data)


class TestUsuarioResponseSchema:
    """Test UsuarioResponse schema serialization."""
    
    def test_valid_usuario_response(self):
        """Test valid UsuarioResponse creation."""
        response_data = {
            "id": 1,
            "nombre_usuario": "testuser",
            "correo": "test@example.com",
            "created_at": datetime(2024, 1, 1, 10, 0, 0),
            "updated_at": datetime(2024, 1, 1, 10, 0, 0),
            "ultimo_login": datetime(2024, 1, 15, 14, 30, 0)
        }
        
        response = UsuarioResponse(**response_data)
        assert response.id == 1
        assert response.nombre_usuario == "testuser"
        assert response.correo == "test@example.com"
        assert response.created_at == datetime(2024, 1, 1, 10, 0, 0)
        assert response.ultimo_login == datetime(2024, 1, 15, 14, 30, 0)
    
    def test_usuario_response_with_null_ultimo_login(self):
        """Test UsuarioResponse with null ultimo_login."""
        response_data = {
            "id": 1,
            "nombre_usuario": "testuser",
            "correo": "test@example.com",
            "created_at": datetime(2024, 1, 1, 10, 0, 0),
            "updated_at": datetime(2024, 1, 1, 10, 0, 0),
            "ultimo_login": None
        }
        
        response = UsuarioResponse(**response_data)
        assert response.ultimo_login is None
    
    def test_usuario_response_missing_required_fields(self):
        """Test UsuarioResponse with missing required fields."""
        # Missing id
        with pytest.raises(ValidationError):
            UsuarioResponse(
                nombre_usuario="test",
                correo="test@example.com",
                created_at=datetime.now(),
                updated_at=datetime.now()
            )
        
        # Missing timestamps
        with pytest.raises(ValidationError):
            UsuarioResponse(
                id=1,
                nombre_usuario="test",
                correo="test@example.com"
            )
    
    def test_usuario_response_excludes_sensitive_fields(self):
        """Ensure UsuarioResponse doesn't include sensitive fields."""
        # Verify that sensitive fields are not in the schema
        schema_fields = set(UsuarioResponse.model_fields.keys())
        sensitive_fields = {
            "contrasena", "contrasena_hash", "sal", "password", "hash"
        }
        
        # No sensitive fields should be present
        assert not any(field in schema_fields for field in sensitive_fields)
        
        # Verify expected fields are present
        expected_fields = {
            "id", "nombre_usuario", "correo", "created_at", "updated_at", "ultimo_login"
        }
        assert expected_fields.issubset(schema_fields)


class TestTokenResponseSchema:
    """Test TokenResponse schema."""
    
    def test_valid_token_response(self):
        """Test valid TokenResponse creation."""
        user_data = {
            "id": 1,
            "nombre_usuario": "testuser",
            "correo": "test@example.com",
            "created_at": datetime(2024, 1, 1, 10, 0, 0),
            "updated_at": datetime(2024, 1, 1, 10, 0, 0),
            "ultimo_login": None
        }
        
        token_data = {
            "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.test",
            "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.refresh",
            "token_type": "bearer",
            "user": UsuarioResponse(**user_data)
        }
        
        token_response = TokenResponse(**token_data)
        assert token_response.access_token.startswith("eyJ0eXAiOiJKV1Qi")
        assert token_response.refresh_token.startswith("eyJ0eXAiOiJKV1Qi")
        assert token_response.token_type == "bearer"
        assert token_response.user.id == 1
        assert token_response.user.nombre_usuario == "testuser"
    
    def test_token_response_default_token_type(self):
        """Test TokenResponse default token_type."""
        user_data = {
            "id": 1,
            "nombre_usuario": "testuser",
            "correo": "test@example.com",
            "created_at": datetime.now(),
            "updated_at": datetime.now(),
            "ultimo_login": None
        }
        
        token_data = {
            "access_token": "test_token",
            "refresh_token": "refresh_token",
            "user": UsuarioResponse(**user_data)
        }
        
        token_response = TokenResponse(**token_data)
        assert token_response.token_type == "bearer"  # Default value
    
    def test_token_response_missing_required_fields(self):
        """Test TokenResponse with missing required fields."""
        user_data = {
            "id": 1,
            "nombre_usuario": "testuser",
            "correo": "test@example.com",
            "created_at": datetime.now(),
            "updated_at": datetime.now()
        }
        
        # Missing access_token
        with pytest.raises(ValidationError):
            TokenResponse(
                refresh_token="refresh_token",
                user=UsuarioResponse(**user_data)
            )
        
        # Missing user
        with pytest.raises(ValidationError):
            TokenResponse(
                access_token="access_token",
                refresh_token="refresh_token"
            )


class TestSchemaIntegration:
    """Test schema integration and edge cases."""
    
    def test_create_to_response_flow(self):
        """Test typical flow from create to response schema."""
        # Create user data
        create_data = {
            "nombre_usuario": "integration_test",
            "correo": "integration@example.com",
            "contrasena": "password123"
        }
        
        user_create = UsuarioCreate(**create_data)
        
        # Simulate response data (what would come from database)
        response_data = {
            "id": 42,
            "nombre_usuario": user_create.nombre_usuario,
            "correo": user_create.correo,
            "created_at": datetime.now(),
            "updated_at": datetime.now(),
            "ultimo_login": None
        }
        
        user_response = UsuarioResponse(**response_data)
        
        # Verify data consistency
        assert user_response.nombre_usuario == user_create.nombre_usuario
        assert user_response.correo == user_create.correo
        assert user_response.id == 42
        
        # Verify password is not in response
        assert not hasattr(user_response, 'contrasena')
    
    def test_email_case_sensitivity(self):
        """Test email handling across schemas."""
        email_variants = [
            "Test@Example.Com",
            "TEST@EXAMPLE.COM",
            "test@example.com"
        ]
        
        for email in email_variants:
            # Should work in all schemas
            UsuarioCreate(
                nombre_usuario="test",
                correo=email,
                contrasena="password123"
            )
            
            UsuarioLogin(correo=email, contrasena="password123")
            
            UsuarioResponse(
                id=1,
                nombre_usuario="test",
                correo=email,
                created_at=datetime.now(),
                updated_at=datetime.now()
            )