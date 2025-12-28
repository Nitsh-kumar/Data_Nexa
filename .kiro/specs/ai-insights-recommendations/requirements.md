# Requirements Document

## Introduction

This spec defines the AI-Powered Insights and Recommendations feature for DataInsight Pro Backend. The feature uses Claude API (Anthropic) to transform technical profiling results into human-readable insights, actionable recommendations, and code snippets. The AI engine provides context-aware analysis based on user goals and generates executive summaries in plain English.

## Requirements

### Requirement 1: Critical Issue Detection

**User Story:** As a user, I want to be alerted to critical data quality issues, so that I can address them before they cause problems.

#### Acceptance Criteria

1. WHEN profiling detects non-unique primary keys THEN the system SHALL generate a critical insight with severity "critical"
2. WHEN a key column has >30% null values THEN the system SHALL flag it as a critical issue
3. WHEN data type mismatches are detected THEN the system SHALL create a critical insight
4. WHEN potential data leakage is detected THEN the system SHALL flag it as critical for ML goals
5. IF multiple critical issues exist THEN the system SHALL prioritize them by impact

### Requirement 2: Warning Generation

**User Story:** As a user, I want to be warned about potential issues, so that I can decide whether to address them.

#### Acceptance Criteria

1. WHEN high correlation (>0.9) is detected between features THEN the system SHALL generate a warning
2. WHEN outliers exceed 10% of data THEN the system SHALL create a warning insight
3. WHEN inconsistent formatting is detected THEN the system SHALL flag it as a warning
4. WHEN missing values exist in recommended fields THEN the system SHALL generate a warning
5. IF warnings are generated THEN the system SHALL include context about why it matters

### Requirement 3: Informational Insights

**User Story:** As a user, I want to understand interesting patterns in my data, so that I can gain insights.

#### Acceptance Criteria

1. WHEN unusual distributions are detected THEN the system SHALL generate informational insights
2. WHEN seasonal patterns are found THEN the system SHALL describe them in plain English
3. WHEN interesting correlations exist THEN the system SHALL highlight them
4. WHEN data quality is good THEN the system SHALL acknowledge strengths
5. IF informational insights are generated THEN the system SHALL make them easy to understand

### Requirement 4: Plain English Explanations

**User Story:** As a non-technical user, I want insights in plain English, so that I can understand them without technical knowledge.

#### Acceptance Criteria

1. WHEN an insight is generated THEN the system SHALL provide a plain English explanation
2. WHEN technical terms are used THEN the system SHALL include definitions or context
3. WHEN numbers are presented THEN the system SHALL include context (e.g., "47 outliers out of 10,000 rows")
4. WHEN recommendations are made THEN the system SHALL explain why they matter
5. IF the user's goal is specified THEN the system SHALL tailor explanations to that context

### Requirement 5: Context-Aware Recommendations

**User Story:** As a user, I want recommendations tailored to my goal, so that they are relevant to my use case.

#### Acceptance Criteria

1. WHEN the goal is ML preparation THEN the system SHALL focus on model-readiness recommendations
2. WHEN the goal is business reporting THEN the system SHALL focus on consistency and accuracy
3. WHEN the goal is anomaly detection THEN the system SHALL focus on unusual patterns
4. WHEN the goal is exploratory THEN the system SHALL provide general data quality recommendations
5. IF no goal is specified THEN the system SHALL provide general recommendations

### Requirement 6: Actionable Fix Suggestions

**User Story:** As a user, I want specific actions I can take, so that I know how to fix issues.

#### Acceptance Criteria

1. WHEN a recommendation is generated THEN the system SHALL include a specific action to take
2. WHEN an action is suggested THEN the system SHALL explain the expected outcome
3. WHEN multiple fixes are possible THEN the system SHALL recommend the best approach
4. WHEN a fix has trade-offs THEN the system SHALL explain them
5. IF a fix is complex THEN the system SHALL break it into steps

### Requirement 7: Code Snippet Generation

**User Story:** As a developer, I want code snippets to implement fixes, so that I can quickly apply recommendations.

#### Acceptance Criteria

1. WHEN a recommendation includes a fix THEN the system SHALL generate Python code snippet
2. WHEN SQL is more appropriate THEN the system SHALL generate SQL code snippet
3. WHEN code is generated THEN the system SHALL include comments explaining each step
4. WHEN code uses libraries THEN the system SHALL specify required imports
5. IF code is complex THEN the system SHALL include usage examples

### Requirement 8: Impact Assessment

**User Story:** As a user, I want to know the impact of each issue, so that I can prioritize my work.

#### Acceptance Criteria

1. WHEN an insight is generated THEN the system SHALL include impact level (Low, Medium, High)
2. WHEN impact is High THEN the system SHALL explain potential consequences of not fixing
3. WHEN impact is Low THEN the system SHALL indicate it's optional
4. WHEN multiple issues exist THEN the system SHALL sort by impact level
5. IF impact depends on context THEN the system SHALL explain the conditions

### Requirement 9: Executive Summary Generation

**User Story:** As a manager, I want a high-level summary, so that I can quickly understand data quality without technical details.

#### Acceptance Criteria

1. WHEN profiling completes THEN the system SHALL generate an executive summary
2. WHEN summary is generated THEN the system SHALL include dataset description
3. WHEN summary is generated THEN the system SHALL include overall quality assessment
4. WHEN summary is generated THEN the system SHALL highlight top 3 issues
5. IF quality is good THEN the system SHALL acknowledge it positively

### Requirement 10: Claude API Integration

**User Story:** As a system, I need to integrate with Claude API, so that I can generate AI-powered insights.

#### Acceptance Criteria

1. WHEN calling Claude API THEN the system SHALL use Anthropic Python SDK
2. WHEN calling Claude API THEN the system SHALL use claude-sonnet-4-20250514 model
3. WHEN calling Claude API THEN the system SHALL set max_tokens to 2000
4. WHEN API call fails THEN the system SHALL retry up to 3 times with exponential backoff
5. IF rate limit is hit THEN the system SHALL queue request for later processing

### Requirement 11: Context-Aware Prompt Construction

**User Story:** As a system, I need to construct effective prompts, so that Claude generates relevant insights.

#### Acceptance Criteria

1. WHEN constructing prompt THEN the system SHALL include dataset characteristics (rows, columns, types)
2. WHEN constructing prompt THEN the system SHALL include user's stated goal
3. WHEN constructing prompt THEN the system SHALL include detected issues from profiling
4. WHEN constructing prompt THEN the system SHALL include sample data (first 5 rows, anonymized)
5. IF sensitive data exists THEN the system SHALL anonymize it before including in prompt

### Requirement 12: Response Parsing and Validation

**User Story:** As a system, I need to parse Claude responses reliably, so that insights are structured correctly.

#### Acceptance Criteria

1. WHEN Claude response is received THEN the system SHALL parse it into structured format
2. WHEN parsing response THEN the system SHALL extract severity, description, and recommendation
3. WHEN parsing response THEN the system SHALL extract code snippets if present
4. WHEN parsing fails THEN the system SHALL log error and use fallback insights
5. IF response is incomplete THEN the system SHALL request completion from Claude

### Requirement 13: Response Caching

**User Story:** As a system, I need to cache AI responses, so that I reduce API costs and improve performance.

#### Acceptance Criteria

1. WHEN an insight is generated THEN the system SHALL cache it for 24 hours
2. WHEN the same dataset is analyzed again THEN the system SHALL return cached insights
3. WHEN dataset changes THEN the system SHALL invalidate cache
4. WHEN cache expires THEN the system SHALL regenerate insights
5. IF cache is full THEN the system SHALL evict oldest entries

### Requirement 14: Error Handling and Fallbacks

**User Story:** As a system, I need robust error handling, so that failures don't break the user experience.

#### Acceptance Criteria

1. WHEN Claude API is unavailable THEN the system SHALL use rule-based fallback insights
2. WHEN API call times out THEN the system SHALL return partial results
3. WHEN API returns error THEN the system SHALL log it and notify administrators
4. WHEN rate limit is exceeded THEN the system SHALL queue requests
5. IF all retries fail THEN the system SHALL return profiling results without AI insights

### Requirement 15: Insight Categorization

**User Story:** As a user, I want insights organized by severity, so that I can focus on what matters most.

#### Acceptance Criteria

1. WHEN insights are returned THEN the system SHALL categorize them as Critical, Warning, or Informational
2. WHEN displaying insights THEN the system SHALL use color coding (Red, Yellow, Blue)
3. WHEN multiple insights exist THEN the system SHALL sort by severity then impact
4. WHEN a category has no insights THEN the system SHALL indicate "No issues found"
5. IF all insights are informational THEN the system SHALL congratulate good data quality

### Requirement 16: Recommendation Prioritization

**User Story:** As a user, I want recommendations prioritized, so that I know what to fix first.

#### Acceptance Criteria

1. WHEN recommendations are generated THEN the system SHALL assign priority (1-5)
2. WHEN priority is assigned THEN the system SHALL consider severity and impact
3. WHEN priority is assigned THEN the system SHALL consider user's goal
4. WHEN displaying recommendations THEN the system SHALL show highest priority first
5. IF two recommendations have same priority THEN the system SHALL sort by ease of implementation

### Requirement 17: Sample Data Anonymization

**User Story:** As a system, I need to anonymize sensitive data, so that it's safe to send to Claude API.

#### Acceptance Criteria

1. WHEN sample data is included in prompt THEN the system SHALL detect PII columns
2. WHEN PII is detected THEN the system SHALL replace values with placeholders
3. WHEN anonymizing emails THEN the system SHALL use format "user***@domain.com"
4. WHEN anonymizing phone numbers THEN the system SHALL use format "***-***-1234"
5. IF column is detected as identifier THEN the system SHALL replace with "ID_1", "ID_2", etc.

### Requirement 18: Multi-Language Code Generation

**User Story:** As a user, I want code in my preferred language, so that I can use it in my workflow.

#### Acceptance Criteria

1. WHEN generating code THEN the system SHALL default to Python
2. WHEN user specifies SQL THEN the system SHALL generate SQL code
3. WHEN user specifies R THEN the system SHALL generate R code
4. WHEN code is generated THEN the system SHALL include language-specific best practices
5. IF language is not supported THEN the system SHALL default to Python with explanation

### Requirement 19: Insight Persistence

**User Story:** As a system, I need to store insights, so that users can review them later.

#### Acceptance Criteria

1. WHEN insights are generated THEN the system SHALL store them in the insights table
2. WHEN storing insights THEN the system SHALL link them to the analysis record
3. WHEN storing insights THEN the system SHALL include all metadata (severity, type, code)
4. WHEN insights are retrieved THEN the system SHALL return them in structured format
5. IF insights are updated THEN the system SHALL maintain version history

### Requirement 20: Performance Requirements

**User Story:** As a user, I want fast insight generation, so that I don't wait long for results.

#### Acceptance Criteria

1. WHEN calling Claude API THEN the system SHALL complete in under 10 seconds
2. WHEN generating insights for large datasets THEN the system SHALL use async processing
3. WHEN multiple insights are needed THEN the system SHALL batch API calls
4. WHEN cache hit occurs THEN the system SHALL return results in under 1 second
5. IF API is slow THEN the system SHALL show progress indicator to user
