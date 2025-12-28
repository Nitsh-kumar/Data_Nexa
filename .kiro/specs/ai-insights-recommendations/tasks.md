# Implementation Plan

- [x] 1. Set up AI engine package structure and dependencies


  - Create `app/core/ai_engine/` directory
  - Create `__init__.py` with package exports
  - Add anthropic==0.18.0 to `requirements.txt`
  - Add tenacity==8.2.3 for retry logic
  - Add Claude API key to `app/config.py`
  - Add CLAUDE_API_KEY to `.env.example`
  - _Requirements: 10.1, 10.2, 10.3_



- [ ] 2. Implement ClaudeClient with retry logic
  - [ ] 2.1 Create ClaudeClient class in `app/core/ai_engine/claude_client.py`
    - Initialize Anthropic async client
    - Implement `generate()` method with retry decorator
    - Add exponential backoff (2s, 4s, 8s)
    - Handle RateLimitError and APITimeoutError
    - Implement TokenUsageTracker for cost monitoring
    - Add logging for API calls and errors
    - _Requirements: 10.1, 10.2, 10.3, 10.4, 10.5, 20.1_
  
  - [ ]* 2.2 Write unit tests for ClaudeClient
    - Test successful API call
    - Test retry on rate limit
    - Test retry on timeout
    - Test failure after max retries
    - Test token usage tracking
    - Mock Anthropic client




    - _Requirements: 10.1, 10.2, 10.3, 10.4, 10.5_

- [ ] 3. Implement DataAnonymizer for PII protection
  - [ ] 3.1 Create DataAnonymizer class in `app/core/ai_engine/anonymizer.py`
    - Implement `anonymize()` method for column profiles
    - Anonymize email addresses (user***@domain.com)
    - Anonymize phone numbers (***-***-1234)
    - Anonymize identifiers (ID_***)
    - Handle numeric data (show range only)
    - _Requirements: 17.1, 17.2, 17.3, 17.4, 17.5_
  
  - [x]* 3.2 Write unit tests for DataAnonymizer


    - Test email anonymization
    - Test phone anonymization
    - Test identifier anonymization
    - Test numeric data handling
    - Test with various column types
    - _Requirements: 17.1, 17.2, 17.3, 17.4, 17.5_

- [x] 4. Create prompt templates



  - Create `app/core/ai_engine/templates/` directory
  - Create `ml_prompt.txt` for ML preparation goal
  - Create `business_prompt.txt` for business reporting goal
  - Create `anomaly_prompt.txt` for anomaly detection goal
  - Create `general_prompt.txt` for general analysis
  - Include placeholders for dataset_summary, issues_summary, sample_data, quality_score, goal
  - _Requirements: 11.1, 11.2, 11.3, 11.4, 11.5, 5.1, 5.2, 5.3, 5.4, 5.5_

- [ ] 5. Implement PromptBuilder for context-aware prompts
  - [ ] 5.1 Create PromptBuilder class in `app/core/ai_engine/prompt_builder.py`
    - Implement `build()` method to construct prompts
    - Implement `_create_dataset_summary()` helper
    - Implement `_create_issues_summary()` helper
    - Implement `_format_column_types()` helper
    - Load templates from files



    - Integrate DataAnonymizer for sample data
    - _Requirements: 11.1, 11.2, 11.3, 11.4, 11.5, 4.1, 4.2, 4.3, 4.4, 4.5_
  
  - [ ]* 5.2 Write unit tests for PromptBuilder
    - Test prompt building for each goal type
    - Test dataset summary creation
    - Test issues summary creation
    - Test template loading
    - Test with different profiling results
    - _Requirements: 11.1, 11.2, 11.3, 11.4, 5.1_

- [ ] 6. Implement ResponseParser for structured output
  - [ ] 6.1 Create ResponseParser class in `app/core/ai_engine/response_parser.py`
    - Implement `parse()` method to extract insights




    - Parse format: "SEVERITY: description | RECOMMENDATION: action"
    - Handle CRITICAL, WARNING, INFO severities
    - Extract description and recommendation
    - Handle malformed responses gracefully
    - _Requirements: 12.1, 12.2, 12.3, 12.4, 12.5_
  
  - [ ]* 6.2 Write unit tests for ResponseParser
    - Test parsing valid responses
    - Test parsing with multiple insights
    - Test handling malformed lines
    - Test with missing recommendations
    - Test with various formats
    - _Requirements: 12.1, 12.2, 12.3, 12.4, 12.5_

- [ ] 7. Implement InsightCategorizer for prioritization
  - [ ] 7.1 Create InsightCategorizer class in `app/core/ai_engine/insight_categorizer.py`
    - Implement `categorize()` method
    - Implement `_map_severity()` to convert strings to enums
    - Implement `_detect_type()` to identify insight types
    - Implement `_calculate_priority()` based on severity and goal
    - Implement `_extract_columns()` to find affected columns
    - Sort insights by priority
    - _Requirements: 15.1, 15.2, 15.3, 15.4, 15.5, 16.1, 16.2, 16.3, 16.4, 16.5_
  
  - [ ]* 7.2 Write unit tests for InsightCategorizer
    - Test severity mapping
    - Test type detection
    - Test priority calculation
    - Test column extraction
    - Test sorting by priority
    - Test with different goal types
    - _Requirements: 15.1, 15.2, 15.3, 16.1, 16.2_

- [ ] 8. Implement CodeGenerator for code snippets
  - [x] 8.1 Create CodeGenerator class in `app/core/ai_engine/code_generator.py`


    - Implement `generate()` method with language parameter
    - Implement `_generate_python()` for Python code
    - Implement `_generate_sql()` for SQL code
    - Generate code for missing data handling
    - Generate code for duplicate removal
    - Generate code for outlier removal
    - Include comments and imports
    - _Requirements: 7.1, 7.2, 7.3, 7.4, 7.5, 18.1, 18.2, 18.3, 18.4, 18.5_
  
  - [ ]* 8.2 Write unit tests for CodeGenerator
    - Test Python code generation for each insight type
    - Test SQL code generation
    - Test with different affected columns
    - Test code includes proper comments
    - Test code includes imports
    - _Requirements: 7.1, 7.2, 7.3, 7.4, 18.1, 18.2_




- [ ] 9. Implement StoryGenerator for executive summaries
  - [ ] 9.1 Create StoryGenerator class in `app/core/ai_engine/story_generator.py`
    - Implement `generate()` method
    - Create dataset description
    - Create quality assessment (excellent/good/fair/poor)
    - Summarize critical and warning counts
    - Highlight top issue
    - Generate plain English narrative
    - _Requirements: 9.1, 9.2, 9.3, 9.4, 9.5, 4.1, 4.2, 4.3, 4.4, 4.5_
  
  - [ ]* 9.2 Write unit tests for StoryGenerator
    - Test summary generation with various quality scores
    - Test with critical issues
    - Test with no issues
    - Test with warnings only


    - Test narrative quality
    - _Requirements: 9.1, 9.2, 9.3, 9.4, 9.5_

- [ ] 10. Implement CacheManager for response caching
  - [ ] 10.1 Create CacheManager class in `app/core/ai_engine/cache_manager.py`
    - Initialize Redis client
    - Implement `get()` method to retrieve cached insights
    - Implement `set()` method to cache insights with 24-hour TTL
    - Use prefix "ai_insights:" for keys
    - Serialize/deserialize insights as JSON
    - _Requirements: 13.1, 13.2, 13.3, 13.4, 13.5, 20.4_
  
  - [ ]* 10.2 Write unit tests for CacheManager
    - Test cache set and get
    - Test cache expiration




    - Test cache miss
    - Test with different insight structures
    - Mock Redis client
    - _Requirements: 13.1, 13.2, 13.3, 13.4_

- [ ] 11. Implement AIService main orchestrator
  - [ ] 11.1 Create AIService class in `app/core/ai_engine/ai_service.py`
    - Implement `generate_insights()` main method
    - Check cache before API call
    - Build prompt using PromptBuilder
    - Call Claude API via ClaudeClient
    - Parse response using ResponseParser
    - Categorize using InsightCategorizer
    - Generate code snippets for recommendations
    - Generate executive summary
    - Cache results
    - Implement `_generate_fallback_insights()` for API failures
    - Implement `_generate_cache_key()` helper
    - _Requirements: 1.1, 2.1, 3.1, 4.1, 5.1, 6.1, 7.1, 8.1, 9.1, 10.1, 11.1, 12.1, 13.1, 14.1, 14.2, 14.3, 14.4, 14.5, 20.1, 20.2_
  
  - [ ]* 11.2 Write unit tests for AIService
    - Test complete insight generation flow
    - Test cache hit scenario





    - Test cache miss scenario
    - Test fallback mechanism
    - Test with different goal types
    - Mock all dependencies
    - _Requirements: 10.1, 11.1, 12.1, 13.1, 14.1, 14.2_

- [ ] 12. Create AI engine data models
  - Create `app/core/ai_engine/models.py` with dataclasses
  - Define RawInsight dataclass
  - Define TokenUsageTracker class
  - Add helper methods for serialization
  - _Requirements: 12.1, 12.2, 20.5_




- [ ] 13. Add custom exceptions for AI operations
  - Add AIServiceException to `app/core/exceptions.py`
  - Add ClaudeAPIException
  - Update exception handler in `app/main.py`
  - _Requirements: 14.1, 14.2, 14.3, 14.4, 14.5_

- [ ] 14. Integrate AIService with AnalysisService
  - Update `app/services/analysis_service.py`
  - Call AIService after profiling completes
  - Store generated insights in database
  - Handle AI service failures gracefully
  - _Requirements: 19.1, 19.2, 19.3, 19.4, 19.5_

- [x] 15. Create insights API endpoints



  - [ ] 15.1 Create insights router in `app/api/v1/insights.py`
    - Implement GET `/api/v1/insights/{analysis_id}` endpoint


    - Add access control verification
    - Return categorized insights
    - Include executive summary


    - Add OpenAPI documentation
    - _Requirements: 15.1, 15.2, 15.3, 15.4, 15.5_
  
  - [ ]* 15.2 Write integration tests for insights endpoints
    - Test insights retrieval
    - Test access control
    - Test with different analysis states
    - Test error scenarios
    - _Requirements: 15.1, 15.2, 15.3_

- [ ] 16. Create insight Pydantic schemas
  - Update `app/schemas/insight.py` with insight schemas
  - Implement InsightResponse schema
  - Implement InsightListResponse schema
  - Add severity and type enums
  - Include code_suggestion field
  - _Requirements: 19.1, 19.2, 19.3, 19.4, 19.5_

- [ ] 17. Register insights router in main application
  - Import insights router in `app/api/v1/__init__.py`
  - Register in `app/main.py` with `/api/v1` prefix
  - _Requirements: 15.1_

- [ ] 18. Update requirements.txt with AI dependencies
  - Add anthropic==0.18.0
  - Add tenacity==8.2.3
  - Verify redis==5.0.0 is included
  - _Requirements: 10.1, 10.2, 10.3_





- [ ] 19. Create mock Claude responses for testing
  - Create `tests/fixtures/mock_claude_responses.py`
  - Add sample responses for different scenarios
  - Include critical, warning, and info insights
  - Add malformed responses for error testing
  - _Requirements: 12.1, 12.2, 14.1_




- [ ]* 20. Write integration tests for complete AI workflow
  - Create `tests/test_integration/test_ai_insights_workflow.py`
  - Test profiling → AI insights → storage flow
  - Test with mock Claude API
  - Test caching behavior
  - Test fallback mechanism
  - Test with different goal types
  - _Requirements: 10.1, 11.1, 12.1, 13.1, 14.1, 20.1, 20.2_

- [ ]* 21. Create performance and cost monitoring
  - Create `app/core/ai_engine/monitoring.py`
  - Track API call latency
  - Track token usage per request
  - Calculate cost estimates
  - Log metrics to database or monitoring service
  - _Requirements: 20.1, 20.2, 20.3, 20.4, 20.5_

- [ ] 22. Create AI insights documentation
  - Document AI service architecture in `docs/AI_INSIGHTS.md`
  - Explain prompt templates
  - Document insight categories
  - Add examples of generated insights
  - Document cost optimization strategies
  - _Requirements: 4.1, 9.1, 15.1_

- [ ] 23. Add logging for AI operations
  - Add structured logging to AIService
  - Log API calls with token usage
  - Log cache hits and misses
  - Log fallback activations
  - Log errors with context
  - _Requirements: 14.3, 20.1_

- [ ] 24. Create admin endpoint for token usage
  - Create GET `/api/v1/admin/ai-usage` endpoint
  - Return total tokens used
  - Return estimated costs
  - Return cache hit rate
  - Require admin authentication
  - _Requirements: 20.5_
