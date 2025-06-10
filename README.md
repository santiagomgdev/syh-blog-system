# Blog System API

A modern blog platform built with FastAPI, SQLAlchemy, and MySQL.

## Features

- User authentication with JWT tokens
- Blog post management
- Comments system with threading
- Role-based access control
- Soft delete functionality

## Project Structure

```
app/
├── core/           # Core application components
│   ├── config/     # Configuration files
│   ├── database/   # Database connection and setup
│   └── models/     # SQLAlchemy models
├── modules/        # Feature modules
│   ├── apis/       # API endpoints
│   ├── schemas/    # Pydantic schemas
│   └── services/   # Business logic
├── test/          # Test files
└── utils/         # Utility functions
```

## Setup

1. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure environment variables:
```bash
cp .env.example .env
# Edit .env with your settings
```

4. Run the application:
```bash
uvicorn app.main:app --reload
```

The API will be available at http://localhost:8000

## Testing

This project includes a comprehensive testing setup using pytest.

### Running Tests

```bash
# Run all tests
python -m pytest

# Run tests with verbose output
python -m pytest -v

# Run tests with coverage report
python -m pytest --cov=app --cov-report=term-missing

# Run tests with HTML coverage report
python -m pytest --cov=app --cov-report=html

# Run specific test file
python -m pytest app/test/test_simple.py

# Run tests and stop on first failure
python -m pytest -x
```

### Test Structure

```txt
app/test/
├── conftest.py           # Test configuration and fixtures
└── test_simple.py        # Basic health check tests
```

### Coverage Reports

After running tests with coverage, you can:
- View terminal coverage summary
- Open `htmlcov/index.html` in your browser for detailed coverage report

### Adding New Tests

1. Create test files following the pattern `test_*.py` in `app/test/`
2. Use the `client` fixture from `conftest.py` for API testing
3. Follow the naming convention `test_*` for test functions

Example:
```python
def test_my_new_feature(client):
    response = client.get("/my-endpoint")
    assert response.status_code == 200
```

## API Documentation

Visit http://localhost:8000/docs for interactive API documentation.