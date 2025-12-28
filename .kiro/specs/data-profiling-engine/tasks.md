# Implementation Plan

- [ ] 1. Set up profiler package structure
  - Create `app/core/profiler/` directory
  - Create `__init__.py` with package exports
  - Add profiler dependencies to `requirements.txt` (scipy for statistics)
  - _Requirements: 17.1, 17.2, 17.3_

- [ ] 2. Implement TypeDetector for column type detection
  - [ ] 2.1 Create TypeDetector class in `app/core/profiler/type_detector.py`
    - Implement `detect()` method for basic type detection (numeric, categorical, datetime, text, boolean)
    - Implement `_detect_semantic_type()` for email, phone, URL patterns
    - Add identifier detection (all unique values)
    - Handle mixed type detection with confidence scoring
    - _Requirements: 1.1, 1.2, 1.3, 1.4, 1.5_
  
  - [ ]* 2.2 Write unit tests for TypeDetector
    - Test numeric type detection
    - Test categorical type detection
    - Test datetime type detection
    - Test email pattern detection
    - Test phone pattern detection
    - Test URL pattern detection
    - Test identifier detection
    - Test mixed type handling
    - _Requirements: 1.1, 1.2, 1.3_

- [ ] 3. Implement StatisticsCalculator for type-specific statistics
  - [ ] 3.1 Create StatisticsCalculator class in `app/core/profiler/statistics_calculator.py`
    - Implement `calculate_numeric()` with min, max, mean, median, std_dev, quartiles, IQR, skewness, kurtosis
    - Implement `calculate_categorical()` with unique count, mode, frequency distribution
    - Implement `calculate_datetime()` with min/max dates, range, frequency detection
    - Implement `calculate_text()` with length statistics and pattern detection
    - Implement `_calculate_histogram()` helper for numeric distributions
    - Implement `_detect_frequency()` helper for time series
    - Implement `_find_common_patterns()` helper for text patterns
    - _Requirements: 2.1, 2.2, 2.3, 2.4, 2.5, 3.1, 3.2, 3.3, 3.4, 3.5, 4.1, 4.2, 4.3, 4.4, 5.1, 5.2, 5.3, 5.4_
  
  - [ ]* 3.2 Write unit tests for StatisticsCalculator
    - Test numeric statistics calculation
    - Test categorical statistics calculation
    - Test datetime statistics calculation
    - Test text statistics calculation
    - Test histogram generation
    - Test frequency detection
    - Test pattern detection
    - _Requirements: 2.1, 2.2, 2.3, 2.4, 2.5, 3.1, 3.2, 3.3, 4.1, 4.2, 5.1_

- [ ] 4. Implement NullAnalyzer for missing data analysis
  - [ ] 4.1 Create NullAnalyzer class in `app/core/profiler/null_analyzer.py`
    - Implement `analyze()` method to calculate null count and percentage
    - Implement `classify_pattern()` to detect MCAR, MAR, MNAR patterns
    - Implement `detect_correlation()` to find correlated missing values
    - Add threshold-based flagging (>50% nulls)
    - _Requirements: 6.1, 6.2, 6.3, 6.4, 6.5_
  
  - [ ]* 4.2 Write unit tests for NullAnalyzer
    - Test null count calculation
    - Test null percentage calculation
    - Test MCAR pattern detection
    - Test MAR pattern detection
    - Test MNAR pattern detection
    - Test correlation detection
    - _Requirements: 6.1, 6.2, 6.3_

- [ ] 5. Implement OutlierDetector for anomaly detection
  - [ ] 5.1 Create OutlierDetector class in `app/core/profiler/outlier_detector.py`
    - Implement `detect()` method using IQR method
    - Add Z-score method as alternative (|z| > 3)
    - Calculate outlier count and percentage
    - Return sample outlier values
    - Add bounds calculation (Q1-1.5*IQR, Q3+1.5*IQR)
    - _Requirements: 8.1, 8.2, 8.3, 8.4, 8.5_
  
  - [ ]* 5.2 Write unit tests for OutlierDetector
    - Test IQR method
    - Test Z-score method
    - Test outlier count calculation
    - Test bounds calculation
    - Test with no outliers
    - Test with many outliers
    - _Requirements: 8.1, 8.2, 8.3_

- [ ] 6. Implement CorrelationAnalyzer for feature relationships
  - [ ] 6.1 Create CorrelationAnalyzer class in `app/core/profiler/correlation_analyzer.py`
    - Implement `calculate()` method for Pearson correlation matrix
    - Filter to numeric columns only
    - Identify high correlation pairs (|r| > 0.8)
    - Format results as nested dictionary
    - _Requirements: 9.1, 9.2, 9.3, 9.4, 9.5_
  
  - [ ]* 6.2 Write unit tests for CorrelationAnalyzer
    - Test correlation matrix calculation
    - Test high correlation detection
    - Test with no numeric columns
    - Test with single numeric column
    - Test perfect correlation detection
    - _Requirements: 9.1, 9.2, 9.5_

- [ ] 7. Implement PatternDetector for data patterns
  - Create PatternDetector class in `app/core/profiler/pattern_detector.py`
  - Implement `detect()` method for common patterns
  - Add regex patterns for phone, ZIP code, SSN formats
  - Detect seasonality in datetime columns
  - Detect gaps in time series
  - _Requirements: 4.3, 4.4, 5.4, 5.5_

- [ ] 8. Implement ColumnAnalyzer to orchestrate column analysis
  - [ ] 8.1 Create ColumnAnalyzer class in `app/core/profiler/column_analyzer.py`
    - Implement `analyze()` method that coordinates all analyzers
    - Call TypeDetector for type detection
    - Call StatisticsCalculator based on detected type
    - Call NullAnalyzer for missing data
    - Call OutlierDetector for numeric columns
    - Call PatternDetector for pattern detection
    - Return ColumnProfile dataclass
    - _Requirements: 1.1, 2.1, 3.1, 4.1, 5.1, 6.1, 8.1_
  
  - [ ]* 8.2 Write unit tests for ColumnAnalyzer
    - Test numeric column analysis
    - Test categorical column analysis
    - Test datetime column analysis
    - Test text column analysis
    - Test with all null column
    - Test with mixed types
    - _Requirements: 1.1, 2.1, 3.1, 4.1, 5.1, 6.1_

- [ ] 9. Implement QualityScorer for overall quality assessment
  - [ ] 9.1 Create QualityScorer class in `app/core/profiler/quality_scorer.py`
    - Implement `calculate()` method with 0-100 scoring
    - Apply null penalty (max -30 points)
    - Apply duplicate penalty (max -20 points)
    - Apply outlier penalty (max -15 points)
    - Ensure score stays between 0 and 100
    - _Requirements: 10.1, 10.2, 10.3, 10.4, 10.5_
  
  - [ ]* 9.2 Write unit tests for QualityScorer
    - Test perfect quality score (100)
    - Test with high nulls
    - Test with high duplicates
    - Test with many outliers
    - Test combined penalties
    - Test score boundaries
    - _Requirements: 10.1, 10.2, 10.3, 10.4, 10.5_

- [ ] 10. Implement ML-specific goal analyzer
  - [ ] 10.1 Create MLAnalyzer class in `app/core/profiler/goal_analyzers/ml_analyzer.py`
    - Implement `analyze()` method for ML-specific checks
    - Check for high cardinality categorical features (>100 unique)
    - Detect constant or near-constant features
    - Check for class imbalance in target variable
    - Detect potential data leakage
    - Return list of GoalInsight objects
    - _Requirements: 11.1, 11.2, 11.3, 11.4, 11.5_
  
  - [ ]* 10.2 Write unit tests for MLAnalyzer
    - Test high cardinality detection
    - Test constant feature detection
    - Test class imbalance detection
    - Test data leakage detection
    - _Requirements: 11.1, 11.2, 11.3, 11.4_

- [ ] 11. Implement Business-specific goal analyzer
  - Create BusinessAnalyzer class in `app/core/profiler/goal_analyzers/business_analyzer.py`
  - Implement `analyze()` method for business checks
  - Check for standard date formats
  - Verify categorical values match expected lists
  - Check for negative values in amount fields
  - Detect inconsistent naming conventions
  - _Requirements: 12.1, 12.2, 12.3, 12.4, 12.5_

- [ ] 12. Implement Anomaly-specific goal analyzer
  - Create AnomalyAnalyzer class in `app/core/profiler/goal_analyzers/anomaly_analyzer.py`
  - Implement `analyze()` method for anomaly checks
  - Flag unusual distributions (high skewness)
  - Detect sudden changes in time series
  - Identify rare categorical values (<1% frequency)
  - Detect unexpected value ranges
  - _Requirements: 13.1, 13.2, 13.3, 13.4, 13.5_

- [ ] 13. Implement GoalAnalyzerFactory
  - Create GoalAnalyzerFactory class in `app/core/profiler/goal_analyzers/__init__.py`
  - Implement `create()` method to return appropriate analyzer
  - Support ml_preparation, general_audit, data_quality, exploratory goals
  - _Requirements: 11.1, 12.1, 13.1_

- [ ] 14. Implement ProfilerEngine main orchestrator
  - [ ] 14.1 Create ProfilerEngine class in `app/core/profiler/base_profiler.py`
    - Implement `profile_dataset()` main method
    - Implement `_load_data()` with file type detection
    - Implement `_load_csv_chunked()` for large CSV files
    - Implement `_analyze_columns()` to process all columns
    - Implement `_check_quality()` for dataset-level checks
    - Implement `_calculate_correlations()` for numeric columns
    - Implement `_generate_recommendations()` based on findings
    - Add duplicate detection logic
    - _Requirements: 1.1, 2.1, 3.1, 4.1, 5.1, 6.1, 7.1, 8.1, 9.1, 10.1, 14.1, 14.2, 14.3, 14.4, 14.5_
  
  - [ ]* 14.2 Write unit tests for ProfilerEngine
    - Test complete profiling workflow
    - Test chunked CSV loading
    - Test Excel file loading
    - Test JSON file loading
    - Test duplicate detection
    - Test correlation calculation
    - Test recommendation generation
    - _Requirements: 14.1, 14.2, 14.3, 14.4, 7.1_

- [ ] 15. Create profiling data models
  - Create `app/core/profiler/models.py` with dataclasses
  - Define ProfileResult dataclass with to_json() method
  - Define ColumnProfile dataclass
  - Define QualityMetrics dataclass
  - Define GoalInsight dataclass
  - Define Recommendation dataclass
  - _Requirements: 16.1, 16.2, 19.1, 19.2, 19.3, 19.4, 19.5_

- [ ] 16. Implement AnalysisService for profiling orchestration
  - [ ] 16.1 Create AnalysisService class in `app/services/analysis_service.py`
    - Implement `start_analysis()` method to create analysis record and queue job
    - Implement `get_analysis_status()` method
    - Implement `get_analysis_results()` method
    - Implement `_store_results()` to save ProfileResult to database
    - Add error handling for profiling failures
    - _Requirements: 15.1, 15.2, 15.3, 15.4, 15.5, 16.1, 16.2, 16.3, 16.4_
  
  - [ ]* 16.2 Write unit tests for AnalysisService
    - Test analysis creation
    - Test status retrieval
    - Test results retrieval
    - Test result storage
    - Test error handling
    - _Requirements: 15.1, 15.2, 15.3, 15.4_

- [ ] 17. Create Celery worker for background profiling
  - [ ] 17.1 Create Celery configuration in `app/core/celery_app.py`
    - Configure Celery with Redis broker
    - Set task timeout to 5 minutes
    - Configure result backend
    - Add task routing
    - _Requirements: 15.1, 15.2, 15.3, 15.4, 15.5, 17.1, 17.2, 17.3_
  
  - [ ] 17.2 Create profiling worker in `app/workers/profiling_worker.py`
    - Implement `run_profiling_task()` Celery task
    - Load dataset from database
    - Initialize ProfilerEngine
    - Run profiling with goal type
    - Store results in database
    - Update analysis status
    - Handle errors and timeouts
    - _Requirements: 15.1, 15.2, 15.3, 15.4, 15.5, 17.1, 17.2, 17.3, 18.1, 18.2, 18.3, 18.4, 18.5_

- [ ] 18. Create analysis API endpoints
  - [ ] 18.1 Create analysis router in `app/api/v1/analysis.py`
    - Implement POST `/api/v1/analysis/start` endpoint
    - Implement GET `/api/v1/analysis/{id}/status` endpoint
    - Implement GET `/api/v1/analysis/{id}/results` endpoint
    - Add request validation with Pydantic schemas
    - Add access control verification
    - Add OpenAPI documentation
    - _Requirements: 15.1, 15.2, 15.3, 19.1, 19.2, 19.3, 19.4, 19.5_
  
  - [ ]* 18.2 Write integration tests for analysis endpoints
    - Test start analysis endpoint
    - Test status endpoint
    - Test results endpoint
    - Test access control
    - Test with different goal types
    - _Requirements: 15.1, 15.2, 15.3_

- [ ] 19. Create analysis Pydantic schemas
  - Create `app/schemas/analysis.py` with analysis schemas
  - Implement AnalysisStartRequest with dataset_id and goal_type
  - Implement AnalysisStatusResponse with status and progress
  - Implement AnalysisResultsResponse with complete profiling results
  - Add validation for goal_type enum
  - _Requirements: 19.1, 19.2, 19.3, 19.4, 19.5_

- [ ] 20. Add custom exceptions for profiling
  - Add ProfilingException to `app/core/exceptions.py`
  - Add TimeoutException for profiling timeouts
  - Update exception handler in `app/main.py`
  - _Requirements: 18.1, 18.2, 18.3, 18.4, 18.5_

- [ ] 21. Register analysis router in main application
  - Import analysis router in `app/api/v1/__init__.py`
  - Register in `app/main.py` with `/api/v1` prefix
  - _Requirements: 15.1_

- [ ] 22. Update requirements.txt with profiling dependencies
  - Add scipy==1.11.0 for statistical calculations
  - Add celery==5.3.0 for background jobs
  - Add redis==5.0.0 for Celery broker
  - Verify numpy and pandas versions
  - _Requirements: 17.1, 17.2, 17.3_

- [ ] 23. Create Redis configuration for Celery
  - Add Redis service to `docker-compose.yml`
  - Configure Redis connection in `app/config.py`
  - Add CELERY_BROKER_URL and CELERY_RESULT_BACKEND to `.env.example`
  - _Requirements: 15.1, 15.2_

- [ ]* 24. Create performance benchmarking tests
  - Create `tests/test_performance/test_profiler_performance.py`
  - Test 100MB file profiling time (<30 seconds)
  - Test 1GB file profiling time (<5 minutes)
  - Test memory usage (<2GB)
  - Test concurrent profiling
  - _Requirements: 17.1, 17.2, 17.3, 17.4, 17.5_

- [ ]* 25. Write integration tests for complete profiling workflow
  - Create `tests/test_integration/test_profiling_workflow.py`
  - Test upload → start analysis → check status → get results flow
  - Test with different file types (CSV, Excel, JSON)
  - Test with different goal types
  - Test error scenarios
  - Test timeout handling
  - _Requirements: 15.1, 15.2, 15.3, 15.4, 15.5, 18.1, 18.2, 18.3, 18.4, 18.5_

- [ ] 26. Create profiling documentation
  - Document profiling algorithms in `docs/PROFILING.md`
  - Explain statistical methods used
  - Document goal-based analysis logic
  - Add examples of profiling results
  - Document performance characteristics
  - _Requirements: 1.1, 2.1, 3.1, 4.1, 5.1, 6.1, 7.1, 8.1, 9.1, 10.1, 11.1, 12.1, 13.1_

- [ ] 27. Add logging for profiling operations
  - Add structured logging to ProfilerEngine
  - Log profiling start and completion
  - Log performance metrics (time, memory)
  - Log errors and warnings
  - Log goal-specific insights
  - _Requirements: 18.1, 18.2, 18.3, 18.4, 18.5_

- [ ] 28. Create profiling progress tracking
  - Implement progress updates during chunked processing
  - Store progress percentage in analysis record
  - Add progress field to status endpoint response
  - Update progress in real-time during profiling
  - _Requirements: 14.4, 15.2_
