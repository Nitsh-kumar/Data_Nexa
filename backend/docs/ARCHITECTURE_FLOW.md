# DataInsight Pro - Architecture Flow Documentation

## Overview

This document explains the complete flow of the DataInsight Pro backend, from user request to AI-generated insights.

## Complete Request Flow

```
┌─────────────┐
│   Client    │
│  (Frontend) │
└──────┬──────┘
       │
       │ 1. POST /api/v1/insights/{analysis_id}/generate
       │    Headers: Authorization: Bearer <JWT>
       │    Query: goal_type=ml_preparation
       │
       ▼
┌─────────────────────────────────────────────────────────────┐
│                    FastAPI Application                       │
│                                                              │
│  ┌────────────────────────────────────────────────────────┐ │
│  │  2. API Layer (insights.py)                            │ │
│  │     - Validates request parameters                     │ │
│  │     - Checks authentication (JWT token)                │ │
│  │     - Verifies user has access to analysis             │ │
│  └────────────────────┬───────────────────────────────────┘ │
│                       │                                      │
│                       ▼                                      │
│  ┌────────────────────────────────────────────────────────┐ │
│  │  3. AIService.generate_insights()                      │ │
│  │     ┌──────────────────────────────────────────────┐   │ │
│  │     │ 3a. Check Redis Cache                        │   │ │
│  │     │     - Generate cache key from analysis ID    │   │ │
│  │     │     - Check if insights already exist        │   │ │
│  │     │     - If HIT: Return cached insights (80%)   │   │ │
│  │     │     - If MISS: Continue to generation        │   │ │
│  │     └──────────────────────────────────────────────┘   │ │
│  │     ┌──────────────────────────────────────────────┐   │ │
│  │     │ 3b. PromptBuilder.build()                    │   │ │
│  │     │     - Select template based on goal_type     │   │ │
│  │     │     - Create dataset summary                 │   │ │
│  │     │     - Create issues summary                  │   │ │
│  │     │     - Anonymize sample data (PII protection) │   │ │
│  │     │     - Format prompt with placeholders        │   │ │
│  │     └──────────────────────────────────────────────┘   │ │
│  │     ┌──────────────────────────────────────────────┐   │ │
│  │     │ 3c. ClaudeClient.generate()                  │   │ │
│  │     │     - Call Claude API with prompt            │   │ │
│  │     │     - Retry on rate limit (3 attempts)       │   │ │
│  │     │     - Track token usage for costs            │   │ │
│  │     │     - If fails: Use fallback insights        │   │ │
│  │     └──────────────────────────────────────────────┘   │ │
│  │     ┌──────────────────────────────────────────────┐   │ │
│  │     │ 3d. ResponseParser.parse()                   │   │ │
│  │     │     - Validate response format               │   │ │
│  │     │     - Parse "SEVERITY: desc | REC: action"   │   │ │
│  │     │     - Extract insights into RawInsight       │   │ │
│  │     └──────────────────────────────────────────────┘   │ │
│  │     ┌──────────────────────────────────────────────┐   │ │
│  │     │ 3e. InsightCategorizer.categorize()          │   │ │
│  │     │     - Detect insight type from description   │   │ │
│  │     │     - Calculate priority (1-5)               │   │ │
│  │     │     - Determine impact (High/Medium/Low)     │   │ │
│  │     │     - Extract affected column names          │   │ │
│  │     └──────────────────────────────────────────────┘   │ │
│  │     ┌──────────────────────────────────────────────┐   │ │
│  │     │ 3f. CodeGenerator.generate()                 │   │ │
│  │     │     - Generate Python code for each insight  │   │ │
│  │     │     - Include pandas operations              │   │ │
│  │     │     - Add comments and imports               │   │ │
│  │     │     - Only for critical/warning insights     │   │ │
│  │     └──────────────────────────────────────────────┘   │ │
│  │     ┌──────────────────────────────────────────────┐   │ │
│  │     │ 3g. StoryGenerator.generate()                │   │ │
│  │     │     - Create executive summary               │   │ │
│  │     │     - Plain English description              │   │ │
│  │     │     - Quality assessment                     │   │ │
│  │     │     - Top issues highlight                   │   │ │
│  │     └──────────────────────────────────────────────┘   │ │
│  │     ┌──────────────────────────────────────────────┐   │ │
│  │     │ 3h. CacheManager.set()                       │   │ │
│  │     │     - Store insights in Redis                │   │ │
│  │     │     - Set 24-hour TTL                        │   │ │
│  │     │     - For future requests                    │   │ │
│  │     └──────────────────────────────────────────────┘   │ │
│  └────────────────────┬───────────────────────────────────┘ │
│                       │                                      │
│                       ▼                                      │
│  ┌────────────────────────────────────────────────────────┐ │
│  │  4. Store Insights in Database                         │ │
│  │     - Save each insight to insights table              │ │
│  │     - Link to analysis_id                              │ │
│  │     - Include all metadata                             │ │
│  └────────────────────┬───────────────────────────────────┘ │
│                       │                                      │
└───────────────────────┼──────────────────────────────────────┘
                        │
                        ▼
                ┌──────────────┐
                │   Response   │
                │   (JSON)     │
                └──────────────┘
```

## Detailed Component Flow

### 1. API Request Handling

**File:** `app/api/v1/insights.py`

```python
POST /api/v1/insights/{analysis_id}/generate
```

**Steps:**
1. FastAPI receives request
2. Validates path parameter (analysis_id must be > 0)
3. Validates query parameter (goal_type)
4. Injects dependencies (AIService, Database session)
5. Checks authentication (JWT token) - TODO
6. Verifies user has access to analysis - TODO

### 2. Cache Check (Performance Optimization)

**File:** `app/core/ai_engine/cache_manager.py`

**Purpose:** Reduce API costs by ~80%

**Steps:**
1. Generate cache key: `MD5(analysis_id + row_count + column_count + quality_score)`
2. Check Redis for existing insights
3. If found (HIT): Return cached insights immediately
4. If not found (MISS): Continue to generation

**Cache Statistics:**
- Hit Rate: ~80% (after initial requests)
- TTL: 24 hours
- Storage: Redis with JSON serialization

### 3. Prompt Building (Context-Aware)

**File:** `app/core/ai_engine/prompt_builder.py`

**Purpose:** Create effective prompts for Claude API

**Steps:**
1. **Select Template** based on goal_type:
   - `ml_preparation` → `ml_prompt.txt`
   - `business_reporting` → `business_prompt.txt`
   - `anomaly_detection` → `anomaly_prompt.txt`
   - `general` → `general_prompt.txt`

2. **Create Dataset Summary:**
   ```
   Dataset Characteristics:
   - Rows: 10,453
   - Columns: 23
   - Quality Score: 82/100
   
   Column Types:
   - numeric: 15 column(s)
   - categorical: 5 column(s)
   - datetime: 2 column(s)
   - text: 1 column(s)
   ```

3. **Create Issues Summary:**
   ```
   - High null percentage (>30%) in: age, income
   - 8.5% duplicate rows detected
   - Outliers detected (>10%) in: price, quantity
   ```

4. **Anonymize Sample Data** (PII Protection):
   ```json
   [
     {
       "name": "email",
       "type": "text",
       "sample": "user***@domain.com",
       "null_percentage": 5.2
     },
     {
       "name": "age",
       "type": "numeric",
       "sample": "Range: 18 - 95",
       "null_percentage": 47.3
     }
   ]
   ```

5. **Format Final Prompt:**
   - Replace placeholders with actual data
   - Include instructions for response format
   - Add goal-specific guidance

### 4. Claude API Call (AI Generation)

**File:** `app/core/ai_engine/claude_client.py`

**Purpose:** Generate insights using Claude AI

**Steps:**
1. **Call Claude API:**
   - Model: `claude-sonnet-4-20250514`
   - Max Tokens: 2000
   - Temperature: 0.7

2. **Retry Logic** (Automatic):
   - Attempt 1: Immediate
   - Attempt 2: Wait 2 seconds
   - Attempt 3: Wait 4 seconds
   - Attempt 4: Wait 8 seconds
   - Only retries on: RateLimitError, APITimeoutError

3. **Track Token Usage:**
   - Input tokens: ~1500 (prompt)
   - Output tokens: ~500 (response)
   - Cost: ~$0.012 per request

4. **Fallback on Failure:**
   - If all retries fail → Use rule-based insights
   - Ensures users always get results

**Expected Response Format:**
```
CRITICAL: Column 'age' has 47% missing values | RECOMMENDATION: Consider dropping this column or investigating the cause
WARNING: High correlation (0.95) between 'price' and 'total_cost' | RECOMMENDATION: Remove one feature to reduce multicollinearity
INFO: Dataset has good temporal coverage with consistent daily records
```

### 5. Response Parsing (Structured Data)

**File:** `app/core/ai_engine/response_parser.py`

**Purpose:** Convert text response to structured insights

**Steps:**
1. **Validate Response:**
   - Check for severity keywords (CRITICAL, WARNING, INFO)
   - Ensure minimum length (>10 characters)

2. **Parse Each Line:**
   - Split by newline
   - Extract severity: `CRITICAL|WARNING|INFO`
   - Extract description: Text before `|`
   - Extract recommendation: Text after `RECOMMENDATION:`

3. **Create RawInsight Objects:**
   ```python
   RawInsight(
       severity="critical",
       description="Column 'age' has 47% missing values",
       recommendation="Consider dropping this column..."
   )
   ```

### 6. Insight Categorization (Prioritization)

**File:** `app/core/ai_engine/insight_categorizer.py`

**Purpose:** Add metadata and prioritize insights

**Steps:**
1. **Detect Type** from description keywords:
   - "missing", "null" → `missing_data`
   - "duplicate" → `duplicates`
   - "outlier" → `outliers`
   - "type", "mismatch" → `data_type_mismatch`
   - "pattern", "format" → `pattern_violation`
   - Default → `quality_issue`

2. **Calculate Priority** (1-5, lower is higher):
   ```python
   Base Priority:
   - critical → 1
   - warning → 2
   - info → 5
   
   Adjustments by Goal:
   - ML preparation: Prioritize missing_data, duplicates
   - Business reporting: Prioritize pattern_violation
   - Anomaly detection: Prioritize outliers
   ```

3. **Determine Impact:**
   - critical → Always "High"
   - warning + (missing_data or duplicates) → "High"
   - warning + other → "Medium"
   - info → "Low"

4. **Extract Affected Columns:**
   - Search description for column names in quotes
   - Match against actual column names from profile

### 7. Code Generation (Actionable Fixes)

**File:** `app/core/ai_engine/code_generator.py`

**Purpose:** Generate executable code to fix issues

**Supported Languages:**
- Python (pandas)
- SQL (PostgreSQL)
- R (dplyr)

**Example Outputs:**

**Missing Data (Python):**
```python
# Handle missing values in 'age'
import pandas as pd

# Option 1: Remove rows with missing values
df = df.dropna(subset=['age'])

# Option 2: Fill with median (for numeric columns)
df['age'].fillna(df['age'].median(), inplace=True)
```

**Duplicates (SQL):**
```sql
-- Remove duplicate rows (PostgreSQL)
DELETE FROM table_name
WHERE ctid NOT IN (
    SELECT MIN(ctid)
    FROM table_name
    GROUP BY column1, column2, column3
);
```

**Outliers (R):**
```r
# Remove outliers from 'price' using IQR method
library(dplyr)

Q1 <- quantile(df$price, 0.25, na.rm = TRUE)
Q3 <- quantile(df$price, 0.75, na.rm = TRUE)
IQR <- Q3 - Q1

lower_bound <- Q1 - 1.5 * IQR
upper_bound <- Q3 + 1.5 * IQR

df <- df %>%
  filter(price >= lower_bound & price <= upper_bound)
```

### 8. Executive Summary (Plain English)

**File:** `app/core/ai_engine/story_generator.py`

**Purpose:** Create non-technical summary

**Components:**
1. **Dataset Description:**
   - Size classification (small/medium/large)
   - Row and column counts

2. **Quality Assessment:**
   - Score interpretation (excellent/good/fair/poor)
   - Based on 0-100 scale

3. **Issues Summary:**
   - Count by severity
   - Highlight top issue

4. **Conclusion:**
   - Actionable next steps
   - Readiness assessment

**Example Output:**
```
This is a medium-sized dataset containing 10,453 rows and 23 columns. 
Overall data quality is good (82/100). There are 2 critical issues that 
require immediate attention. Additionally, 5 warnings should be reviewed. 
The most critical issue is: Column 'age' has 47% missing values. Address 
the critical issues before proceeding with analysis to ensure reliable results.
```

### 9. Caching Results (Cost Optimization)

**File:** `app/core/ai_engine/cache_manager.py`

**Purpose:** Store results for future requests

**Steps:**
1. Serialize insights to JSON
2. Store in Redis with key
3. Set TTL to 24 hours (86400 seconds)
4. Log cache operation

**Benefits:**
- 80% reduction in API calls
- Faster response time (<100ms vs ~3s)
- Lower costs (~$0.0024 vs $0.012 per request)

### 10. Database Storage

**File:** `app/services/analysis_service.py` (TODO)

**Purpose:** Persist insights for retrieval

**Steps:**
1. Create Insight records
2. Link to analysis_id
3. Store all metadata
4. Commit transaction

## Error Handling Flow

```
┌─────────────────┐
│  Any Component  │
│     Fails       │
└────────┬────────┘
         │
         ▼
    ┌─────────┐
    │ Logging │ ← Log error with context
    └────┬────┘
         │
         ▼
┌────────────────────┐
│ Fallback Strategy  │
├────────────────────┤
│ Claude API Fails   │ → Rule-based insights
│ Cache Fails        │ → Continue without cache
│ Code Gen Fails     │ → Skip code, keep insight
│ Summary Fails      │ → Skip summary
└────────┬───────────┘
         │
         ▼
┌────────────────────┐
│ Return Partial     │
│ Results to User    │
└────────────────────┘
```

## Performance Metrics

### Typical Request Times

| Scenario | Time | Cost |
|----------|------|------|
| Cache HIT | ~100ms | $0 |
| Cache MISS (Claude API) | ~3-5s | $0.012 |
| Fallback (no API) | ~500ms | $0 |

### Token Usage

| Component | Tokens | Cost |
|-----------|--------|------|
| Prompt (Input) | ~1500 | $0.0045 |
| Response (Output) | ~500 | $0.0075 |
| **Total** | **~2000** | **$0.012** |

### Cache Performance

| Metric | Value |
|--------|-------|
| Hit Rate | ~80% |
| TTL | 24 hours |
| Average Cost per Analysis | $0.0024 |
| Monthly Cost (1000 analyses) | ~$2.40 |

## Security Considerations

### 1. PII Protection
- All sample data is anonymized before sending to Claude
- Email: `user***@domain.com`
- Phone: `***-***-1234`
- IDs: `ID_***`

### 2. Authentication
- JWT tokens required (TODO: implement)
- Workspace access verification (TODO: implement)

### 3. Rate Limiting
- Consider adding rate limits per user
- Prevent abuse of Claude API

### 4. API Key Security
- Stored in environment variables
- Never logged or exposed
- Rotated regularly

## Monitoring and Observability

### Logs to Monitor

```python
# Success logs
"Generating insights for analysis {id} with goal '{goal}'"
"Cache HIT - Using cached insights"
"Successfully generated {count} insights"

# Warning logs
"Cache MISS - Generating new insights"
"Claude API failed: {error}, using fallback"
"Failed to generate code: {error}"

# Error logs
"Failed to generate insights: {error}"
"Error fetching insights: {error}"
```

### Metrics to Track

1. **API Performance:**
   - Request latency (p50, p95, p99)
   - Error rate
   - Cache hit rate

2. **Claude API:**
   - Token usage per request
   - Cost per analysis
   - Retry rate
   - Failure rate

3. **Business Metrics:**
   - Insights generated per day
   - Most common insight types
   - Average insights per analysis

## Future Enhancements

1. **Streaming Responses:**
   - Stream insights as they're generated
   - Better UX for long-running requests

2. **Batch Processing:**
   - Process multiple analyses in parallel
   - Reduce overall latency

3. **Custom Templates:**
   - Allow users to define custom prompts
   - Industry-specific templates

4. **Feedback Loop:**
   - Learn from user feedback
   - Improve insight quality over time

5. **Multi-Model Support:**
   - Support GPT-4, Gemini
   - Model selection based on use case
