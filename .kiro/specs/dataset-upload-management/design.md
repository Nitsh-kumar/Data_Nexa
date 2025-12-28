# Design Document

## Overview

This design document outlines the implementation of the Dataset Upload and Management feature for DataInsight Pro Backend. The feature enables users to upload data files (CSV, Excel, JSON), extract metadata, store files securely in S3-compatible storage, and manage datasets through RESTful API endpoints with proper access control and background processing for large files.

## Architecture

### High-Level Data Flow

```
┌─────────────┐
│   Client    │
│  (Frontend) │
└──────┬──────┘
       │ 1. POST /api/v1/datasets/upload
       │    (multipart/form-data)
       ▼
┌─────────────────────────────────────────────────────────┐
│                    FastAPI Backend                       │
│                                                          │
│  ┌──────────────────────────────────────────────────┐  │
│  │  API Layer (datasets.py)                         │  │
│  │  - Validate file type, size                      │  │
│  │  - Check workspace access                        │  │
│  └────────────────┬─────────────────────────────────┘  │
│                   │                                     │
│                   ▼                                     │
│  ┌──────────────────────────────────────────────────┐  │
│  │  DatasetService                                  │  │
│  │  - Validate file integrity                       │  │
│  │  - Generate unique file path                     │  │
│  │  - Upload to S3                                  │  │
│  │  - Create database record                        │  │
│  │  - Queue background job (if large)               │  │
│  └────────────────┬─────────────────────────────────┘  │
│                   │                                     │
└───────────────────┼─────────────────────────────────────┘
                    │
        ┌───────────┴───────────┐
        │                       │
        ▼                       ▼
┌──────────────┐      ┌──────────────────┐
│  PostgreSQL  │      │   S3 / MinIO     │
│  (Metadata)  │      │  (File Storage)  │
└──────────────┘      └──────────────────┘
        │
        │ 2. If file > 10MB
        ▼
┌──────────────────┐
│  Celery Worker   │
│  - Extract       │
│    metadata      │
│  - Update status │
└──────────────────┘
```

### Component Architecture

```
app/
├── api/v1/
│   └── datasets.py          # API endpoints
├── services/
│   ├── dataset_service.py   # Business logic
│   └── storage_service.py   # S3/MinIO operations
├── core/
│   ├── file_validator.py    # File validation
│   └── metadata_extractor.py # Extract row/column counts
├── utils/
│   ├── file_handler.py      # File operations
│   └── path_generator.py    # Unique path generation
└── workers/
    └── dataset_worker.py    # Background jobs
```

## Components and Interfaces

### 1. API Layer (datasets.py)

**Purpose:** Handle HTTP requests for dataset operations.

**Endpoints:**

```python
POST   /api/v1/datasets/upload
GET    /api/v1/datasets
GET    /api/v1/datasets/{dataset_id}
DELETE /api/v1/datasets/{dataset_id}
GET    /api/v1/datasets/{dataset_id}/download
```

**Endpoint Details:**

#### POST /api/v1/datasets/upload

**Request:**
```python
Content-Type: multipart/form-data

Fields:
- file: UploadFile (required)
- workspace_id: int (required)
- name: str (optional, defaults to filename)
```

**Response (201):**
```json
{
  "id": 1,
  "name": "sales_data.csv",
  "file_size": 1048576,
  "row_count": null,
  "column_count": null,
  "status": "processing",
  "workspace_id": 1,
  "uploaded_by": 1,
  "uploaded_at": "2025-01-15T10:30:00Z"
}
```

**Implementation:**
```python
@router.post("/upload", response_model=DatasetResponse, status_code=201)
async def upload_dataset(
    file: UploadFile = File(...),
    workspace_id: int = Form(...),
    name: str | None = Form(None),
    current_user: User = Depends(get_current_user),
    dataset_service: DatasetService = Depends(get_dataset_service),
    db: AsyncSession = Depends(get_db),
) -> DatasetResponse:
    """Upload a new dataset file."""
    # Validate workspace access
    await verify_workspace_access(workspace_id, current_user.id, db)
    
    # Validate file
    validate_file_upload(file, current_user.tier)
    
    # Upload and create dataset
    dataset = await dataset_service.create_dataset(
        file=file,
        workspace_id=workspace_id,
        user_id=current_user.id,
        name=name or file.filename,
    )
    
    return dataset
```

#### GET /api/v1/datasets

**Query Parameters:**
```python
- workspace_id: int (optional)
- status: DatasetStatus (optional)
- page: int (default: 1)
- page_size: int (default: 20, max: 100)
- sort_by: str (default: "uploaded_at")
- sort_order: str (default: "desc")
```

**Response (200):**
```json
{
  "items": [
    {
      "id": 1,
      "name": "sales_data.csv",
      "file_size": 1048576,
      "row_count": 10453,
      "column_count": 23,
      "status": "completed",
      "workspace_id": 1,
      "uploaded_at": "2025-01-15T10:30:00Z"
    }
  ],
  "total": 45,
  "page": 1,
  "page_size": 20,
  "pages": 3
}
```

#### GET /api/v1/datasets/{dataset_id}

**Response (200):**
```json
{
  "id": 1,
  "name": "sales_data.csv",
  "file_path": "workspaces/1/2025/01/uuid-sales_data.csv",
  "file_size": 1048576,
  "row_count": 10453,
  "column_count": 23,
  "status": "completed",
  "workspace": {
    "id": 1,
    "name": "Marketing Analytics"
  },
  "uploader": {
    "id": 1,
    "full_name": "John Doe",
    "email": "john@example.com"
  },
  "uploaded_at": "2025-01-15T10:30:00Z",
  "analyses_count": 3
}
```

#### DELETE /api/v1/datasets/{dataset_id}

**Response (204):** No content

#### GET /api/v1/datasets/{dataset_id}/download

**Response (200):**
```json
{
  "download_url": "https://s3.amazonaws.com/bucket/path?signature=...",
  "expires_at": "2025-01-15T11:30:00Z",
  "filename": "sales_data.csv"
}
```

### 2. DatasetService

**Purpose:** Orchestrate dataset operations and business logic.

**Interface:**

```python
class DatasetService:
    def __init__(
        self,
        db: AsyncSession,
        storage_service: StorageService,
        file_validator: FileValidator,
        metadata_extractor: MetadataExtractor,
    ):
        self.db = db
        self.storage = storage_service
        self.validator = file_validator
        self.extractor = metadata_extractor
    
    async def create_dataset(
        self,
        file: UploadFile,
        workspace_id: int,
        user_id: int,
        name: str,
    ) -> Dataset:
        """Create a new dataset from uploaded file.
        
        Args:
            file: Uploaded file object
            workspace_id: Target workspace ID
            user_id: Uploader user ID
            name: Dataset name
            
        Returns:
            Created dataset object
            
        Raises:
            ValidationException: If file validation fails
            StorageException: If file upload fails
        """
        # Validate file integrity
        await self.validator.validate_file_content(file)
        
        # Generate unique file path
        file_path = generate_file_path(workspace_id, file.filename)
        
        # Upload to S3
        await self.storage.upload_file(file, file_path)
        
        # Create database record
        dataset = Dataset(
            name=name,
            file_path=file_path,
            file_size=file.size,
            workspace_id=workspace_id,
            uploaded_by=user_id,
            status=DatasetStatus.PENDING,
        )
        self.db.add(dataset)
        await self.db.commit()
        await self.db.refresh(dataset)
        
        # Queue background job for metadata extraction
        if file.size > 10 * 1024 * 1024:  # 10MB
            await queue_metadata_extraction.delay(dataset.id)
        else:
            # Extract metadata synchronously for small files
            await self._extract_metadata(dataset)
        
        return dataset
    
    async def _extract_metadata(self, dataset: Dataset) -> None:
        """Extract metadata from dataset file."""
        try:
            dataset.status = DatasetStatus.PROCESSING
            await self.db.commit()
            
            # Download file from S3
            file_content = await self.storage.download_file(dataset.file_path)
            
            # Extract metadata based on file type
            metadata = await self.extractor.extract(file_content, dataset.name)
            
            # Update dataset
            dataset.row_count = metadata.row_count
            dataset.column_count = metadata.column_count
            dataset.status = DatasetStatus.COMPLETED
            await self.db.commit()
            
        except Exception as e:
            dataset.status = DatasetStatus.FAILED
            dataset.error_message = str(e)
            await self.db.commit()
            raise
    
    async def list_datasets(
        self,
        user_id: int,
        workspace_id: int | None = None,
        status: DatasetStatus | None = None,
        page: int = 1,
        page_size: int = 20,
        sort_by: str = "uploaded_at",
        sort_order: str = "desc",
    ) -> tuple[list[Dataset], int]:
        """List datasets with pagination and filtering."""
        # Build query
        query = select(Dataset).join(Workspace)
        
        # Filter by accessible workspaces
        accessible_workspaces = await self._get_accessible_workspaces(user_id)
        query = query.where(Dataset.workspace_id.in_(accessible_workspaces))
        
        # Apply filters
        if workspace_id:
            query = query.where(Dataset.workspace_id == workspace_id)
        if status:
            query = query.where(Dataset.status == status)
        
        # Count total
        count_query = select(func.count()).select_from(query.subquery())
        total = await self.db.scalar(count_query)
        
        # Apply sorting
        sort_column = getattr(Dataset, sort_by)
        if sort_order == "desc":
            sort_column = sort_column.desc()
        query = query.order_by(sort_column)
        
        # Apply pagination
        query = query.limit(page_size).offset((page - 1) * page_size)
        
        # Execute query
        result = await self.db.execute(query)
        datasets = result.scalars().all()
        
        return datasets, total
    
    async def get_dataset(
        self,
        dataset_id: int,
        user_id: int,
    ) -> Dataset:
        """Get dataset by ID with access control."""
        query = (
            select(Dataset)
            .options(
                selectinload(Dataset.workspace),
                selectinload(Dataset.uploader),
            )
            .where(Dataset.id == dataset_id)
        )
        
        result = await self.db.execute(query)
        dataset = result.scalar_one_or_none()
        
        if not dataset:
            raise NotFoundException("Dataset not found")
        
        # Verify access
        if not await self._has_workspace_access(user_id, dataset.workspace_id):
            raise UnauthorizedException("Access denied")
        
        return dataset
    
    async def delete_dataset(
        self,
        dataset_id: int,
        user_id: int,
    ) -> None:
        """Delete dataset and associated file."""
        dataset = await self.get_dataset(dataset_id, user_id)
        
        # Delete file from S3
        await self.storage.delete_file(dataset.file_path)
        
        # Delete database record (cascade deletes analyses)
        await self.db.delete(dataset)
        await self.db.commit()
    
    async def get_download_url(
        self,
        dataset_id: int,
        user_id: int,
    ) -> dict[str, str]:
        """Generate pre-signed download URL."""
        dataset = await self.get_dataset(dataset_id, user_id)
        
        # Generate pre-signed URL (expires in 1 hour)
        url = await self.storage.generate_presigned_url(
            dataset.file_path,
            expiration=3600,
        )
        
        return {
            "download_url": url,
            "expires_at": datetime.utcnow() + timedelta(hours=1),
            "filename": dataset.name,
        }
```

### 3. StorageService

**Purpose:** Handle S3/MinIO file operations.

**Interface:**

```python
class StorageService:
    def __init__(self, s3_client: Any, bucket_name: str):
        self.s3 = s3_client
        self.bucket = bucket_name
    
    async def upload_file(
        self,
        file: UploadFile,
        file_path: str,
    ) -> None:
        """Upload file to S3.
        
        Args:
            file: File to upload
            file_path: Destination path in S3
            
        Raises:
            StorageException: If upload fails
        """
        try:
            await self.s3.upload_fileobj(
                file.file,
                self.bucket,
                file_path,
                ExtraArgs={"ContentType": file.content_type},
            )
        except Exception as e:
            raise StorageException(f"Failed to upload file: {str(e)}")
    
    async def download_file(self, file_path: str) -> bytes:
        """Download file from S3."""
        response = await self.s3.get_object(Bucket=self.bucket, Key=file_path)
        return await response["Body"].read()
    
    async def delete_file(self, file_path: str) -> None:
        """Delete file from S3."""
        await self.s3.delete_object(Bucket=self.bucket, Key=file_path)
    
    async def generate_presigned_url(
        self,
        file_path: str,
        expiration: int = 3600,
    ) -> str:
        """Generate pre-signed download URL."""
        url = await self.s3.generate_presigned_url(
            "get_object",
            Params={"Bucket": self.bucket, "Key": file_path},
            ExpiresIn=expiration,
        )
        return url
```

### 4. FileValidator

**Purpose:** Validate file type, size, and integrity.

**Interface:**

```python
class FileValidator:
    ALLOWED_EXTENSIONS = {".csv", ".xlsx", ".xls", ".json"}
    MAX_FILE_SIZE_FREE = 100 * 1024 * 1024  # 100MB
    MAX_FILE_SIZE_PRO = 5 * 1024 * 1024 * 1024  # 5GB
    
    def validate_file_upload(
        self,
        file: UploadFile,
        user_tier: str,
    ) -> None:
        """Validate file before upload.
        
        Args:
            file: Uploaded file
            user_tier: User's subscription tier
            
        Raises:
            ValidationException: If validation fails
        """
        # Check file extension
        ext = Path(file.filename).suffix.lower()
        if ext not in self.ALLOWED_EXTENSIONS:
            raise ValidationException(
                f"File type not supported. Allowed: {', '.join(self.ALLOWED_EXTENSIONS)}"
            )
        
        # Check file size
        max_size = (
            self.MAX_FILE_SIZE_PRO
            if user_tier == "pro"
            else self.MAX_FILE_SIZE_FREE
        )
        if file.size > max_size:
            raise ValidationException(
                f"File size exceeds limit of {max_size / (1024**2):.0f}MB"
            )
        
        # Check file is not empty
        if file.size == 0:
            raise ValidationException("File is empty")
    
    async def validate_file_content(self, file: UploadFile) -> None:
        """Validate file content integrity.
        
        Args:
            file: Uploaded file
            
        Raises:
            ValidationException: If file is corrupted or invalid
        """
        ext = Path(file.filename).suffix.lower()
        
        # Read first chunk for validation
        chunk = await file.read(8192)
        await file.seek(0)  # Reset file pointer
        
        try:
            if ext == ".csv":
                self._validate_csv(chunk)
            elif ext in {".xlsx", ".xls"}:
                self._validate_excel(chunk)
            elif ext == ".json":
                self._validate_json(chunk)
        except Exception as e:
            raise ValidationException(f"File is corrupted or invalid: {str(e)}")
    
    def _validate_csv(self, chunk: bytes) -> None:
        """Validate CSV content."""
        try:
            csv.reader(io.StringIO(chunk.decode("utf-8")))
        except Exception:
            raise ValidationException("Invalid CSV format")
    
    def _validate_excel(self, chunk: bytes) -> None:
        """Validate Excel content."""
        # Check for Excel magic bytes
        if not chunk.startswith(b"PK"):  # ZIP format
            raise ValidationException("Invalid Excel format")
    
    def _validate_json(self, chunk: bytes) -> None:
        """Validate JSON content."""
        try:
            json.loads(chunk.decode("utf-8"))
        except json.JSONDecodeError:
            raise ValidationException("Invalid JSON format")
```

### 5. MetadataExtractor

**Purpose:** Extract row count, column count, and other metadata.

**Interface:**

```python
class MetadataExtractor:
    async def extract(
        self,
        file_content: bytes,
        filename: str,
    ) -> DatasetMetadata:
        """Extract metadata from file.
        
        Args:
            file_content: File content as bytes
            filename: Original filename
            
        Returns:
            Extracted metadata
            
        Raises:
            ExtractionException: If extraction fails
        """
        ext = Path(filename).suffix.lower()
        
        if ext == ".csv":
            return await self._extract_csv(file_content)
        elif ext in {".xlsx", ".xls"}:
            return await self._extract_excel(file_content)
        elif ext == ".json":
            return await self._extract_json(file_content)
        else:
            raise ExtractionException(f"Unsupported file type: {ext}")
    
    async def _extract_csv(self, content: bytes) -> DatasetMetadata:
        """Extract metadata from CSV."""
        df = pd.read_csv(io.BytesIO(content))
        return DatasetMetadata(
            row_count=len(df),
            column_count=len(df.columns),
        )
    
    async def _extract_excel(self, content: bytes) -> DatasetMetadata:
        """Extract metadata from Excel (first sheet)."""
        df = pd.read_excel(io.BytesIO(content), sheet_name=0)
        return DatasetMetadata(
            row_count=len(df),
            column_count=len(df.columns),
        )
    
    async def _extract_json(self, content: bytes) -> DatasetMetadata:
        """Extract metadata from JSON."""
        data = json.loads(content.decode("utf-8"))
        
        if isinstance(data, list):
            df = pd.DataFrame(data)
        elif isinstance(data, dict):
            df = pd.DataFrame([data])
        else:
            raise ExtractionException("JSON must be array or object")
        
        return DatasetMetadata(
            row_count=len(df),
            column_count=len(df.columns),
        )
```

### 6. Path Generator Utility

**Purpose:** Generate unique file paths.

**Implementation:**

```python
def generate_file_path(workspace_id: int, filename: str) -> str:
    """Generate unique file path for S3 storage.
    
    Args:
        workspace_id: Workspace ID
        filename: Original filename
        
    Returns:
        Unique file path
        
    Example:
        workspaces/1/2025/01/15/uuid-sales_data.csv
    """
    # Sanitize filename
    safe_filename = sanitize_filename(filename)
    
    # Generate UUID prefix
    unique_id = uuid.uuid4().hex[:8]
    
    # Build path with date hierarchy
    now = datetime.utcnow()
    path = (
        f"workspaces/{workspace_id}/"
        f"{now.year}/{now.month:02d}/{now.day:02d}/"
        f"{unique_id}-{safe_filename}"
    )
    
    return path


def sanitize_filename(filename: str) -> str:
    """Sanitize filename by removing special characters.
    
    Args:
        filename: Original filename
        
    Returns:
        Sanitized filename
    """
    # Remove special characters except dots, dashes, underscores
    safe_name = re.sub(r"[^\w\s.-]", "", filename)
    
    # Replace spaces with underscores
    safe_name = safe_name.replace(" ", "_")
    
    # Limit length
    name, ext = os.path.splitext(safe_name)
    if len(name) > 100:
        name = name[:100]
    
    return f"{name}{ext}"
```

## Data Models

### DatasetMetadata

```python
@dataclass
class DatasetMetadata:
    """Extracted dataset metadata."""
    row_count: int
    column_count: int
```

### Updated Dataset Schema

```python
class DatasetDetailResponse(DatasetResponse):
    """Detailed dataset response with relationships."""
    workspace: WorkspaceResponse
    uploader: UserResponse
    analyses_count: int
    
    model_config = ConfigDict(from_attributes=True)


class DatasetListParams(BaseModel):
    """Query parameters for dataset list."""
    workspace_id: int | None = None
    status: DatasetStatus | None = None
    page: int = Field(1, ge=1)
    page_size: int = Field(20, ge=1, le=100)
    sort_by: str = Field("uploaded_at", pattern="^(uploaded_at|name|file_size)$")
    sort_order: str = Field("desc", pattern="^(asc|desc)$")


class DatasetDownloadResponse(BaseModel):
    """Download URL response."""
    download_url: str
    expires_at: datetime
    filename: str
```

## Error Handling

### Custom Exceptions

```python
class StorageException(AppException):
    """Storage operation failed."""
    def __init__(self, detail: str):
        super().__init__(status_code=500, detail=detail, error_code="STORAGE_ERROR")


class ExtractionException(AppException):
    """Metadata extraction failed."""
    def __init__(self, detail: str):
        super().__init__(status_code=422, detail=detail, error_code="EXTRACTION_ERROR")
```

### Error Responses

```json
{
  "detail": "File size exceeds limit of 100MB",
  "error_code": "VALIDATION_ERROR"
}
```

## Testing Strategy

### Unit Tests

1. **FileValidator Tests**
   - Test file extension validation
   - Test file size limits for different tiers
   - Test empty file detection
   - Test content validation for each format

2. **MetadataExtractor Tests**
   - Test CSV extraction
   - Test Excel extraction (first sheet)
   - Test JSON extraction (array and object)
   - Test error handling for corrupted files

3. **Path Generator Tests**
   - Test unique path generation
   - Test filename sanitization
   - Test special character handling

### Integration Tests

1. **Upload Flow**
   - Test successful upload
   - Test large file async processing
   - Test workspace access control
   - Test file size limit enforcement

2. **List and Filter**
   - Test pagination
   - Test filtering by workspace and status
   - Test sorting

3. **Download**
   - Test pre-signed URL generation
   - Test access control

4. **Delete**
   - Test cascade delete
   - Test S3 file deletion

## Performance Considerations

### File Upload Optimization

1. **Streaming Upload**: Use streaming for large files to avoid memory issues
2. **Multipart Upload**: Use S3 multipart upload for files > 100MB
3. **Compression**: Consider gzip compression for CSV files

### Metadata Extraction

1. **Sampling**: For very large files, sample first N rows for quick metadata
2. **Caching**: Cache metadata extraction results
3. **Parallel Processing**: Process multiple files concurrently

### Database Queries

1. **Indexes**: Ensure indexes on workspace_id, status, uploaded_at
2. **Eager Loading**: Use selectinload for relationships
3. **Pagination**: Always use LIMIT/OFFSET

## Security Considerations

1. **File Validation**: Validate file type and content before processing
2. **Path Traversal**: Sanitize filenames to prevent path traversal attacks
3. **Access Control**: Verify workspace membership before all operations
4. **Pre-signed URLs**: Set short expiration (1 hour) for download URLs
5. **Rate Limiting**: Limit upload requests per user (e.g., 10/minute)

## Dependencies

### New Packages Required

```
boto3==1.34.0           # AWS S3 client
aioboto3==12.3.0        # Async S3 client
pandas==2.2.0           # Data processing
openpyxl==3.1.2         # Excel support
python-multipart==0.0.6 # File upload support
```

### Configuration

```python
# app/config.py additions
class Settings(BaseSettings):
    # ... existing settings ...
    
    # S3 Storage
    S3_ENDPOINT_URL: str = "http://localhost:9000"  # MinIO for local
    S3_ACCESS_KEY: str
    S3_SECRET_KEY: str
    S3_BUCKET_NAME: str = "datainsight-datasets"
    S3_REGION: str = "us-east-1"
    
    # File Upload
    MAX_FILE_SIZE_FREE: int = 100 * 1024 * 1024  # 100MB
    MAX_FILE_SIZE_PRO: int = 5 * 1024 * 1024 * 1024  # 5GB
    ALLOWED_FILE_EXTENSIONS: list[str] = [".csv", ".xlsx", ".xls", ".json"]
    
    # Background Jobs
    CELERY_BROKER_URL: str = "redis://localhost:6379/0"
    CELERY_RESULT_BACKEND: str = "redis://localhost:6379/0"
```

## Future Enhancements

1. **Chunked Upload**: Support resumable uploads for very large files
2. **File Preview**: Generate preview of first N rows
3. **Column Type Detection**: Auto-detect column data types
4. **Data Validation**: Validate data against user-defined schemas
5. **Version Control**: Track dataset versions
6. **Sharing**: Share datasets with external users via links
