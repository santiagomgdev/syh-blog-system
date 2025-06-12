# tests/test_security.py
import pytest
import time
from app.core.models.auth.user import Usuario
from app.utils.security import hash_password, generate_salt, verify_password

def test_password_hashing():
    password = "test_password_123"
    salt = generate_salt()
    hashed = hash_password(password, salt)
    
    # Hash should not be the same as original password
    assert hashed != password.encode('utf-8')
    # Hash should be bytes
    assert isinstance(hashed, bytes)
    
def test_password_verification():
    password = "test_password_123"
    salt = generate_salt()
    hashed = hash_password(password, salt)
    
    # Correct password should verify
    assert verify_password(password, hashed) is True
    # Wrong password should not verify
    assert verify_password("wrong_password", hashed) is False

def test_different_passwords_different_hashes():
    password1 = "password123"
    password2 = "password456"
    salt = generate_salt()
    
    hash1 = hash_password(password1, salt)
    hash2 = hash_password(password2, salt)
    
    # Different passwords should produce different hashes
    assert hash1 != hash2

def test_same_password_different_salts():
    password = "same_password"
    salt1 = generate_salt()
    salt2 = generate_salt()
    
    hash1 = hash_password(password, salt1)
    hash2 = hash_password(password, salt2)
    
    # Same password with different salts should produce different hashes
    assert hash1 != hash2
    # But both should verify correctly
    assert verify_password(password, hash1)
    assert verify_password(password, hash2)

def test_user_password_integration():
    # Test that password gets hashed when creating user
    plain_password = "test123"
    salt = generate_salt()
    hashed_password = hash_password(plain_password, salt)
    
    # Create user with hashed password
    user = Usuario(
        nombre_usuario="testuser",
        correo="test@example.com",
        contrasena_hash=hashed_password.decode('utf-8'),
        sal=salt.decode('utf-8')
    )
    
    # Verify the original password works
    assert verify_password(plain_password, hashed_password)
    assert not verify_password("wrong_password", hashed_password)

def test_hashing_performance():
    password = "test_password_for_performance"
    
    start_time = time.time()
    salt = generate_salt()
    hashed = hash_password(password, salt)
    end_time = time.time()
    
    hash_time = end_time - start_time
    
    # Hash should complete in reasonable time
    assert hash_time < 1.0  # Less than 1 second
    print(f"Password hashing took: {hash_time:.4f} seconds")
    
    # Verify the hash works
    assert verify_password(password, hashed)