import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.app import create_app
from app.core.models.base import Base
from app.core.database.connection import get_db

# Simple test database (SQLite in memory)
test_engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)

@pytest.fixture
def client():
    """Simple test client - this is what you'll use in your tests"""
    
    # Create test database tables
    Base.metadata.create_all(bind=test_engine)
    
    # Create test database session
    def get_test_db():
        db = TestSessionLocal()
        try:
            yield db
        finally:
            db.close()
    
    # Create the app and override the database
    app = create_app()
    app.dependency_overrides[get_db] = get_test_db
    
    # Return test client
    with TestClient(app) as test_client:
        yield test_client
    
    # Clean up
    Base.metadata.drop_all(bind=test_engine)