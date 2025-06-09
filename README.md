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

## API Documentation

Visit http://localhost:8000/docs for interactive API documentation.