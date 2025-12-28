# DataInsight Pro Backend

A SaaS data profiling tool backend that analyzes CSV/Excel files and provides AI-powered insights.

## Features

- 📊 CSV/Excel file upload and parsing
- 🔍 Automated data profiling and analysis
- 🤖 AI-powered insights generation
- 🔐 JWT-based authentication
- 🏢 Multi-tenant architecture
- ⚡ Async FastAPI for high performance

## Tech Stack

- **Framework**: FastAPI
- **Database**: PostgreSQL with SQLAlchemy 2.0 (async)
- **Authentication**: JWT tokens with bcrypt
- **Data Processing**: Pandas, OpenPyXL
- **Code Quality**: Black, isort, mypy, pytest

## Prerequisites

- Python 3.11+
- PostgreSQL 14+
- pip or poetry

## Setup

### 1. Clone and Install

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure Environment

```bash
cp .env.example .env
# Edit .env with your configuration
```

Generate a secure secret key:
```bash
openssl rand -hex 32
```

### 3. Database Setup

```bash
# Create database
createdb datainsight

# Run migrations (when available)
alembic upgrade head
```

### 4. Run Development Server

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

API will be available at: http://localhost:8000
API docs: http://localhost:8000/docs

## Development

### Code Formatting

```bash
black app/ tests/
isort app/ tests/
```

### Type Checking

```bash
mypy app/
```

### Running Tests

```bash
pytest tests/ -v
```

## Project Structure

```
backend/
├── app/
│   ├── api/v1/         # API endpoints
│   ├── core/           # Security, config, exceptions
│   ├── models/         # SQLAlchemy models
│   ├── schemas/        # Pydantic schemas
│   ├── services/       # Business logic
│   ├── utils/          # Utilities
│   └── db/             # Database config
├── tests/              # Test suite
└── alembic/           # Database migrations
```

## API Documentation

Once running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### Available Endpoints

**AI Insights:**
- `GET /api/v1/insights/{analysis_id}` - Get insights for an analysis
- `GET /api/v1/insights/{analysis_id}/summary` - Get insights summary
- `POST /api/v1/insights/{analysis_id}/generate` - Generate new insights
- `GET /api/v1/insights/stats/tokens` - Get Claude API token usage
- `GET /api/v1/insights/stats/cache` - Get Redis cache statistics

**Health:**
- `GET /health` - Health check endpoint

## Architecture Documentation

For detailed architecture and flow documentation, see:
- **Architecture Flow:** `docs/ARCHITECTURE_FLOW.md` - Complete request flow
- **AI Insights Guide:** `docs/AI_INSIGHTS.md` - AI engine documentation
- **Code Review Guide:** `docs/CODE_REVIEW_GUIDE.md` - For code reviewers

## Docker

```bash
docker build -t datainsight-backend .
docker run -p 8000:8000 --env-file .env datainsight-backend
```

## Contributing

1. Follow Black formatting (max line length: 100)
2. Add type hints to all functions
3. Write docstrings in Google format
4. Write tests for new features
5. Use the repository pattern for data access

## License

Proprietary
