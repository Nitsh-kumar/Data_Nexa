# Implementation Plan

- [ ] 1. Set up database base configuration and utilities
  - Create `app/db/base.py` with SQLAlchemy Base class and TimestampMixin
  - Update `app/db/session.py` with async engine, session factory, and get_db dependency
  - Add database configuration to `app/config.py` (pool settings, echo mode)
  - _Requirements: 8.1, 8.2, 8.3, 8.4, 8.5, 10.1, 10.2, 10.3, 10.5_

- [ ] 2. Implement User model and schemas
  - [ ] 2.1 Create User SQLAlchemy model in `app/models/user.py`
    - Define User model with id, email, password_hash, full_name, is_active fields
    - Add TimestampMixin for created_at and updated_at
    - Configure unique index on email field
    - Set up relationships to workspaces and datasets
    - _Requirements: 1.1, 1.2, 1.3, 1.4, 9.2_
  
  - [ ] 2.2 Create User Pydantic schemas in `app/schemas/user.py`
    - Implement UserBase, UserCreate, UserUpdate, UserResponse schemas
    - Add email validation using EmailStr
    - Add password length validation (min 8 characters)
    - Configure from_attributes for ORM compatibility
    - _Requirements: 7.1, 7.2, 7.3, 7.4_

- [ ] 3. Implement Workspace model and schemas
  - [ ] 3.1 Create Workspace SQLAlchemy model in `app/models/workspace.py`
    - Define Workspace model with id, name, owner_id fields
    - Add TimestampMixin for timestamps
    - Configure foreign key to users table with index
    - Set up relationships to owner and datasets
    - _Requirements: 2.1, 2.2, 2.3, 2.4, 9.3_
  
  - [ ] 3.2 Create Workspace Pydantic schemas in `app/schemas/workspace.py`
    - Implement WorkspaceBase, WorkspaceCreate, WorkspaceUpdate, WorkspaceResponse schemas
    - Add name validation (non-empty string)
    - Include owner information in response schema
    - _Requirements: 2.5, 7.1, 7.2, 7.3, 7.4_

- [ ] 4. Implement Dataset model and schemas
  - [ ] 4.1 Create DatasetStatus enum and Dataset model in `app/models/dataset.py`
    - Define DatasetStatus enum (pending, processing, completed, failed)
    - Create Dataset model with all required fields
    - Add indexes on workspace_id, uploaded_by, and status
    - Set up relationships to workspace, uploader, and analyses
    - Configure cascade delete for analyses
    - _Requirements: 3.1, 3.2, 3.3, 3.4, 3.5, 9.3, 9.4_
  
  - [ ] 4.2 Create Dataset Pydantic schemas in `app/schemas/dataset.py`
    - Implement DatasetBase, DatasetCreate, DatasetUpdate, DatasetResponse schemas
    - Add file_path validation (non-null)
    - Include workspace and uploader details in response
    - _Requirements: 7.1, 7.2, 7.3, 7.4_

- [ ] 5. Implement Analysis model and schemas
  - [ ] 5.1 Create Analysis enums and model in `app/models/analysis.py`
    - Define AnalysisGoalType enum (ml_preparation, general_audit, data_quality, exploratory)
    - Define AnalysisStatus enum (pending, running, completed, failed)
    - Create Analysis model with all required fields
    - Add indexes on dataset_id and status
    - Set up relationships to dataset, column_profiles, and insights
    - Configure cascade delete for child records
    - _Requirements: 4.1, 4.2, 4.3, 4.4, 4.5, 9.4_
  
  - [ ] 5.2 Create Analysis Pydantic schemas in `app/schemas/analysis.py`
    - Implement AnalysisBase, AnalysisCreate, AnalysisUpdate, AnalysisResponse schemas
    - Add quality_score validation (0-100 range)
    - Include dataset details in response
    - _Requirements: 4.6, 7.1, 7.2, 7.3, 7.4_

- [ ] 6. Implement ColumnProfile model and schemas
  - [ ] 6.1 Create ColumnProfile model in `app/models/column_profile.py`
    - Define ColumnProfile model with all statistics fields
    - Configure JSON type for distribution_data field
    - Add composite index on (analysis_id, column_name)
    - Set up relationship to analysis
    - _Requirements: 5.1, 5.2, 5.3, 5.4, 5.5_
  
  - [ ] 6.2 Create ColumnProfile Pydantic schemas in `app/schemas/column_profile.py`
    - Implement ColumnProfileBase, ColumnProfileCreate, ColumnProfileResponse schemas
    - Add column_name validation (non-empty)
    - Handle optional numeric statistics fields
    - _Requirements: 7.1, 7.2, 7.4_

- [ ] 7. Implement Insight model and schemas
  - [ ] 7.1 Create Insight enums and model in `app/models/insight.py`
    - Define InsightSeverity enum (critical, high, medium, low, info)
    - Define InsightType enum (missing_data, outliers, duplicates, etc.)
    - Create Insight model with all required fields
    - Add indexes on analysis_id and severity
    - Set up relationship to analysis
    - _Requirements: 6.1, 6.2, 6.3, 6.4, 6.5, 9.5_
  
  - [ ] 7.2 Create Insight Pydantic schemas in `app/schemas/insight.py`
    - Implement InsightBase, InsightCreate, InsightResponse schemas
    - Handle optional code_suggestion field
    - Include severity and type enums in schema
    - _Requirements: 7.1, 7.2, 7.4_

- [ ] 8. Create common schemas and pagination
  - Create `app/schemas/common.py` with PaginatedResponse generic schema
  - Implement pagination parameters schema (page, page_size)
  - Add common response wrappers (success, error)
  - _Requirements: 7.5_

- [ ] 9. Update models __init__.py for imports
  - Import all models in `app/models/__init__.py`
  - Import Base from `app/db/base.py`
  - Ensure proper import order for relationships
  - _Requirements: 8.4_

- [ ] 10. Update schemas __init__.py for imports
  - Import all schemas in `app/schemas/__init__.py`
  - Export commonly used schemas
  - _Requirements: 7.1_

- [ ] 11. Create Alembic migration configuration
  - Initialize Alembic in backend directory
  - Configure `alembic.ini` with database URL from settings
  - Update `env.py` to import all models
  - Configure async migration support
  - _Requirements: 8.1, 8.5_

- [ ] 12. Generate initial database migration
  - Create initial migration with all tables
  - Review auto-generated migration for correctness
  - Verify indexes and constraints are included
  - Test migration up and down
  - _Requirements: 9.1, 9.2, 9.3, 9.4, 9.5_

- [ ]* 13. Create database utility functions
  - Create `app/db/utils.py` with helper functions
  - Implement `init_db()` function for database initialization
  - Add `check_db_connection()` health check function
  - Create `reset_db()` function for testing
  - _Requirements: 8.2, 8.3_

- [ ]* 14. Write unit tests for models
  - Create `tests/test_models/` directory
  - Write tests for User model (creation, relationships, constraints)
  - Write tests for Workspace model (relationships, cascade)
  - Write tests for Dataset model (status enum, relationships)
  - Write tests for Analysis model (enums, quality score validation)
  - Write tests for ColumnProfile model (JSON field, statistics)
  - Write tests for Insight model (enums, relationships)
  - _Requirements: 1.1, 1.2, 1.3, 2.1, 3.1, 4.1, 5.1, 6.1_

- [ ]* 15. Write unit tests for schemas
  - Create `tests/test_schemas/` directory
  - Write tests for User schemas (validation, email format)
  - Write tests for Workspace schemas (name validation)
  - Write tests for Dataset schemas (status enum)
  - Write tests for Analysis schemas (quality score range)
  - Write tests for ColumnProfile schemas (optional fields)
  - Write tests for Insight schemas (enums)
  - Test pagination schema
  - _Requirements: 7.1, 7.2, 7.3, 7.4, 7.5_

- [ ]* 16. Write integration tests for database operations
  - Create `tests/test_db/` directory
  - Test database session lifecycle (commit, rollback)
  - Test cascade deletes (workspace -> datasets -> analyses)
  - Test unique constraints (duplicate email)
  - Test foreign key constraints
  - Test transaction isolation
  - _Requirements: 1.5, 2.3, 3.5, 8.2_

- [ ]* 17. Create database seeding script
  - Create `scripts/seed_db.py` for development data
  - Add sample users, workspaces, and datasets
  - Include various analysis states for testing
  - Add command-line arguments for customization
  - _Requirements: 8.1_

- [ ] 18. Update main.py with database initialization
  - Add startup event to check database connection
  - Add shutdown event to close database connections
  - Include database health check in /health endpoint
  - _Requirements: 8.2, 8.3_

- [ ] 19. Update requirements.txt with database dependencies
  - Verify sqlalchemy[asyncio]==2.0.25 is included
  - Verify asyncpg==0.29.0 is included
  - Verify alembic==1.13.1 is included
  - Add pydantic[email] for email validation
  - _Requirements: 8.5_

- [ ] 20. Create database documentation
  - Document database schema in `docs/DATABASE.md`
  - Include ER diagram (can use Mermaid)
  - Document all enums and their values
  - Add migration workflow instructions
  - Document common query patterns
  - _Requirements: 8.1, 8.2_
