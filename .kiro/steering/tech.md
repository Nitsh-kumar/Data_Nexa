# Technology Stack

## Backend Framework
- **FastAPI**: Modern async web framework for building APIs
- **Python 3.11+**: Required for latest type hints and performance

## Database
- **PostgreSQL**: Primary database
- **SQLAlchemy 2.0+**: ORM with async support
- **Alembic**: Database migrations

## Data Processing
- **Pandas**: CSV/Excel file processing
- **OpenPyXL**: Excel file handling

## Authentication & Security
- **JWT tokens**: Authentication
- **bcrypt**: Password hashing
- **python-jose**: JWT implementation

## Code Quality
- **Black**: Code formatter (max line length: 100)
- **isort**: Import sorting
- **mypy**: Static type checking
- **pytest**: Testing framework

## Common Commands

### Development
```bash
# Install dependencies
pip install -r requirements.txt

# Run development server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Format code
black app/ tests/
isort app/ tests/

# Type checking
mypy app/

# Run tests
pytest tests/ -v
```

### Database
```bash
# Create migration
alembic revision --autogenerate -m "description"

# Apply migrations
alembic upgrade head

# Rollback migration
alembic downgrade -1
```

### Docker
```bash
# Build image
docker build -t datainsight-backend .

# Run container
docker-compose up -d
```
