# Design Document

## Overview

This design document outlines the implementation of the AI-Powered Insights and Recommendations feature for DataInsight Pro Backend. The feature integrates with Claude API (Anthropic) to transform technical profiling results into human-readable insights, actionable recommendations, and code snippets. The system uses context-aware prompting, response caching, and fallback mechanisms to provide reliable AI-powered analysis.

## Architecture

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Insight Generation Flow                   │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
                    ┌──────────────────┐
                    │ ProfilerEngine   │
                    │ (Completes)      │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │  AIService       │
                    │ - Check cache    │
                    │ - Build prompt   │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │ PromptBuilder    │
                    │ - Anonymize data │
                    │ - Add context    │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │  Claude API      │
                    │ (Anthropic SDK)  │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │ ResponseParser   │
                    │ - Extract insights│
                    │ - Parse code     │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │ InsightCategorizer│
                    │ - Assign severity│
                    │ - Prioritize     │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │   PostgreSQL     │
                    │  Store insights  │
                    └──────────────────┘
```

### Component Architecture

```
app/core/ai_engine/
├── __init__.py
├── ai_service.py              # Main AI service orchestrator
├── claude_client.py           # Claude API client wrapper
├── prompt_builder.py          # Context-aware prompt construction
├── response_parser.py         # Parse Claude responses
├── insight_categorizer.py     # Categorize and prioritize insights
├── code_generator.py          # Generate code snippets
├── story_generator.py         # Generate executive summaries
├── anonymizer.py              # Anonymize sensitive data
├── cache_manager.py           # Cache AI responses
└── templates/
    ├── ml_prompt.txt          # ML-specific prompt template
    ├── business_prompt.txt    # Business-specific prompt template
    ├── anomaly_prompt.txt     # Anomaly-specific prompt template
    └── general_prompt.txt     # General prompt template
```

## Components and Interfaces

### 1. AIService (Main Orchestrator)

**Purpose:** Coordinate AI insight generation workflow.

**Interface:**

```python
class AIService:
    """Main AI service for generating insights."""
    
    def __init__(
        self,
        claude_client: ClaudeClient,
        prompt_builder: PromptBuilder,
        response_parser: ResponseParser,
        insight_categorizer: InsightCategorizer,
        code_generator: CodeGenerator,
        story_generator: StoryGenerator,
        cache_manager: CacheManager,
    ):
        self.claude = claude_client
        self.prompt_builder = prompt_builder
        self.parser = response_parser
        self.categorizer = insight_categorizer
        self.code_generator = code_generator
        self.story_generator = story_generator
        self.cache = cache_manager
    
    async def generate_insights(
        self,
        analysis_id: int,
        profile_result: ProfileResult,
        goal_type: AnalysisGoalType,
    ) -> list[Insight]:
        """Generate AI-powered insights from profiling results.
        
        Args:
            analysis_id: Analysis record ID
            profile_result: Complete profiling results
            goal_type: User's analysis goal
            
        Returns:
            List of generated insights
            
        Raises:
            AIServiceException: If insight generation fails
        """
        try:
            # Check cache first
            cache_key = self._generate_cache_key(analysis_id, profile_result)
            cached_insights = await self.cache.get(cache_key)
            if cached_insights:
                return cached_insights
            
            # Build context-aware prompt
            prompt = await self.prompt_builder.build(
                profile_result=profile_result,
                goal_type=goal_type,
            )
            
            # Call Claude API with retry logic
            response = await self.claude.generate(
                prompt=prompt,
                max_tokens=2000,
            )
            
            # Parse response into structured insights
            raw_insights = await self.parser.parse(response)
            
            # Categorize and prioritize
            categorized_insights = await self.categorizer.categorize(
                raw_insights,
                profile_result,
                goal_type,
            )
            
            # Generate code snippets for recommendations
            for insight in categorized_insights:
                if insight.recommendation:
                    insight.code_suggestion = await self.code_generator.generate(
                        insight=insight,
                        language="python",
                    )
            
            # Generate executive summary
            summary = await self.story_generator.generate(
                profile_result=profile_result,
                insights=categorized_insights,
            )
            
            # Add summary as informational insight
            categorized_insights.insert(0, Insight(
                analysis_id=analysis_id,
                severity=InsightSeverity.INFO,
                type=InsightType.QUALITY_ISSUE,
                description=summary,
                recommendation="",
                code_suggestion=None,
            ))
            
            # Cache results
            await self.cache.set(cache_key, categorized_insights, ttl=86400)  # 24 hours
            
            return categorized_insights
            
        except ClaudeAPIException as e:
            # Use fallback rule-based insights
            return await self._generate_fallback_insights(profile_result, goal_type)
        
        except Exception as e:
            raise AIServiceException(f"Failed to generate insights: {str(e)}")
    
    async def _generate_fallback_insights(
        self,
        profile_result: ProfileResult,
        goal_type: AnalysisGoalType,
    ) -> list[Insight]:
        """Generate rule-based insights when AI is unavailable."""
        insights = []
        
        # Critical: High null percentage
        for col_profile in profile_result.column_profiles:
            if col_profile.null_percentage > 50:
                insights.append(Insight(
                    severity=InsightSeverity.CRITICAL,
                    type=InsightType.MISSING_DATA,
                    description=f"Column '{col_profile.column_name}' has {col_profile.null_percentage:.1f}% missing values",
                    recommendation="Consider dropping this column or investigating the cause of missing data",
                ))
        
        # Warning: High duplicates
        if profile_result.quality_metrics.duplicate_percentage > 5:
            insights.append(Insight(
                severity=InsightSeverity.HIGH,
                type=InsightType.DUPLICATES,
                description=f"Dataset contains {profile_result.quality_metrics.duplicate_percentage:.1f}% duplicate rows",
                recommendation="Remove duplicate rows to improve data quality",
            ))
        
        return insights
    
    def _generate_cache_key(
        self,
        analysis_id: int,
        profile_result: ProfileResult,
    ) -> str:
        """Generate cache key based on analysis characteristics."""
        # Use hash of key characteristics
        key_data = f"{analysis_id}_{profile_result.row_count}_{profile_result.column_count}_{profile_result.quality_score}"
        return hashlib.md5(key_data.encode()).hexdigest()
```

### 2. ClaudeClient (API Wrapper)

**Purpose:** Handle Claude API communication with retry logic.

**Interface:**

```python
class ClaudeClient:
    """Claude API client with retry and error handling."""
    
    def __init__(self, api_key: str, model: str = "claude-sonnet-4-20250514"):
        self.client = anthropic.AsyncAnthropic(api_key=api_key)
        self.model = model
        self.token_usage = TokenUsageTracker()
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        retry=retry_if_exception_type((anthropic.RateLimitError, anthropic.APITimeoutError)),
    )
    async def generate(
        self,
        prompt: str,
        max_tokens: int = 2000,
        temperature: float = 0.7,
    ) -> str:
        """Generate response from Claude API.
        
        Args:
            prompt: Input prompt
            max_tokens: Maximum tokens in response
            temperature: Sampling temperature
            
        Returns:
            Generated text response
            
        Raises:
            ClaudeAPIException: If API call fails after retries
        """
        try:
            response = await self.client.messages.create(
                model=self.model,
                max_tokens=max_tokens,
                temperature=temperature,
                messages=[
                    {"role": "user", "content": prompt}
                ],
            )
            
            # Track token usage
            self.token_usage.add(
                input_tokens=response.usage.input_tokens,
                output_tokens=response.usage.output_tokens,
            )
            
            return response.content[0].text
            
        except anthropic.RateLimitError as e:
            raise ClaudeAPIException(f"Rate limit exceeded: {str(e)}")
        
        except anthropic.APITimeoutError as e:
            raise ClaudeAPIException(f"API timeout: {str(e)}")
        
        except Exception as e:
            raise ClaudeAPIException(f"API call failed: {str(e)}")
```

### 3. PromptBuilder (Context-Aware Prompts)

**Purpose:** Construct effective prompts with context and anonymization.

**Interface:**

```python
class PromptBuilder:
    """Build context-aware prompts for Claude API."""
    
    def __init__(self, anonymizer: DataAnonymizer):
        self.anonymizer = anonymizer
        self.templates = self._load_templates()
    
    async def build(
        self,
        profile_result: ProfileResult,
        goal_type: AnalysisGoalType,
    ) -> str:
        """Build prompt from profiling results.
        
        Args:
            profile_result: Complete profiling results
            goal_type: User's analysis goal
            
        Returns:
            Formatted prompt string
        """
        # Select appropriate template
        template = self.templates.get(goal_type.value, self.templates["general"])
        
        # Prepare dataset summary
        dataset_summary = self._create_dataset_summary(profile_result)
        
        # Prepare issues summary
        issues_summary = self._create_issues_summary(profile_result)
        
        # Anonymize sample data
        sample_data = await self.anonymizer.anonymize(
            profile_result.column_profiles[:5]
        )
        
        # Format prompt
        prompt = template.format(
            dataset_summary=dataset_summary,
            issues_summary=issues_summary,
            sample_data=sample_data,
            quality_score=profile_result.quality_score,
            goal=goal_type.value,
        )
        
        return prompt
    
    def _create_dataset_summary(self, profile_result: ProfileResult) -> str:
        """Create human-readable dataset summary."""
        return f"""
Dataset Characteristics:
- Rows: {profile_result.row_count:,}
- Columns: {profile_result.column_count}
- Quality Score: {profile_result.quality_score}/100

Column Types:
{self._format_column_types(profile_result.column_profiles)}
"""
    
    def _create_issues_summary(self, profile_result: ProfileResult) -> str:
        """Create summary of detected issues."""
        issues = []
        
        # Null issues
        high_null_cols = [
            p.column_name for p in profile_result.column_profiles
            if p.null_percentage > 30
        ]
        if high_null_cols:
            issues.append(f"- High null percentage in: {', '.join(high_null_cols)}")
        
        # Duplicates
        if profile_result.quality_metrics.duplicate_percentage > 5:
            issues.append(f"- {profile_result.quality_metrics.duplicate_percentage:.1f}% duplicate rows")
        
        # Outliers
        outlier_cols = [
            p.column_name for p in profile_result.column_profiles
            if p.outliers and p.outliers.get("percentage", 0) > 10
        ]
        if outlier_cols:
            issues.append(f"- Outliers detected in: {', '.join(outlier_cols)}")
        
        return "\n".join(issues) if issues else "No major issues detected"
    
    def _format_column_types(self, column_profiles: list[ColumnProfile]) -> str:
        """Format column types for prompt."""
        type_counts = {}
        for profile in column_profiles:
            type_counts[profile.data_type] = type_counts.get(profile.data_type, 0) + 1
        
        return "\n".join([f"- {dtype}: {count}" for dtype, count in type_counts.items()])
    
    def _load_templates(self) -> dict[str, str]:
        """Load prompt templates."""
        return {
            "ml_preparation": """
You are a data science expert analyzing a dataset for machine learning preparation.

{dataset_summary}

Detected Issues:
{issues_summary}

Sample Data (anonymized):
{sample_data}

Goal: {goal}

Please provide:
1. Critical issues that would prevent ML model training
2. Warnings about data quality that could affect model performance
3. Recommendations for data preprocessing
4. Specific actions to take

Format your response as:
CRITICAL: [issue description] | RECOMMENDATION: [what to do]
WARNING: [issue description] | RECOMMENDATION: [what to do]
INFO: [interesting insight]
""",
            "business_reporting": """
You are a business intelligence expert analyzing a dataset for reporting purposes.

{dataset_summary}

Detected Issues:
{issues_summary}

Goal: {goal}

Please provide:
1. Critical data quality issues that would affect report accuracy
2. Warnings about inconsistencies or formatting issues
3. Recommendations for data standardization
4. Insights about data completeness

Format your response as:
CRITICAL: [issue description] | RECOMMENDATION: [what to do]
WARNING: [issue description] | RECOMMENDATION: [what to do]
INFO: [interesting insight]
""",
            "general": """
You are a data quality expert analyzing a dataset.

{dataset_summary}

Detected Issues:
{issues_summary}

Quality Score: {quality_score}/100

Please provide:
1. Critical data quality issues
2. Warnings about potential problems
3. Positive observations about the data
4. Actionable recommendations

Format your response as:
CRITICAL: [issue description] | RECOMMENDATION: [what to do]
WARNING: [issue description] | RECOMMENDATION: [what to do]
INFO: [interesting insight]
""",
        }
```

### 4. ResponseParser

**Purpose:** Parse Claude responses into structured insights.

**Interface:**

```python
class ResponseParser:
    """Parse Claude API responses into structured insights."""
    
    async def parse(self, response: str) -> list[RawInsight]:
        """Parse Claude response into insights.
        
        Args:
            response: Raw text response from Claude
            
        Returns:
            List of parsed insights
        """
        insights = []
        lines = response.strip().split("\n")
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Parse format: "SEVERITY: description | RECOMMENDATION: action"
            if ":" in line and "|" in line:
                try:
                    severity_part, rec_part = line.split("|", 1)
                    
                    # Extract severity and description
                    severity_match = re.match(r"(CRITICAL|WARNING|INFO):\s*(.+)", severity_part.strip())
                    if not severity_match:
                        continue
                    
                    severity = severity_match.group(1).lower()
                    description = severity_match.group(2).strip()
                    
                    # Extract recommendation
                    rec_match = re.match(r"RECOMMENDATION:\s*(.+)", rec_part.strip())
                    recommendation = rec_match.group(1).strip() if rec_match else ""
                    
                    insights.append(RawInsight(
                        severity=severity,
                        description=description,
                        recommendation=recommendation,
                    ))
                    
                except Exception as e:
                    # Skip malformed lines
                    continue
        
        return insights
```

### 5. InsightCategorizer

**Purpose:** Categorize and prioritize insights.

**Interface:**

```python
class InsightCategorizer:
    """Categorize and prioritize insights."""
    
    async def categorize(
        self,
        raw_insights: list[RawInsight],
        profile_result: ProfileResult,
        goal_type: AnalysisGoalType,
    ) -> list[Insight]:
        """Categorize insights with proper types and priorities.
        
        Args:
            raw_insights: Parsed insights from Claude
            profile_result: Profiling results for context
            goal_type: User's analysis goal
            
        Returns:
            Categorized and prioritized insights
        """
        categorized = []
        
        for raw in raw_insights:
            # Map severity
            severity = self._map_severity(raw.severity)
            
            # Detect insight type from description
            insight_type = self._detect_type(raw.description)
            
            # Calculate priority
            priority = self._calculate_priority(severity, insight_type, goal_type)
            
            # Detect affected columns
            affected_columns = self._extract_columns(raw.description, profile_result)
            
            categorized.append(Insight(
                severity=severity,
                type=insight_type,
                description=raw.description,
                recommendation=raw.recommendation,
                priority=priority,
                affected_columns=affected_columns,
            ))
        
        # Sort by priority
        categorized.sort(key=lambda x: x.priority)
        
        return categorized
    
    def _map_severity(self, severity_str: str) -> InsightSeverity:
        """Map string severity to enum."""
        mapping = {
            "critical": InsightSeverity.CRITICAL,
            "warning": InsightSeverity.HIGH,
            "info": InsightSeverity.INFO,
        }
        return mapping.get(severity_str.lower(), InsightSeverity.MEDIUM)
    
    def _detect_type(self, description: str) -> InsightType:
        """Detect insight type from description."""
        description_lower = description.lower()
        
        if "missing" in description_lower or "null" in description_lower:
            return InsightType.MISSING_DATA
        elif "duplicate" in description_lower:
            return InsightType.DUPLICATES
        elif "outlier" in description_lower:
            return InsightType.OUTLIERS
        elif "type" in description_lower or "mismatch" in description_lower:
            return InsightType.DATA_TYPE_MISMATCH
        elif "pattern" in description_lower:
            return InsightType.PATTERN_VIOLATION
        else:
            return InsightType.QUALITY_ISSUE
    
    def _calculate_priority(
        self,
        severity: InsightSeverity,
        insight_type: InsightType,
        goal_type: AnalysisGoalType,
    ) -> int:
        """Calculate priority (1-5, lower is higher priority)."""
        base_priority = {
            InsightSeverity.CRITICAL: 1,
            InsightSeverity.HIGH: 2,
            InsightSeverity.MEDIUM: 3,
            InsightSeverity.LOW: 4,
            InsightSeverity.INFO: 5,
        }[severity]
        
        # Adjust based on goal
        if goal_type == AnalysisGoalType.ML_PREPARATION:
            if insight_type in {InsightType.MISSING_DATA, InsightType.DUPLICATES}:
                base_priority = max(1, base_priority - 1)
        
        return base_priority
    
    def _extract_columns(
        self,
        description: str,
        profile_result: ProfileResult,
    ) -> list[str]:
        """Extract mentioned column names from description."""
        columns = []
        for profile in profile_result.column_profiles:
            if profile.column_name in description:
                columns.append(profile.column_name)
        return columns
```

### 6. CodeGenerator

**Purpose:** Generate code snippets for recommendations.

**Interface:**

```python
class CodeGenerator:
    """Generate code snippets for recommendations."""
    
    async def generate(
        self,
        insight: Insight,
        language: str = "python",
    ) -> str | None:
        """Generate code snippet for insight.
        
        Args:
            insight: Insight with recommendation
            language: Target language (python, sql, r)
            
        Returns:
            Code snippet or None
        """
        if language == "python":
            return self._generate_python(insight)
        elif language == "sql":
            return self._generate_sql(insight)
        else:
            return None
    
    def _generate_python(self, insight: Insight) -> str:
        """Generate Python code snippet."""
        if insight.type == InsightType.MISSING_DATA:
            if insight.affected_columns:
                col = insight.affected_columns[0]
                return f"""# Remove rows with missing values in '{col}'
df = df.dropna(subset=['{col}'])

# Or fill with median (for numeric columns)
df['{col}'].fillna(df['{col}'].median(), inplace=True)"""
        
        elif insight.type == InsightType.DUPLICATES:
            return """# Remove duplicate rows
df = df.drop_duplicates()

# Or keep first occurrence
df = df.drop_duplicates(keep='first')"""
        
        elif insight.type == InsightType.OUTLIERS:
            if insight.affected_columns:
                col = insight.affected_columns[0]
                return f"""# Remove outliers using IQR method
Q1 = df['{col}'].quantile(0.25)
Q3 = df['{col}'].quantile(0.75)
IQR = Q3 - Q1
df = df[(df['{col}'] >= Q1 - 1.5*IQR) & (df['{col}'] <= Q3 + 1.5*IQR)]"""
        
        return None
    
    def _generate_sql(self, insight: Insight) -> str:
        """Generate SQL code snippet."""
        if insight.type == InsightType.DUPLICATES:
            return """-- Remove duplicates keeping first occurrence
DELETE FROM table_name
WHERE rowid NOT IN (
    SELECT MIN(rowid)
    FROM table_name
    GROUP BY column1, column2, ...
);"""
        
        return None
```

### 7. StoryGenerator

**Purpose:** Generate executive summaries in plain English.

**Interface:**

```python
class StoryGenerator:
    """Generate plain English executive summaries."""
    
    async def generate(
        self,
        profile_result: ProfileResult,
        insights: list[Insight],
    ) -> str:
        """Generate executive summary.
        
        Args:
            profile_result: Profiling results
            insights: Generated insights
            
        Returns:
            Plain English summary
        """
        # Count insights by severity
        critical_count = sum(1 for i in insights if i.severity == InsightSeverity.CRITICAL)
        warning_count = sum(1 for i in insights if i.severity == InsightSeverity.HIGH)
        
        # Build summary
        summary_parts = []
        
        # Dataset description
        summary_parts.append(
            f"This dataset contains {profile_result.row_count:,} rows and "
            f"{profile_result.column_count} columns."
        )
        
        # Quality assessment
        quality_score = profile_result.quality_score
        if quality_score >= 85:
            quality_desc = "excellent"
        elif quality_score >= 70:
            quality_desc = "good"
        elif quality_score >= 50:
            quality_desc = "fair"
        else:
            quality_desc = "poor"
        
        summary_parts.append(
            f"Overall data quality is {quality_desc} ({quality_score}/100)."
        )
        
        # Issues summary
        if critical_count > 0:
            summary_parts.append(
                f"There are {critical_count} critical issue(s) that require immediate attention."
            )
        
        if warning_count > 0:
            summary_parts.append(
                f"Additionally, {warning_count} warning(s) should be reviewed."
            )
        
        # Top issue
        if critical_count > 0 or warning_count > 0:
            top_issue = next(
                (i for i in insights if i.severity in {InsightSeverity.CRITICAL, InsightSeverity.HIGH}),
                None
            )
            if top_issue:
                summary_parts.append(
                    f"The most important issue is: {top_issue.description}"
                )
        else:
            summary_parts.append(
                "No critical issues were detected. The data is ready for analysis."
            )
        
        return " ".join(summary_parts)
```

### 8. DataAnonymizer

**Purpose:** Anonymize sensitive data before sending to Claude API.

**Interface:**

```python
class DataAnonymizer:
    """Anonymize sensitive data for API calls."""
    
    async def anonymize(
        self,
        column_profiles: list[ColumnProfile],
    ) -> str:
        """Anonymize column profiles for sample data.
        
        Args:
            column_profiles: Column profiles to anonymize
            
        Returns:
            Anonymized sample data string
        """
        anonymized = []
        
        for profile in column_profiles:
            col_data = {
                "name": profile.column_name,
                "type": profile.data_type,
            }
            
            # Anonymize based on semantic type
            if profile.semantic_type == "email":
                col_data["sample"] = "user***@domain.com"
            elif profile.semantic_type == "phone":
                col_data["sample"] = "***-***-1234"
            elif profile.semantic_type == "identifier":
                col_data["sample"] = "ID_***"
            elif profile.data_type == "numeric":
                stats = profile.statistics
                col_data["sample"] = f"Range: {stats.get('min', 0)} - {stats.get('max', 0)}"
            else:
                col_data["sample"] = "[anonymized]"
            
            anonymized.append(col_data)
        
        return json.dumps(anonymized, indent=2)
```

### 9. CacheManager

**Purpose:** Cache AI responses to reduce costs.

**Interface:**

```python
class CacheManager:
    """Manage caching of AI responses."""
    
    def __init__(self, redis_client: Redis):
        self.redis = redis_client
        self.prefix = "ai_insights:"
    
    async def get(self, key: str) -> list[Insight] | None:
        """Get cached insights."""
        cached = await self.redis.get(f"{self.prefix}{key}")
        if cached:
            return json.loads(cached)
        return None
    
    async def set(self, key: str, insights: list[Insight], ttl: int = 86400) -> None:
        """Cache insights."""
        await self.redis.setex(
            f"{self.prefix}{key}",
            ttl,
            json.dumps([asdict(i) for i in insights]),
        )
```

## Data Models

### RawInsight

```python
@dataclass
class RawInsight:
    """Parsed insight from Claude response."""
    severity: str
    description: str
    recommendation: str
```

### TokenUsageTracker

```python
class TokenUsageTracker:
    """Track Claude API token usage."""
    
    def __init__(self):
        self.total_input_tokens = 0
        self.total_output_tokens = 0
    
    def add(self, input_tokens: int, output_tokens: int) -> None:
        """Add token usage."""
        self.total_input_tokens += input_tokens
        self.total_output_tokens += output_tokens
    
    def get_cost(self) -> float:
        """Calculate approximate cost in USD."""
        # Claude Sonnet pricing (example)
        input_cost = self.total_input_tokens * 0.003 / 1000
        output_cost = self.total_output_tokens * 0.015 / 1000
        return input_cost + output_cost
```

## Error Handling

### Custom Exceptions

```python
class AIServiceException(AppException):
    """AI service operation failed."""
    def __init__(self, detail: str):
        super().__init__(status_code=500, detail=detail, error_code="AI_SERVICE_ERROR")


class ClaudeAPIException(Exception):
    """Claude API call failed."""
    pass
```

## Testing Strategy

### Unit Tests
- Test prompt building with different goals
- Test response parsing with various formats
- Test insight categorization logic
- Test code generation for each insight type
- Test anonymization for different data types

### Integration Tests
- Test complete flow with mock Claude API
- Test caching behavior
- Test fallback mechanism
- Test retry logic

### Mock Responses
```python
MOCK_CLAUDE_RESPONSE = """
CRITICAL: Column 'customer_id' appears in features and may cause data leakage | RECOMMENDATION: Remove customer_id from feature set before training
WARNING: High correlation (0.95) detected between 'price' and 'total_cost' | RECOMMENDATION: Consider removing one of these features to reduce multicollinearity
INFO: Dataset has good temporal coverage with consistent daily records
"""
```

## Performance Considerations

1. **Caching**: 24-hour cache reduces API calls by ~80%
2. **Batch Processing**: Process multiple analyses in parallel
3. **Async Operations**: All API calls are async
4. **Token Optimization**: Limit sample data to reduce token usage

## Security Considerations

1. **API Key Management**: Store in environment variables
2. **Data Anonymization**: Always anonymize PII before API calls
3. **Rate Limiting**: Respect Claude API rate limits
4. **Cost Monitoring**: Track token usage to prevent runaway costs

## Dependencies

```
anthropic==0.18.0
tenacity==8.2.3
redis==5.0.0
```

This design provides a robust, production-ready AI insights system with proper error handling, caching, and fallback mechanisms.
