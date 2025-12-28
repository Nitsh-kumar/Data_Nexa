# AI Insights Engine Documentation

## Overview

The AI Insights Engine uses Claude API (Anthropic) to generate human-readable insights and actionable recommendations from data profiling results. The engine provides context-aware analysis based on user goals and generates code snippets to fix identified issues.

## Architecture

```
AIService (Main Orchestrator)
├── ClaudeClient (API Communication)
│   ├── Retry Logic (Exponential Backoff)
│   └── Token Usage Tracking
├── PromptBuilder (Context-Aware Prompts)
│   ├── DataAnonymizer (PII Protection)
│   └── Templates (ML/Business/Anomaly/General)
├── ResponseParser (Structured Parsing)
├── InsightCategorizer (Prioritization)
├── CodeGenerator (Python/SQL/R Snippets)
├── StoryGenerator (Executive Summaries)
└── CacheManager (Redis Caching)
```

## Components

### 1. ClaudeClient

**Purpose:** Handle Claude API communication with retry logic and error handling.

**Features:**
- Exponential backoff retry (2s, 4s, 8s)
- Handles rate limits and timeouts
- Token usage tracking for cost monitoring
- Async operations

**Usage:**
```python
from app.core.ai_engine import ClaudeClient

client = ClaudeClient()
response = await client.generate(prompt="Analyze this data...")
stats = client.get_token_stats()
```

### 2. PromptBuilder

**Purpose:** Construct context-aware prompts based on profiling results and user goals.

**Features:**
- Goal-specific templates (ML, Business, Anomaly, General)
- Dataset summary generation
- Issues summary generation
- PII anonymization

**Templates:**
- `ml_prompt.txt`: ML preparation focus
- `business_prompt.txt`: Business reporting focus
- `anomaly_prompt.txt`: Anomaly detection focus
- `general_prompt.txt`: General analysis

**Usage:**
```python
from app.core.ai_engine import PromptBuilder

builder = PromptBuilder()
prompt = await builder.build(
    profile_result=profile_result,
    goal_type="ml_preparation"
)
```

### 3. ResponseParser

**Purpose:** Parse Claude API responses into structured insights.

**Format Expected:**
```
CRITICAL: [issue description] | RECOMMENDATION: [action to take]
WARNING: [issue description] | RECOMMENDATION: [action to take]
INFO: [interesting insight]
```

**Usage:**
```python
from app.core.ai_engine import ResponseParser

parser = ResponseParser()
insights = await parser.parse(claude_response)
```

### 4. InsightCategorizer

**Purpose:** Categorize and prioritize insights.

**Features:**
- Type detection (missing_data, duplicates, outliers, etc.)
- Priority calculation (1-5, lower is higher priority)
- Impact assessment (High/Medium/Low)
- Affected column extraction

**Insight Types:**
- `missing_data`: Null values, missing data
- `duplicates`: Duplicate rows
- `outliers`: Statistical outliers
- `data_type_mismatch`: Type inconsistencies
- `pattern_violation`: Format issues
- `quality_issue`: General quality problems

**Usage:**
```python
from app.core.ai_engine import InsightCategorizer

categorizer = InsightCategorizer()
categorized = await categorizer.categorize(
    raw_insights=raw_insights,
    profile_result=profile_result,
    goal_type="ml_preparation"
)
```

### 5. CodeGenerator

**Purpose:** Generate code snippets to fix identified issues.

**Supported Languages:**
- Python (pandas operations)
- SQL (PostgreSQL compatible)
- R (dplyr operations)

**Supported Operations:**
- Missing data handling (dropna, fillna, imputation)
- Duplicate removal
- Outlier detection and removal (IQR, Z-score)
- Data type conversion
- Pattern standardization
- High correlation handling
- High cardinality reduction

**Usage:**
```python
from app.core.ai_engine import CodeGenerator

generator = CodeGenerator()
code = await generator.generate(
    insight=insight,
    language="python"
)
```

**Example Output:**
```python
# Handle missing values in 'age'
import pandas as pd

# Option 1: Remove rows with missing values
df = df.dropna(subset=['age'])

# Option 2: Fill with median (for numeric columns)
df['age'].fillna(df['age'].median(), inplace=True)
```

### 6. StoryGenerator

**Purpose:** Generate plain English executive summaries.

**Features:**
- Dataset description
- Quality assessment (excellent/good/fair/poor)
- Issue counts by severity
- Top issue highlights
- Actionable conclusions

**Usage:**
```python
from app.core.ai_engine import StoryGenerator

generator = StoryGenerator()
summary = await generator.generate(
    profile_result=profile_result,
    insights=insights
)
```

**Example Output:**
```
This is a medium-sized dataset containing 10,453 rows and 23 columns. 
Overall data quality is good (82/100). There are 2 critical issues that 
require immediate attention. The most critical issue is: Column 'customer_id' 
has 47% missing values. Address the critical issues before proceeding with 
analysis to ensure reliable results.
```

### 7. CacheManager

**Purpose:** Cache AI responses to reduce costs and improve performance.

**Features:**
- Redis-based caching
- 24-hour TTL (configurable)
- Cache statistics (hit rate, counts)
- Automatic key generation

**Usage:**
```python
from app.core.ai_engine import CacheManager

cache = CacheManager()
cached = await cache.get(key)
if not cached:
    # Generate insights
    await cache.set(key, insights, ttl=86400)
```

**Cache Statistics:**
```python
stats = await cache.get_stats()
# {
#     "cached_insights_count": 42,
#     "redis_hits": 150,
#     "redis_misses": 30,
#     "hit_rate": 83.33
# }
```

### 8. AIService

**Purpose:** Main orchestrator that coordinates all components.

**Features:**
- Cache-first strategy
- Fallback to rule-based insights
- Code generation for recommendations
- Executive summary generation
- Comprehensive error handling

**Usage:**
```python
from app.core.ai_engine import AIService

ai_service = AIService()
insights = await ai_service.generate_insights(
    analysis_id=123,
    profile_result=profile_result,
    goal_type="ml_preparation"
)
```

## API Endpoints

### GET /api/v1/insights/{analysis_id}

Get insights for an analysis.

**Parameters:**
- `analysis_id` (path): Analysis ID
- `page` (query): Page number (default: 1)
- `page_size` (query): Items per page (default: 20)
- `severity` (query): Filter by severity (optional)

**Response:**
```json
{
  "items": [
    {
      "id": 1,
      "analysis_id": 123,
      "severity": "critical",
      "type": "missing_data",
      "description": "Column 'age' has 47% missing values",
      "recommendation": "Consider dropping this column or investigating the cause",
      "code_suggestion": "df = df.dropna(subset=['age'])",
      "priority": 1,
      "affected_columns": ["age"],
      "impact": "High",
      "created_at": "2025-01-15T10:30:00Z"
    }
  ],
  "total": 15,
  "page": 1,
  "page_size": 20,
  "pages": 1
}
```

### GET /api/v1/insights/{analysis_id}/summary

Get insights summary.

**Response:**
```json
{
  "critical_count": 2,
  "warning_count": 5,
  "info_count": 8,
  "total_count": 15,
  "executive_summary": "This dataset contains 10,453 rows..."
}
```

### POST /api/v1/insights/{analysis_id}/generate

Generate insights for an analysis.

**Parameters:**
- `analysis_id` (path): Analysis ID
- `goal_type` (query): Analysis goal (default: "general")

**Response:** Same as GET endpoint

### GET /api/v1/insights/stats/tokens

Get token usage statistics.

**Response:**
```json
{
  "input_tokens": 15000,
  "output_tokens": 3000,
  "total_tokens": 18000,
  "estimated_cost_usd": 0.09
}
```

### GET /api/v1/insights/stats/cache

Get cache statistics.

**Response:**
```json
{
  "cached_insights_count": 42,
  "redis_hits": 150,
  "redis_misses": 30,
  "hit_rate": 83.33
}
```

## Configuration

### Environment Variables

```bash
# Claude API
CLAUDE_API_KEY=your_api_key_here
CLAUDE_MODEL=claude-sonnet-4-20250514
CLAUDE_MAX_TOKENS=2000
CLAUDE_TEMPERATURE=0.7

# Redis Cache
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0
REDIS_PASSWORD=
CACHE_TTL=86400  # 24 hours
```

### Cost Optimization

1. **Caching**: 24-hour cache reduces API calls by ~80%
2. **Token Limits**: Max 2000 tokens per request
3. **Fallback**: Rule-based insights when API unavailable
4. **Monitoring**: Track token usage and costs

**Estimated Costs (Claude Sonnet):**
- Input: $0.003 per 1K tokens
- Output: $0.015 per 1K tokens
- Average request: ~1500 input + 500 output = $0.012
- With 80% cache hit rate: ~$0.0024 per analysis

## Error Handling

### Fallback Mechanism

If Claude API fails, the system automatically falls back to rule-based insights:

1. **Critical**: High null percentage (>50%)
2. **Warning**: High duplicates (>5%)
3. **Warning**: High outliers (>10%)
4. **Info**: Quality summary

### Retry Logic

- 3 retry attempts
- Exponential backoff: 2s, 4s, 8s
- Handles rate limits and timeouts

### Error Types

- `AIServiceException`: General AI service error
- `ClaudeAPIException`: Claude API specific error
- `ValidationException`: Invalid input
- `NotFoundException`: Resource not found

## Best Practices

### 1. Goal Selection

Choose the appropriate goal type for your use case:
- `ml_preparation`: Focus on model readiness
- `business_reporting`: Focus on consistency
- `anomaly_detection`: Focus on unusual patterns
- `general`: Balanced analysis

### 2. Cache Management

- Cache is automatically managed
- 24-hour TTL is optimal for most use cases
- Clear cache if data changes significantly

### 3. Cost Management

- Monitor token usage regularly
- Use caching effectively
- Consider batch processing for multiple analyses

### 4. Code Snippets

- Review generated code before execution
- Test on sample data first
- Adapt to your specific use case

## Troubleshooting

### Issue: Claude API Rate Limit

**Solution:** The system automatically retries with exponential backoff. If persistent, check your API quota.

### Issue: Cache Not Working

**Solution:** Verify Redis is running and connection settings are correct.

### Issue: Poor Quality Insights

**Solution:** 
- Ensure profiling results are complete
- Try different goal types
- Check prompt templates

### Issue: High Costs

**Solution:**
- Verify caching is enabled
- Check cache hit rate
- Consider reducing max_tokens

## Examples

### Complete Workflow

```python
from app.core.ai_engine import AIService

# Initialize service
ai_service = AIService()

# Generate insights
insights = await ai_service.generate_insights(
    analysis_id=123,
    profile_result=profile_result,
    goal_type="ml_preparation"
)

# Access insights
for insight in insights:
    print(f"{insight.severity}: {insight.description}")
    if insight.code_suggestion:
        print(f"Code: {insight.code_suggestion}")

# Get statistics
token_stats = ai_service.get_token_stats()
cache_stats = await ai_service.get_cache_stats()

print(f"Cost: ${token_stats['estimated_cost_usd']}")
print(f"Cache hit rate: {cache_stats['hit_rate']}%")
```

## Future Enhancements

1. **Multi-Model Support**: Support for GPT-4, Gemini
2. **Custom Templates**: User-defined prompt templates
3. **Insight Feedback**: Learn from user feedback
4. **Batch Processing**: Process multiple analyses in parallel
5. **Advanced Caching**: Semantic caching for similar analyses
6. **Cost Alerts**: Notify when costs exceed threshold
