# Code Review Guide - AI Insights Engine

## Quick Reference for Reviewers

This guide helps code reviewers understand the AI Insights Engine implementation quickly.

## File Organization

### Core AI Engine (`app/core/ai_engine/`)

| File | Purpose | Key Functions | Review Focus |
|------|---------|---------------|--------------|
| `ai_service.py` | Main orchestrator | `generate_insights()` | Flow logic, error handling |
| `claude_client.py` | API wrapper | `generate()` | Retry logic, token tracking |
| `prompt_builder.py` | Prompt creation | `build()` | Template selection, anonymization |
| `response_parser.py` | Parse responses | `parse()` | Regex patterns, validation |
| `insight_categorizer.py` | Categorization | `categorize()` | Type detection, priority calc |
| `code_generator.py` | Code snippets | `generate()` | Code templates, language support |
| `story_generator.py` | Summaries | `generate()` | Plain English generation |
| `cache_manager.py` | Redis caching | `get()`, `set()` | TTL, serialization |
| `anonymizer.py` | PII protection | `anonymize()` | Data masking |
| `models.py` | Data structures | N/A | Dataclass definitions |

### API Layer (`app/api/v1/`)

| File | Purpose | Endpoints | Review Focus |
|------|---------|-----------|--------------|
| `insights.py` | REST API | 5 endpoints | Request validation, error handling |

### Schemas (`app/schemas/`)

| File | Purpose | Models | Review Focus |
|------|---------|--------|--------------|
| `insight.py` | Pydantic schemas | 8 schemas | Validation rules, field types |

## Key Design Patterns

### 1. Dependency Injection

```python
# AIService accepts all dependencies
def __init__(
    self,
    claude_client: ClaudeClient | None = None,
    prompt_builder: PromptBuilder | None = None,
    # ... other dependencies
):
    # Use provided or create default
    self.claude = claude_client or ClaudeClient()
```

**Why:** Testability, flexibility, loose coupling

### 2. Retry with Exponential Backoff

```python
@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=2, max=10),
    retry=retry_if_exception_type((RateLimitError, APITimeoutError))
)
async def generate(self, prompt: str) -> str:
```

**Why:** Handle transient failures, respect rate limits

### 3. Cache-First Strategy

```python
# Check cache first
cached = await self.cache.get(key)
if cached:
    return cached

# Generate if not cached
result = await self._generate()

# Cache for future
await self.cache.set(key, result, ttl=86400)
```

**Why:** Reduce costs, improve performance

### 4. Fallback Mechanism

```python
try:
    response = await self.claude.generate(prompt)
except ClaudeAPIException:
    # Use rule-based fallback
    return await self._generate_fallback_insights()
```

**Why:** Reliability, always return results

## Critical Code Sections

### 1. AIService.generate_insights() - Main Flow

**Location:** `app/core/ai_engine/ai_service.py:60-180`

**What to Review:**
- ✅ Cache check happens first
- ✅ All steps have try-except blocks
- ✅ Fallback is triggered on any failure
- ✅ Results are cached before returning
- ✅ Logging at each step

**Common Issues:**
- ❌ Missing error handling
- ❌ Not caching results
- ❌ Not using fallback on failure

### 2. ClaudeClient.generate() - API Call

**Location:** `app/core/ai_engine/claude_client.py:80-150`

**What to Review:**
- ✅ Retry decorator is configured correctly
- ✅ Token usage is tracked
- ✅ Only specific errors trigger retry
- ✅ Timeout is reasonable

**Common Issues:**
- ❌ Retrying on all errors (expensive)
- ❌ Not tracking token usage
- ❌ Missing timeout configuration

### 3. ResponseParser.parse() - Text Parsing

**Location:** `app/core/ai_engine/response_parser.py:20-80`

**What to Review:**
- ✅ Regex patterns are correct
- ✅ Handles malformed input gracefully
- ✅ Validates before parsing
- ✅ Logs parsing failures

**Common Issues:**
- ❌ Regex too strict (misses valid input)
- ❌ Crashes on unexpected format
- ❌ No validation before parsing

### 4. CacheManager - Redis Operations

**Location:** `app/core/ai_engine/cache_manager.py:30-120`

**What to Review:**
- ✅ TTL is set correctly (24 hours)
- ✅ Serialization handles all data types
- ✅ Errors don't crash the app
- ✅ Connection is properly managed

**Common Issues:**
- ❌ No TTL (cache grows forever)
- ❌ Serialization fails on complex objects
- ❌ Redis errors crash the app

## Security Checklist

### PII Protection

```python
# ✅ GOOD: Anonymize before sending to API
sample_data = await self.anonymizer.anonymize(column_profiles)

# ❌ BAD: Send raw data to API
sample_data = column_profiles  # Contains PII!
```

### API Key Management

```python
# ✅ GOOD: Load from environment
api_key = settings.CLAUDE_API_KEY

# ❌ BAD: Hardcode in code
api_key = "sk-ant-..."  # Never do this!
```

### Input Validation

```python
# ✅ GOOD: Validate with Pydantic
analysis_id: int = Path(..., gt=0)

# ❌ BAD: No validation
analysis_id = request.path_params["analysis_id"]
```

## Performance Checklist

### Async Operations

```python
# ✅ GOOD: Use async/await
async def generate_insights(self):
    response = await self.claude.generate(prompt)

# ❌ BAD: Blocking operations
def generate_insights(self):
    response = self.claude.generate_sync(prompt)  # Blocks!
```

### Caching

```python
# ✅ GOOD: Cache expensive operations
cached = await self.cache.get(key)
if cached:
    return cached

# ❌ BAD: No caching
result = await expensive_operation()  # Every time!
```

### Database Queries

```python
# ✅ GOOD: Use pagination
query = query.limit(page_size).offset(offset)

# ❌ BAD: Load all records
query = select(Insight)  # Could be millions!
```

## Testing Checklist

### Unit Tests

- [ ] Test happy path
- [ ] Test error cases
- [ ] Test edge cases (empty input, null values)
- [ ] Mock external dependencies (Claude API, Redis)
- [ ] Test retry logic
- [ ] Test fallback mechanism

### Integration Tests

- [ ] Test complete flow end-to-end
- [ ] Test with real Redis (not mocked)
- [ ] Test cache hit and miss scenarios
- [ ] Test concurrent requests
- [ ] Test timeout scenarios

### Performance Tests

- [ ] Measure response time (target: <5s)
- [ ] Measure cache hit rate (target: >70%)
- [ ] Measure token usage (target: <2500 per request)
- [ ] Test with large datasets

## Common Pitfalls

### 1. Not Handling Async Properly

```python
# ❌ BAD: Forgetting await
result = self.cache.get(key)  # Returns coroutine, not result!

# ✅ GOOD: Always await async functions
result = await self.cache.get(key)
```

### 2. Swallowing Exceptions

```python
# ❌ BAD: Silent failure
try:
    result = await operation()
except Exception:
    pass  # Error is lost!

# ✅ GOOD: Log and handle
try:
    result = await operation()
except Exception as e:
    logger.error(f"Operation failed: {e}")
    raise
```

### 3. Not Closing Resources

```python
# ❌ BAD: Resource leak
redis = Redis()
# ... use redis ...
# Never closed!

# ✅ GOOD: Use context manager or close explicitly
async with Redis() as redis:
    # ... use redis ...
# Automatically closed
```

### 4. Hardcoding Values

```python
# ❌ BAD: Magic numbers
await cache.set(key, value, 86400)  # What is 86400?

# ✅ GOOD: Use constants
CACHE_TTL = 86400  # 24 hours
await cache.set(key, value, CACHE_TTL)
```

## Code Quality Metrics

### Complexity

| File | Lines | Functions | Complexity | Status |
|------|-------|-----------|------------|--------|
| `ai_service.py` | ~400 | 5 | Medium | ✅ OK |
| `claude_client.py` | ~150 | 4 | Low | ✅ Good |
| `code_generator.py` | ~350 | 10 | Medium | ✅ OK |
| `prompt_builder.py` | ~200 | 8 | Low | ✅ Good |

### Test Coverage (Target: >80%)

| Component | Coverage | Status |
|-----------|----------|--------|
| Core Logic | 0% | ⚠️ TODO |
| API Endpoints | 0% | ⚠️ TODO |
| Utilities | 0% | ⚠️ TODO |

## Review Checklist

### Code Quality

- [ ] All functions have docstrings
- [ ] Type hints on all parameters
- [ ] No hardcoded values
- [ ] Proper error handling
- [ ] Logging at appropriate levels
- [ ] No commented-out code
- [ ] Consistent naming conventions

### Functionality

- [ ] Implements requirements correctly
- [ ] Handles edge cases
- [ ] Has fallback mechanisms
- [ ] Validates all inputs
- [ ] Returns appropriate status codes

### Performance

- [ ] Uses async/await correctly
- [ ] Implements caching
- [ ] No N+1 queries
- [ ] Reasonable timeouts
- [ ] Efficient algorithms

### Security

- [ ] No hardcoded secrets
- [ ] Input validation
- [ ] PII is anonymized
- [ ] SQL injection prevention
- [ ] Rate limiting considered

### Testing

- [ ] Unit tests exist
- [ ] Integration tests exist
- [ ] Edge cases covered
- [ ] Mocks used appropriately
- [ ] Tests are maintainable

## Questions for Author

1. **Why was this approach chosen?**
   - Alternative approaches considered?
   - Trade-offs made?

2. **How is this tested?**
   - Unit tests?
   - Integration tests?
   - Manual testing done?

3. **What are the failure modes?**
   - What happens if Claude API is down?
   - What happens if Redis is down?
   - What happens with invalid input?

4. **Performance considerations?**
   - Expected response time?
   - Expected token usage?
   - Cache hit rate target?

5. **Security considerations?**
   - PII handling?
   - API key management?
   - Input validation?

## Approval Criteria

### Must Have ✅

- [ ] Code compiles/runs without errors
- [ ] All functions have docstrings
- [ ] Error handling is comprehensive
- [ ] Logging is appropriate
- [ ] No security vulnerabilities
- [ ] Follows project conventions

### Should Have 📋

- [ ] Unit tests with >70% coverage
- [ ] Integration tests for main flows
- [ ] Performance benchmarks
- [ ] Documentation is complete
- [ ] Code is well-commented

### Nice to Have 🎯

- [ ] >90% test coverage
- [ ] Performance optimizations
- [ ] Additional features
- [ ] Comprehensive examples

## Resources

- **Architecture Flow:** `docs/ARCHITECTURE_FLOW.md`
- **AI Insights Guide:** `docs/AI_INSIGHTS.md`
- **API Documentation:** http://localhost:8000/docs
- **Design Specs:** `.kiro/specs/ai-insights-recommendations/`
