# Design Document

## Overview

This design document outlines the implementation of the database layer for DataInsight Pro Backend. The database layer consists of SQLAlchemy ORM models, Pydantic validation schemas, and async database session management. The design follows a multi-tenant architecture with proper relationships, indexes, and type safety.

## Architecture

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     FastAPI Application                      │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌──────────────┐      ┌──────────────┐                     │
│  │   API Layer  │─────▶│   Schemas    │ (Pydantic)          │
│  │  (Routes)    │      │  (Validation)│                     │
│  └──────────────┘      └──────────────┘                     │
│         │                      │                             │
│         ▼                      ▼                             │
│  ┌──────────────┐      ┌──────────────┐                     │
│  │   Services   │─────▶│    Models    │ (SQLAlchemy)        │
│  │   (Logic)    │      │  (Database)  │                     │
│  └──────────────┘      └──────────────┘                     │
│         │                      │                             │
│         └──────────┬───────────┘                             │
│                    ▼                                         │
│            ┌──────────────┐                                  │
│            │   Session    │ (Async)                          │
│            │  Management  │                                  │
│            └──────────────┘                                  │
│                    │                                         │
└────────────────────┼─────────────────────────────────────────┘
                     ▼
            ┌──────────────┐
            │  PostgreSQL  │
            │   Database   │
            └──────────────┘
```

### Database Schema Relationships

```
┌──────────────┐
│    User      │
│──────────────│
│ id (PK)      │◀─────────┐
│ email        │          │
│ password_hash│          │
│ full_name    │          │
└──────────────┘          │
       │                  │
       │ owns             │ uploaded_by
       ▼                  │
┌──────────────┐          │
│  Workspace   │          │
│──────────────│          │
│ id (PK)      │          │
│ name         │          │
│ owner_id (FK)│          │
└──────────────┘          │
       │                  │
       │ contains         │
       ▼                  │
┌──────────────┐          │
│   Dataset    │          │
│──────────────│          │
│ id (PK)      │◀─────────┘
│ name         │
│ file_path    │
│ workspace_id │
│ uploaded_by  │
└──────────────┘
       │
       │ has
       ▼
┌──────────────┐
│   Analysis   │
│──────────────│
│ id (PK)      │
│ dataset_id   │
│ goal_type    │
│ status       │
│ quality_score│
└──────────────┘
       │
       ├─────────────┬──────────────┐
       │             │              │
       ▼             ▼              ▼
┌──────────────┐ ┌──────────────┐ ┌──────────────┐
│ColumnProfile│ │   Insight    │ │  (Future)    │
│──────────────│ │──────────────│ │              │
│ id (PK)      │ │ id (PK)      │ │              │
│ analysis_id  │ │ analysis_id  │ │              │
│ column_name  │ │ severity     │ │              │
│ data_type    │ │ type         │ │              │
│ statistics   │ │ description  │ │              │
└──────────────┘ └──────────────┘ └──────────────┘
```

## Components and Interfaces

### 1. Base Model Configuration

**File:** `app/db/base.py`

**Purpose:** Provide base class for all SQLAlchemy models with common functionality.

**Design:**
```python
class Base(DeclarativeBase):
    """Base class for all database models."""
    pass

class TimestampMixin:
    """Mixin for automatic timestamp management."""
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), 
        server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )
```

**Key Features:**
- Declarative base for all models
- Timestamp mixin for automatic created_at/updated_at
- Type hints using SQLAlchemy 2.0 Mapped syntax

### 2. Database Session Management

**File:** `app/db/session.py`

**Purpose:** Manage async database connections and sessions.

**Design:**
```python
# Async engine with connection pooling
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,
    pool_pre_ping=True,
    pool_size=10,
    max_overflow=20
)

# Async session factory
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# Dependency for FastAPI
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
```

**Key Features:**
- Connection pooling for performance
- Automatic commit/rollback
- Context manager for safe session handling

### 3. User Model

**File:** `app/models/user.py`

**Purpose:** Store user authentication and profile data.

**Design:**
```python
class User(Base, TimestampMixin):
    __tablename__ = "users"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    password_hash: Mapped[str] = mapped_column(String(255))
    full_name: Mapped[str] = mapped_column(String(255))
    is_active: Mapped[bool] = mapped_column(default=True)
    
    # Relationships
    workspaces: Mapped[list["Workspace"]] = relationship(
        back_populates="owner",
        cascade="all, delete-orphan"
    )
    datasets: Mapped[list["Dataset"]] = relationship(
        back_populates="uploader"
    )
```

**Indexes:**
- Primary key on `id`
- Unique index on `email`

**Constraints:**
- Email must be unique
- Password hash required

### 4. Workspace Model

**File:** `app/models/workspace.py`

**Purpose:** Multi-tenant workspace organization.

**Design:**
```python
class Workspace(Base, TimestampMixin):
    __tablename__ = "workspaces"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255))
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    
    # Relationships
    owner: Mapped["User"] = relationship(back_populates="workspaces")
    datasets: Mapped[list["Dataset"]] = relationship(
        back_populates="workspace",
        cascade="all, delete-orphan"
    )
```

**Indexes:**
- Primary key on `id`
- Foreign key index on `owner_id`

**Business Rules:**
- Each workspace must have an owner
- Workspace name required

### 5. Dataset Model

**File:** `app/models/dataset.py`

**Purpose:** Store uploaded file metadata.

**Design:**
```python
class DatasetStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"

class Dataset(Base, TimestampMixin):
    __tablename__ = "datasets"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255))
    file_path: Mapped[str] = mapped_column(String(500))
    file_size: Mapped[int] = mapped_column()  # bytes
    row_count: Mapped[int | None] = mapped_column()
    column_count: Mapped[int | None] = mapped_column()
    status: Mapped[DatasetStatus] = mapped_column(
        Enum(DatasetStatus),
        default=DatasetStatus.PENDING,
        index=True
    )
    
    workspace_id: Mapped[int] = mapped_column(
        ForeignKey("workspaces.id"),
        index=True
    )
    uploaded_by: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        index=True
    )
    uploaded_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )
    
    # Relationships
    workspace: Mapped["Workspace"] = relationship(back_populates="datasets")
    uploader: Mapped["User"] = relationship(back_populates="datasets")
    analyses: Mapped[list["Analysis"]] = relationship(
        back_populates="dataset",
        cascade="all, delete-orphan"
    )
```

**Indexes:**
- Primary key on `id`
- Foreign key indexes on `workspace_id`, `uploaded_by`
- Index on `status` for filtering

### 6. Analysis Model

**File:** `app/models/analysis.py`

**Purpose:** Store analysis execution metadata and results.

**Design:**
```python
class AnalysisGoalType(str, Enum):
    ML_PREPARATION = "ml_preparation"
    GENERAL_AUDIT = "general_audit"
    DATA_QUALITY = "data_quality"
    EXPLORATORY = "exploratory"

class AnalysisStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"

class Analysis(Base, TimestampMixin):
    __tablename__ = "analyses"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    dataset_id: Mapped[int] = mapped_column(
        ForeignKey("datasets.id"),
        index=True
    )
    goal_type: Mapped[AnalysisGoalType] = mapped_column(Enum(AnalysisGoalType))
    status: Mapped[AnalysisStatus] = mapped_column(
        Enum(AnalysisStatus),
        default=AnalysisStatus.PENDING,
        index=True
    )
    quality_score: Mapped[float | None] = mapped_column()
    started_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    error_message: Mapped[str | None] = mapped_column(Text)
    
    # Relationships
    dataset: Mapped["Dataset"] = relationship(back_populates="analyses")
    column_profiles: Mapped[list["ColumnProfile"]] = relationship(
        back_populates="analysis",
        cascade="all, delete-orphan"
    )
    insights: Mapped[list["Insight"]] = relationship(
        back_populates="analysis",
        cascade="all, delete-orphan"
    )
```

**Indexes:**
- Primary key on `id`
- Foreign key index on `dataset_id`
- Index on `status` for filtering

**Constraints:**
- Quality score between 0 and 100 (enforced at application level)

### 7. Column Profile Model

**File:** `app/models/column_profile.py`

**Purpose:** Store detailed column-level statistics.

**Design:**
```python
class ColumnProfile(Base):
    __tablename__ = "column_profiles"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    analysis_id: Mapped[int] = mapped_column(
        ForeignKey("analyses.id"),
        index=True
    )
    column_name: Mapped[str] = mapped_column(String(255))
    data_type: Mapped[str] = mapped_column(String(50))
    null_count: Mapped[int] = mapped_column()
    unique_count: Mapped[int] = mapped_column()
    min_value: Mapped[str | None] = mapped_column(String(255))
    max_value: Mapped[str | None] = mapped_column(String(255))
    mean: Mapped[float | None] = mapped_column()
    median: Mapped[float | None] = mapped_column()
    distribution_data: Mapped[dict | None] = mapped_column(JSON)
    
    # Relationships
    analysis: Mapped["Analysis"] = relationship(back_populates="column_profiles")
```

**Indexes:**
- Primary key on `id`
- Foreign key index on `analysis_id`
- Composite index on `(analysis_id, column_name)` for lookups

### 8. Insight Model

**File:** `app/models/insight.py`

**Purpose:** Store AI-generated insights and recommendations.

**Design:**
```python
class InsightSeverity(str, Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"

class InsightType(str, Enum):
    MISSING_DATA = "missing_data"
    OUTLIERS = "outliers"
    DUPLICATES = "duplicates"
    DATA_TYPE_MISMATCH = "data_type_mismatch"
    PATTERN_VIOLATION = "pattern_violation"
    QUALITY_ISSUE = "quality_issue"

class Insight(Base):
    __tablename__ = "insights"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    analysis_id: Mapped[int] = mapped_column(
        ForeignKey("analyses.id"),
        index=True
    )
    severity: Mapped[InsightSeverity] = mapped_column(
        Enum(InsightSeverity),
        index=True
    )
    type: Mapped[InsightType] = mapped_column(Enum(InsightType))
    description: Mapped[str] = mapped_column(Text)
    recommendation: Mapped[str] = mapped_column(Text)
    code_suggestion: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )
    
    # Relationships
    analysis: Mapped["Analysis"] = relationship(back_populates="insights")
```

**Indexes:**
- Primary key on `id`
- Foreign key index on `analysis_id`
- Index on `severity` for filtering

## Data Models

### Pydantic Schema Structure

Each model will have four schema variants:

1. **Base Schema**: Common fields shared across variants
2. **Create Schema**: For POST requests (excludes auto-generated fields)
3. **Update Schema**: For PATCH requests (all fields optional)
4. **Response Schema**: For API responses (includes all fields)

**Example Structure:**
```python
# Base schema with common fields
class UserBase(BaseModel):
    email: EmailStr
    full_name: str

# Create schema for registration
class UserCreate(UserBase):
    password: str = Field(min_length=8)

# Update schema for profile updates
class UserUpdate(BaseModel):
    email: EmailStr | None = None
    full_name: str | None = None
    password: str | None = Field(None, min_length=8)

# Response schema
class UserResponse(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

# Paginated list response
class UserListResponse(BaseModel):
    items: list[UserResponse]
    total: int
    page: int
    page_size: int
```

### Schema Files Organization

```
app/schemas/
├── __init__.py
├── user.py          # User schemas
├── workspace.py     # Workspace schemas
├── dataset.py       # Dataset schemas
├── analysis.py      # Analysis schemas
├── column_profile.py # Column profile schemas
├── insight.py       # Insight schemas
└── common.py        # Shared schemas (pagination, etc.)
```

## Error Handling

### Database Error Handling Strategy

1. **Integrity Errors**: Catch unique constraint violations
   ```python
   try:
       await session.commit()
   except IntegrityError as e:
       if "unique constraint" in str(e):
           raise ValidationException("Email already exists")
   ```

2. **Foreign Key Violations**: Validate relationships exist
   ```python
   workspace = await session.get(Workspace, workspace_id)
   if not workspace:
       raise NotFoundException("Workspace not found")
   ```

3. **Connection Errors**: Retry logic with exponential backoff
   ```python
   @retry(stop=stop_after_attempt(3), wait=wait_exponential())
   async def execute_query():
       ...
   ```

## Testing Strategy

### Unit Tests

**Test Coverage:**
- Model creation and validation
- Relationship loading
- Enum constraints
- Timestamp automation
- Schema validation

**Example Test:**
```python
async def test_create_user():
    user = User(
        email="test@example.com",
        password_hash="hashed",
        full_name="Test User"
    )
    session.add(user)
    await session.commit()
    
    assert user.id is not None
    assert user.created_at is not None
    assert user.is_active is True
```

### Integration Tests

**Test Coverage:**
- Database session lifecycle
- Transaction rollback
- Cascade deletes
- Query performance

**Example Test:**
```python
async def test_cascade_delete_workspace():
    # Create workspace with datasets
    workspace = Workspace(name="Test", owner_id=1)
    dataset = Dataset(name="Test", workspace=workspace)
    
    # Delete workspace
    await session.delete(workspace)
    await session.commit()
    
    # Verify dataset is also deleted
    result = await session.get(Dataset, dataset.id)
    assert result is None
```

## Performance Considerations

### Indexing Strategy

1. **Primary Keys**: Automatic B-tree indexes
2. **Foreign Keys**: Explicit indexes for join performance
3. **Status Fields**: Indexes for filtering queries
4. **Composite Indexes**: For common query patterns

### Query Optimization

1. **Eager Loading**: Use `selectinload()` for relationships
   ```python
   stmt = select(User).options(selectinload(User.workspaces))
   ```

2. **Pagination**: Always use LIMIT/OFFSET
   ```python
   stmt = select(Dataset).limit(page_size).offset(page * page_size)
   ```

3. **Projection**: Select only needed columns
   ```python
   stmt = select(User.id, User.email)
   ```

### Connection Pooling

- Pool size: 10 connections
- Max overflow: 20 connections
- Pool pre-ping: Enabled for stale connection detection
- Pool recycle: 3600 seconds

## Security Considerations

### Data Protection

1. **Password Storage**: Never store plain text passwords
2. **Sensitive Data**: Consider encryption for PII
3. **SQL Injection**: Use parameterized queries (SQLAlchemy handles this)
4. **Access Control**: Validate workspace ownership before operations

### Audit Trail

- All models include `created_at` timestamp
- Models with updates include `updated_at` timestamp
- Consider adding `deleted_at` for soft deletes (future enhancement)

## Migration Strategy

### Alembic Configuration

1. **Initial Migration**: Create all tables
2. **Version Control**: Track schema changes in git
3. **Rollback Support**: Test downgrade migrations
4. **Data Migrations**: Separate from schema migrations

**Migration Workflow:**
```bash
# Create migration
alembic revision --autogenerate -m "create initial tables"

# Review generated migration
# Edit if needed

# Apply migration
alembic upgrade head

# Rollback if needed
alembic downgrade -1
```

## Dependencies

### Required Packages

```
sqlalchemy[asyncio]==2.0.25
asyncpg==0.29.0
alembic==1.13.1
pydantic==2.5.3
pydantic[email]==2.5.3
```

### Configuration Requirements

**Environment Variables:**
```
DATABASE_URL=postgresql+asyncpg://user:pass@localhost/dbname
DATABASE_POOL_SIZE=10
DATABASE_MAX_OVERFLOW=20
DATABASE_ECHO=false
```

## Future Enhancements

1. **Soft Deletes**: Add `deleted_at` field for recovery
2. **Audit Logging**: Track all changes with user attribution
3. **Read Replicas**: Support read-only database connections
4. **Sharding**: Partition data by workspace for scale
5. **Full-Text Search**: Add PostgreSQL full-text search indexes
6. **Materialized Views**: For complex analytics queries
