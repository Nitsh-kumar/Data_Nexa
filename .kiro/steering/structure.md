# Project Structure

## Directory Organization

```
backend/
├── app/                    # Main application package
│   ├── api/v1/            # API version 1 endpoints
│   ├── core/              # Core functionality (security, config)
│   ├── models/            # SQLAlchemy models
│   ├── schemas/           # Pydantic schemas
│   ├── services/          # Business logic layer
│   ├── utils/             # Utility functions
│   └── db/                # Database configuration and session
├── tests/                 # Test suite
└── alembic/              # Database migrations
```

## Module Responsibilities

### app/api/v1/
API route handlers organized by resource (users, files, insights, etc.)
- Each resource gets its own file (e.g., `users.py`, `files.py`)
- Use APIRouter for route organization
- Keep handlers thin - delegate to services

### app/core/
Core application components
- `security.py`: Authentication, authorization, password hashing
- `config.py`: Application settings
- `exceptions.py`: Custom exception classes

### app/models/
SQLAlchemy ORM models
- One file per model or group related models
- Use async-compatible base class
- Include relationships and indexes

### app/schemas/
Pydantic schemas for request/response validation
- Separate schemas for create, update, and response
- Use Pydantic v2 syntax
- Include examples for documentation

### app/services/
Business logic and repository pattern
- Service classes handle business logic
- Repository classes handle data access
- Use dependency injection

### app/db/
Database configuration
- `session.py`: Database session management
- `base.py`: Base model class

## Naming Conventions
- Files: lowercase with underscores (`user_service.py`)
- Classes: PascalCase (`UserService`)
- Functions: lowercase with underscores (`get_current_user`)
- Constants: UPPERCASE (`MAX_FILE_SIZE`)
