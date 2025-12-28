# Code Conventions

## API Standards
- Follow REST conventions strictly
- Use proper HTTP methods (GET, POST, PUT, PATCH, DELETE)
- Use plural nouns for resources (`/users`, `/files`)
- Version APIs with prefix (`/api/v1/`)
- Return appropriate status codes

## Code Style
- **Formatter**: Black with max line length 100
- **Import sorting**: isort with Black-compatible profile
- **Type hints**: Required on all functions
- **Docstrings**: Google format for all public functions/classes

## Type Hints
```python
def process_file(file_id: int, user_id: int) -> FileAnalysis:
    """Process uploaded file and return analysis."""
    pass
```

## Docstring Format
```python
def analyze_data(data: pd.DataFrame, options: AnalysisOptions) -> dict[str, Any]:
    """Analyze dataframe and generate insights.
    
    Args:
        data: Input dataframe to analyze
        options: Configuration options for analysis
        
    Returns:
        Dictionary containing analysis results and insights
        
    Raises:
        ValidationError: If data format is invalid
        AnalysisError: If analysis fails
    """
    pass
```

## Error Handling
- Use custom exception classes (inherit from `HTTPException`)
- Handle exceptions at appropriate levels
- Return consistent error responses
- Log errors with context

## Security
- Never commit secrets or credentials
- Use environment variables for configuration
- Validate all user inputs
- Use parameterized queries (SQLAlchemy handles this)
- Implement rate limiting on endpoints
- Use HTTPS in production

## Dependency Injection
```python
from fastapi import Depends

def get_user_service(db: Session = Depends(get_db)) -> UserService:
    return UserService(db)

@router.get("/users/me")
async def get_current_user(
    service: UserService = Depends(get_user_service),
    token: str = Depends(oauth2_scheme)
):
    return await service.get_current_user(token)
```

## Repository Pattern
- Separate data access from business logic
- Repository handles CRUD operations
- Service layer orchestrates business logic
- Keep controllers thin

## Testing
- Write tests for all business logic
- Use pytest fixtures for setup
- Mock external dependencies
- Aim for >80% coverage on services
