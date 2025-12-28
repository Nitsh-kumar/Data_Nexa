# Implementation Plan

- [ ] 1. Set up S3/MinIO storage configuration
  - Add S3 configuration to `app/config.py` (endpoint, credentials, bucket)
  - Add boto3 and aioboto3 to `requirements.txt`
  - Create S3 client initialization in `app/core/storage.py`
  - Add environment variables to `.env.example`
  - _Requirements: 2.2, 2.3_

- [ ] 2. Implement StorageService for S3 operations
  - [ ] 2.1 Create StorageService class in `app/services/storage_service.py`
    - Implement `upload_file()` method with streaming support
    - Implement `download_file()` method
    - Implement `delete_file()` method
    - Implement `generate_presigned_url()` method with 1-hour expiration
    - Add error handling for S3 operations
    - _Requirements: 2.1, 2.2, 2.3, 8.1, 8.2_
  
  - [ ]* 2.2 Write unit tests for StorageService
    - Test file upload with mocked S3 client
    - Test file download
    - Test file deletion
    - Test pre-signed URL generation
    - Test error handling
    - _Requirements: 2.1, 2.2, 8.1_

- [ ] 3. Implement file validation utilities
  - [ ] 3.1 Create FileValidator class in `app/core/file_validator.py`
    - Implement `validate_file_upload()` for extension and size checks
    - Implement `validate_file_content()` for integrity checks
    - Add CSV validation method
    - Add Excel validation method
    - Add JSON validation method
    - Handle empty file detection
    - _Requirements: 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 10.1, 10.2, 10.3, 10.4, 10.5_
  
  - [ ]* 3.2 Write unit tests for FileValidator
    - Test file extension validation
    - Test file size limits for free and pro tiers
    - Test empty file detection
    - Test CSV content validation
    - Test Excel content validation
    - Test JSON content validation
    - Test corrupted file handling
    - _Requirements: 1.1, 1.2, 1.3, 10.1, 10.2, 10.3, 10.4, 10.5_

- [ ] 4. Implement path generation utilities
  - Create `generate_file_path()` function in `app/utils/path_generator.py`
  - Create `sanitize_filename()` function to handle special characters
  - Add UUID prefix generation
  - Implement date-based hierarchy (year/month/day)
  - _Requirements: 2.1, 2.4, 2.5, 11.4, 11.5_

- [ ] 5. Implement metadata extraction
  - [ ] 5.1 Create MetadataExtractor class in `app/core/metadata_extractor.py`
    - Implement `extract()` method with file type detection
    - Implement `_extract_csv()` for CSV files
    - Implement `_extract_excel()` for Excel files (first sheet)
    - Implement `_extract_json()` for JSON files (array and object)
    - Add error handling for extraction failures
    - _Requirements: 3.1, 3.2, 3.3, 3.4, 3.5, 11.1, 11.2, 11.3_
  
  - [ ]* 5.2 Write unit tests for MetadataExtractor
    - Test CSV metadata extraction
    - Test Excel metadata extraction
    - Test JSON array metadata extraction
    - Test JSON object metadata extraction
    - Test error handling for malformed files
    - _Requirements: 3.1, 3.2, 3.3, 3.4, 11.1, 11.2, 11.3_

- [ ] 6. Implement DatasetService business logic
  - [ ] 6.1 Create DatasetService class in `app/services/dataset_service.py`
    - Implement `create_dataset()` method with file upload and validation
    - Implement `_extract_metadata()` private method
    - Implement `list_datasets()` with pagination and filtering
    - Implement `get_dataset()` with access control
    - Implement `delete_dataset()` with cascade and S3 cleanup
    - Implement `get_download_url()` with pre-signed URL generation
    - Add `_get_accessible_workspaces()` helper method
    - Add `_has_workspace_access()` helper method
    - _Requirements: 2.1, 3.1, 4.1, 4.2, 4.3, 4.4, 4.5, 5.1, 5.2, 5.3, 5.4, 5.5, 6.1, 6.2, 6.3, 6.4, 6.5, 7.1, 7.2, 7.3, 7.4, 7.5, 8.1, 8.2, 8.3, 8.4, 9.1, 9.2, 9.3, 9.4, 9.5_
  
  - [ ]* 6.2 Write unit tests for DatasetService
    - Test dataset creation with small files (sync metadata)
    - Test dataset creation with large files (async metadata)
    - Test list datasets with pagination
    - Test list datasets with filtering
    - Test get dataset with access control
    - Test delete dataset with S3 cleanup
    - Test download URL generation
    - Test workspace access validation
    - _Requirements: 4.1, 5.1, 6.1, 7.1, 8.1, 9.1_

- [ ] 7. Create dataset Pydantic schemas
  - Create `app/schemas/dataset.py` with all dataset schemas
  - Implement DatasetBase, DatasetCreate, DatasetUpdate, DatasetResponse
  - Implement DatasetDetailResponse with relationships
  - Implement DatasetListParams for query parameters
  - Implement DatasetDownloadResponse
  - Add validation for file size and workspace_id
  - _Requirements: 12.1, 12.2, 12.3, 12.4, 12.5_

- [ ] 8. Implement dataset upload endpoint
  - [ ] 8.1 Create datasets router in `app/api/v1/datasets.py`
    - Implement POST `/api/v1/datasets/upload` endpoint
    - Add multipart/form-data handling
    - Add workspace access verification
    - Add file validation before upload
    - Return 201 status with dataset object
    - Add OpenAPI documentation with examples
    - _Requirements: 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 9.1, 9.2, 12.1_
  
  - [ ]* 8.2 Write integration tests for upload endpoint
    - Test successful file upload
    - Test file type validation
    - Test file size limit enforcement
    - Test workspace access control
    - Test empty file rejection
    - Test corrupted file rejection
    - _Requirements: 1.1, 1.2, 1.3, 1.6, 9.1, 10.1, 10.4, 10.5_

- [ ] 9. Implement dataset list endpoint
  - [ ] 9.1 Add GET `/api/v1/datasets` endpoint to datasets router
    - Add query parameter parsing
    - Add pagination support (20 items per page)
    - Add filtering by workspace_id and status
    - Add sorting by uploaded_at and name
    - Return 200 status with paginated response
    - Add OpenAPI documentation
    - _Requirements: 5.1, 5.2, 5.3, 5.4, 5.5, 9.3, 12.2_
  
  - [ ]* 9.2 Write integration tests for list endpoint
    - Test pagination
    - Test filtering by workspace
    - Test filtering by status
    - Test sorting
    - Test access control (only accessible workspaces)
    - _Requirements: 5.1, 5.2, 5.3, 5.4, 5.5, 9.3_

- [ ] 10. Implement dataset detail endpoint
  - [ ] 10.1 Add GET `/api/v1/datasets/{dataset_id}` endpoint to datasets router
    - Add dataset ID path parameter
    - Load dataset with relationships (workspace, uploader)
    - Add analyses count
    - Add access control verification
    - Return 200 status with detailed response
    - Return 404 if dataset not found
    - Add OpenAPI documentation
    - _Requirements: 6.1, 6.2, 6.3, 6.4, 6.5, 9.4, 12.2_
  
  - [ ]* 10.2 Write integration tests for detail endpoint
    - Test successful retrieval
    - Test 404 for non-existent dataset
    - Test 403 for unauthorized access
    - Test relationship loading
    - _Requirements: 6.1, 6.5, 9.4_

- [ ] 11. Implement dataset delete endpoint
  - [ ] 11.1 Add DELETE `/api/v1/datasets/{dataset_id}` endpoint to datasets router
    - Add dataset ID path parameter
    - Verify user has delete permission
    - Delete file from S3
    - Delete database record with cascade
    - Return 204 status with no content
    - Return 404 if dataset not found
    - Return 403 if unauthorized
    - Add OpenAPI documentation
    - _Requirements: 7.1, 7.2, 7.3, 7.4, 7.5, 9.4, 12.3_
  
  - [ ]* 11.2 Write integration tests for delete endpoint
    - Test successful deletion
    - Test S3 file deletion
    - Test cascade delete of analyses
    - Test 404 for non-existent dataset
    - Test 403 for unauthorized access
    - _Requirements: 7.1, 7.2, 7.3, 7.4, 7.5_

- [ ] 12. Implement dataset download endpoint
  - [ ] 12.1 Add GET `/api/v1/datasets/{dataset_id}/download` endpoint to datasets router
    - Add dataset ID path parameter
    - Verify user has access
    - Generate pre-signed URL with 1-hour expiration
    - Return 200 status with download URL and metadata
    - Return 404 if dataset or file not found
    - Return 403 if unauthorized
    - Add OpenAPI documentation
    - _Requirements: 8.1, 8.2, 8.3, 8.4, 8.5, 9.4, 12.2_
  
  - [ ]* 12.2 Write integration tests for download endpoint
    - Test pre-signed URL generation
    - Test URL expiration time
    - Test access control
    - Test 404 for non-existent dataset
    - Test 403 for unauthorized access
    - _Requirements: 8.1, 8.2, 8.3, 8.4, 8.5_

- [ ] 13. Add custom exceptions for dataset operations
  - Add StorageException to `app/core/exceptions.py`
  - Add ExtractionException to `app/core/exceptions.py`
  - Update exception handler in `app/main.py`
  - _Requirements: 1.6, 3.5, 10.4, 10.5, 12.4, 12.5_

- [ ] 14. Create workspace access control utilities
  - Create `verify_workspace_access()` function in `app/utils/dependencies.py`
  - Implement workspace membership check
  - Add caching for workspace access checks
  - _Requirements: 9.1, 9.2, 9.3, 9.4, 9.5_

- [ ] 15. Register datasets router in main application
  - Import datasets router in `app/api/v1/__init__.py`
  - Create API router aggregator
  - Register in `app/main.py` with `/api/v1` prefix
  - _Requirements: 12.1, 12.2, 12.3_

- [ ] 16. Update requirements.txt with new dependencies
  - Add boto3==1.34.0 for S3 client
  - Add aioboto3==12.3.0 for async S3 operations
  - Verify pandas==2.2.0 is included
  - Verify openpyxl==3.1.2 is included
  - Verify python-multipart==0.0.6 is included
  - _Requirements: 1.1, 2.2, 3.1_

- [ ] 17. Create docker-compose configuration for MinIO
  - Add MinIO service to `docker-compose.yml`
  - Configure MinIO with access keys
  - Create bucket initialization script
  - Add MinIO console port mapping
  - _Requirements: 2.2_

- [ ] 18. Update .env.example with S3 configuration
  - Add S3_ENDPOINT_URL for MinIO
  - Add S3_ACCESS_KEY and S3_SECRET_KEY
  - Add S3_BUCKET_NAME
  - Add S3_REGION
  - Add MAX_FILE_SIZE_FREE and MAX_FILE_SIZE_PRO
  - _Requirements: 1.4, 1.5, 2.2_

- [ ]* 19. Create background worker for large file processing
  - Create Celery configuration in `app/core/celery_app.py`
  - Create dataset worker in `app/workers/dataset_worker.py`
  - Implement `queue_metadata_extraction` task
  - Add Celery to requirements.txt
  - Add Redis configuration for Celery broker
  - _Requirements: 4.1, 4.2, 4.3, 4.4, 4.5_

- [ ]* 20. Write end-to-end integration tests
  - Create `tests/test_e2e/test_dataset_workflow.py`
  - Test complete upload → list → detail → download → delete flow
  - Test multi-user access control scenarios
  - Test large file async processing
  - Test error scenarios
  - _Requirements: 1.1, 2.1, 3.1, 4.1, 5.1, 6.1, 7.1, 8.1, 9.1_

- [ ] 21. Create API documentation
  - Document all endpoints in `docs/API.md`
  - Include request/response examples
  - Document error codes and messages
  - Add authentication requirements
  - Add rate limiting information
  - _Requirements: 12.1, 12.2, 12.3, 12.4, 12.5_

- [ ] 22. Add logging for dataset operations
  - Add structured logging to DatasetService methods
  - Log file uploads with user_id and workspace_id
  - Log file deletions
  - Log access control violations
  - Log S3 operation failures
  - _Requirements: 2.1, 3.5, 7.1, 9.4_
