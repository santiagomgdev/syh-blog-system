import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.app import create_app
from app.core.models.base import Base
from app.core.database.connection import get_db

# Test database configuration
TEST_DATABASE_URL = "postgresql://postgres:root@localhost:5432/test_myapp"


@pytest.fixture(scope="session")
def test_engine():
    """Create test database engine"""
    engine = create_engine(TEST_DATABASE_URL)
    return engine

@pytest.fixture(scope="session")
def setup_test_db(test_engine):
    """Set up test database schema once per session"""
    # Create all tables
    Base.metadata.create_all(bind=test_engine)
    yield
    # Drop all tables after all tests
    Base.metadata.drop_all(bind=test_engine)

@pytest.fixture
def db_session(test_engine, setup_test_db):
    """Create a clean database session for each test"""

    # Start a transaction
    connection = test_engine.connect()
    transaction = connection.begin()

    TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=connection)
    session = TestSessionLocal()
    
    try:
        yield session
    finally:
        # Rollback transaction to clean up data
        session.close()
        transaction.rollback()
        connection.close()

@pytest.fixture
def client(db_session):
    """FastAPI test client with PostgreSQL database"""
    
    def get_test_db():
        try:
            yield db_session
        finally:
            pass
    
    app = create_app()
    app.dependency_overrides[get_db] = get_test_db
    
    with TestClient(app) as test_client:
        yield test_client

@pytest.fixture
def test_user():
    """Test user data fixture"""
    return {
        "nombre_usuario": "Test User",
        "correo": "test@example.com",
        "contrasena": "testpassword123"
    }

# Integration Tests - Endpoint
def test_user_registration_success(client, test_user):
    """Test successful user registration endpoint"""
    response = client.post("/api/v1/auth/register", json=test_user)

    print(test_user)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")
    
    assert response.status_code == 201
    data = response.json()
    assert data["correo"] == test_user["correo"]
    assert data["nombre_usuario"] == test_user["nombre_usuario"]
    assert "contrasena_hash" not in data
    assert "contrasena" not in data
    assert "id" in data

def test_duplicate_email_registration(client, test_user):
    """Test duplicate email registration fails"""
    # Register user first
    client.post("/api/v1/auth/register", json=test_user)
    
    # Try to register again with same email
    response = client.post("/api/v1/auth/register", json=test_user)
    assert response.status_code == 409

# Input Validation Tests
def test_invalid_email_format(client):
    """Test registration with invalid email format"""
    invalid_user = {
        "nombre_usuario": "Test User",
        "correo": "invalid-email",
        "contrasena": "testpassword123"
    }
    
    response = client.post("/api/v1/auth/register", json=invalid_user)
    assert response.status_code == 422

def test_missing_required_fields(client):
    """Test registration with missing required fields"""
    incomplete_user = {
        "correo": "test@example.com"
        # Missing name and password
    }
    
    response = client.post("/api/v1/auth/register", json=incomplete_user)
    assert response.status_code == 422

def test_empty_password(client):
    """Test registration with empty password"""
    user_empty_password = {
        "nombre_usuario": "Test User",
        "correo": "test@example.com",
        "contrasena": ""
    }
    
    response = client.post("/api/v1/auth/register", json=user_empty_password)
    assert response.status_code == 422

def test_short_password(client):
    """Test registration with password too short"""
    user_short_password = {
        "nombre_usuario": "Test User",
        "correo": "test@example.com",
        "contrasena": "123"
    }
    
    response = client.post("/api/v1/auth/register", json=user_short_password)
    assert response.status_code == 422

# Edge Cases
def test_registration_with_whitespace_email(client):
    """Test registration trims whitespace from email"""
    user_with_spaces = {
        "nombre_usuario": "Test User",
        "correo": "  test@example.com  ",
        "contrasena": "testpassword123"
    }
    
    response = client.post("/api/v1/auth/register", json=user_with_spaces)
    
    if response.status_code == 201:
        data = response.json()
        assert data["correo"] == "test@example.com"

def test_registration_case_insensitive_email(client):
    """Test email case sensitivity handling"""
    user1 = {
        "nombre_usuario": "Test User 1",
        "correo": "Test@Example.com",
        "contrasena": "testpassword123"
    }
    
    user2 = {
        "nombre_usuario": "Test User 2",
        "correo": "test@example.com",
        "contrasena": "testpassword456"
    }
    
    # Register first user
    response1 = client.post("/api/v1/auth/register", json=user1)
    assert response1.status_code == 201
    
    # Try to register second user with same email (different case)
    response2 = client.post("/api/v1/auth/register", json=user2)
    assert response2.status_code == 409

def test_registration_long_name(client):
    """Test registration with very long name"""
    long_name_user = {
        "nombre_usuario": "A" * 200,  # Very long name
        "correo": "longname@example.com",
        "contrasena": "testpassword123"
    }
    
    response = client.post("/api/v1/auth/register", json=long_name_user)
    # Should either succeed or fail with validation error
    assert response.status_code in [201, 422]

def test_special_characters_in_name(client):
    """Test registration with special characters in name"""
    special_name_user = {
        "nombre_usuario": "José María O'Connor-Smith",
        "correo": "special@example.com",
        "contrasena": "testpassword123"
    }
    
    response = client.post("/api/v1/auth/register", json=special_name_user)
    assert response.status_code == 201
    data = response.json()
    assert data["nombre_usuario"] == special_name_user["nombre_usuario"]