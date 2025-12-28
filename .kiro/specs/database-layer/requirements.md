# Requirements Document

## Introduction

This spec defines the database layer implementation for DataInsight Pro Backend, including SQLAlchemy models, Pydantic schemas, and database configuration. The database layer provides the foundation for storing users, workspaces, datasets, analysis results, column profiles, and AI-generated insights with proper relationships and multi-tenancy support.

## Requirements

### Requirement 1: User Management

**User Story:** As a system, I need to store user authentication data and profile information, so that users can register, login, and manage their account.

#### Acceptance Criteria

1. WHEN a user model is created THEN the system SHALL include fields for id, email, password_hash, full_name, created_at, and updated_at
2. WHEN a user is created THEN the system SHALL automatically set created_at and updated_at timestamps
3. WHEN a user email is stored THEN the system SHALL enforce uniqueness constraint
4. WHEN querying users THEN the system SHALL support relationships to workspaces and datasets
5. IF a user is deleted THEN the system SHALL handle cascade behavior for related records

### Requirement 2: Workspace Multi-Tenancy

**User Story:** As a user, I want to organize my datasets into workspaces, so that I can separate different projects and collaborate with team members.

#### Acceptance Criteria

1. WHEN a workspace is created THEN the system SHALL include fields for id, name, owner_id, and created_at
2. WHEN a workspace is created THEN the system SHALL establish a foreign key relationship to the user model
3. WHEN querying a workspace THEN the system SHALL support relationships to members and datasets
4. WHEN a workspace owner is queried THEN the system SHALL return the associated user object
5. IF a workspace name is provided THEN the system SHALL validate it is not empty

### Requirement 3: Dataset Metadata Storage

**User Story:** As a user, I want the system to store metadata about my uploaded files, so that I can track file information and analysis history.

#### Acceptance Criteria

1. WHEN a dataset is uploaded THEN the system SHALL store id, name, file_path, file_size, row_count, column_count, workspace_id, uploaded_by, uploaded_at, and status
2. WHEN a dataset is created THEN the system SHALL use an enum for status field with values: pending, processing, completed, failed
3. WHEN querying a dataset THEN the system SHALL support relationships to workspace, uploader user, and analyses
4. WHEN a dataset file_path is stored THEN the system SHALL validate it is not null
5. IF a dataset belongs to a workspace THEN the system SHALL enforce foreign key constraint

### Requirement 4: Analysis Results Storage

**User Story:** As a system, I need to store analysis execution metadata and results, so that users can track analysis progress and retrieve completed results.

#### Acceptance Criteria

1. WHEN an analysis is created THEN the system SHALL include fields for id, dataset_id, goal_type, status, quality_score, started_at, completed_at, and error_message
2. WHEN an analysis goal_type is set THEN the system SHALL use an enum with values: ml_preparation, general_audit, data_quality, exploratory
3. WHEN an analysis status is set THEN the system SHALL use an enum with values: pending, running, completed, failed
4. WHEN querying an analysis THEN the system SHALL support relationships to dataset, column_profiles, and insights
5. IF an analysis fails THEN the system SHALL store the error_message
6. WHEN an analysis quality_score is stored THEN the system SHALL validate it is between 0 and 100

### Requirement 5: Column Profile Statistics

**User Story:** As a system, I need to store detailed column-level statistics from data profiling, so that users can view granular analysis results for each column.

#### Acceptance Criteria

1. WHEN a column profile is created THEN the system SHALL include fields for id, analysis_id, column_name, data_type, null_count, unique_count, min_value, max_value, mean, median, and distribution_data
2. WHEN distribution_data is stored THEN the system SHALL use JSON type for flexible storage
3. WHEN querying a column profile THEN the system SHALL support relationship to parent analysis
4. WHEN a column_name is stored THEN the system SHALL validate it is not empty
5. IF numeric statistics are stored THEN the system SHALL allow null values for non-numeric columns

### Requirement 6: AI-Generated Insights Storage

**User Story:** As a user, I want the system to store AI-generated insights and recommendations, so that I can review actionable suggestions for data quality improvements.

#### Acceptance Criteria

1. WHEN an insight is created THEN the system SHALL include fields for id, analysis_id, severity, type, description, recommendation, code_suggestion, and created_at
2. WHEN an insight severity is set THEN the system SHALL use an enum with values: critical, high, medium, low, info
3. WHEN an insight type is set THEN the system SHALL use an enum with values: missing_data, outliers, duplicates, data_type_mismatch, pattern_violation, quality_issue
4. WHEN querying an insight THEN the system SHALL support relationship to parent analysis
5. IF a code_suggestion is provided THEN the system SHALL store it as text

### Requirement 7: Pydantic Schema Validation

**User Story:** As an API developer, I need Pydantic schemas for request/response validation, so that API contracts are enforced and documented.

#### Acceptance Criteria

1. WHEN a schema is created for each model THEN the system SHALL provide Base, Create, Update, and Response schema variants
2. WHEN a Create schema is used THEN the system SHALL exclude auto-generated fields like id and timestamps
3. WHEN an Update schema is used THEN the system SHALL make all fields optional
4. WHEN a Response schema is used THEN the system SHALL include all fields with proper types
5. WHEN a list response is needed THEN the system SHALL provide pagination schema with items, total, page, and page_size

### Requirement 8: Database Configuration

**User Story:** As a developer, I need proper database configuration and session management, so that the application can connect to PostgreSQL with async support.

#### Acceptance Criteria

1. WHEN the database is initialized THEN the system SHALL use SQLAlchemy 2.0+ async syntax
2. WHEN a database session is needed THEN the system SHALL provide an async context manager
3. WHEN FastAPI endpoints need database access THEN the system SHALL provide a get_db dependency function
4. WHEN models are defined THEN the system SHALL use a common Base class
5. IF the database URL is configured THEN the system SHALL support PostgreSQL with asyncpg driver

### Requirement 9: Database Indexes and Performance

**User Story:** As a system administrator, I need proper database indexes, so that queries perform efficiently at scale.

#### Acceptance Criteria

1. WHEN a foreign key is defined THEN the system SHALL create an index on that column
2. WHEN a user email is stored THEN the system SHALL create a unique index
3. WHEN datasets are queried by workspace THEN the system SHALL have an index on workspace_id
4. WHEN analyses are queried by status THEN the system SHALL have an index on status field
5. WHEN insights are queried by severity THEN the system SHALL have an index on severity field

### Requirement 10: Timestamp Automation

**User Story:** As a developer, I want automatic timestamp management, so that created_at and updated_at fields are maintained without manual intervention.

#### Acceptance Criteria

1. WHEN a record is created THEN the system SHALL automatically set created_at to current UTC time
2. WHEN a record is updated THEN the system SHALL automatically update updated_at to current UTC time
3. WHEN timestamps are stored THEN the system SHALL use timezone-aware datetime
4. WHEN querying records THEN the system SHALL return timestamps in ISO 8601 format
5. IF a model has timestamps THEN the system SHALL use a mixin or base class for consistency
