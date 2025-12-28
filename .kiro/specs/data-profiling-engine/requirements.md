# Requirements Document

## Introduction

This spec defines the Core Data Profiling Engine for DataInsight Pro Backend. The profiling engine analyzes uploaded datasets to generate comprehensive reports including column type detection, statistical analysis, data quality metrics, and pattern detection. The engine supports goal-based analysis tailored to different use cases (ML preparation, business reporting, anomaly detection) and processes large files efficiently using chunked streaming.

## Requirements

### Requirement 1: Column Type Detection

**User Story:** As a user, I want the system to automatically detect column data types, so that I can understand my data structure without manual inspection.

#### Acceptance Criteria

1. WHEN a column is analyzed THEN the system SHALL detect basic types: numeric, categorical, datetime, text, boolean
2. WHEN a column contains mixed types THEN the system SHALL identify the predominant type and flag inconsistencies
3. WHEN analyzing text columns THEN the system SHALL detect semantic types: email, phone, URL, PII (names, addresses)
4. WHEN a column type is ambiguous THEN the system SHALL provide confidence score for the detected type
5. IF a column contains all unique values THEN the system SHALL flag it as a potential identifier

### Requirement 2: Statistical Analysis for Numeric Columns

**User Story:** As a data analyst, I want detailed statistics for numeric columns, so that I can understand distributions and ranges.

#### Acceptance Criteria

1. WHEN a numeric column is analyzed THEN the system SHALL calculate min, max, mean, median, and standard deviation
2. WHEN a numeric column is analyzed THEN the system SHALL calculate quartiles (Q1, Q2, Q3) and IQR
3. WHEN a numeric column is analyzed THEN the system SHALL generate histogram data with 10 bins
4. WHEN a numeric column is analyzed THEN the system SHALL detect skewness and kurtosis
5. IF a numeric column has outliers THEN the system SHALL identify them using IQR method (values < Q1-1.5*IQR or > Q3+1.5*IQR)

### Requirement 3: Statistical Analysis for Categorical Columns

**User Story:** As a user, I want to understand categorical data distributions, so that I can identify dominant categories and rare values.

#### Acceptance Criteria

1. WHEN a categorical column is analyzed THEN the system SHALL count unique values
2. WHEN a categorical column is analyzed THEN the system SHALL identify the mode (most frequent value)
3. WHEN a categorical column is analyzed THEN the system SHALL generate frequency distribution for top 20 values
4. WHEN a categorical column has high cardinality THEN the system SHALL flag it (>50% unique values)
5. IF a categorical column has very low cardinality THEN the system SHALL suggest converting to boolean (<5 unique values)

### Requirement 4: Statistical Analysis for Datetime Columns

**User Story:** As a user, I want to analyze temporal patterns in datetime columns, so that I can understand time-based trends.

#### Acceptance Criteria

1. WHEN a datetime column is analyzed THEN the system SHALL calculate min date, max date, and date range
2. WHEN a datetime column is analyzed THEN the system SHALL detect frequency patterns (daily, weekly, monthly)
3. WHEN a datetime column is analyzed THEN the system SHALL identify gaps in time series
4. WHEN a datetime column is analyzed THEN the system SHALL detect seasonality patterns
5. IF datetime values are in the future THEN the system SHALL flag them as potential data quality issues

### Requirement 5: Statistical Analysis for Text Columns

**User Story:** As a user, I want to understand text data characteristics, so that I can identify patterns and anomalies.

#### Acceptance Criteria

1. WHEN a text column is analyzed THEN the system SHALL calculate min, max, and average text length
2. WHEN a text column is analyzed THEN the system SHALL detect common patterns using regex
3. WHEN a text column is analyzed THEN the system SHALL identify most frequent words (excluding stop words)
4. WHEN a text column contains structured data THEN the system SHALL detect format patterns (e.g., "XXX-XXX-XXXX" for phone)
5. IF text length varies significantly THEN the system SHALL flag inconsistent formatting

### Requirement 6: Null Value Analysis

**User Story:** As a data scientist, I want to understand missing data patterns, so that I can choose appropriate imputation strategies.

#### Acceptance Criteria

1. WHEN a column is analyzed THEN the system SHALL calculate null count and null percentage
2. WHEN analyzing nulls THEN the system SHALL classify pattern as MCAR (Missing Completely At Random), MAR (Missing At Random), or MNAR (Missing Not At Random)
3. WHEN multiple columns have nulls THEN the system SHALL detect correlation between missing values
4. WHEN null percentage exceeds 50% THEN the system SHALL flag the column as high-risk
5. IF nulls follow a pattern THEN the system SHALL provide insights on the pattern

### Requirement 7: Duplicate Detection

**User Story:** As a user, I want to identify duplicate rows, so that I can clean my data before analysis.

#### Acceptance Criteria

1. WHEN a dataset is analyzed THEN the system SHALL detect exact duplicate rows
2. WHEN duplicates are found THEN the system SHALL report count and percentage
3. WHEN analyzing duplicates THEN the system SHALL identify which columns contribute to duplicates
4. WHEN a primary key column is specified THEN the system SHALL check for duplicate keys
5. IF duplicates exceed 5% THEN the system SHALL flag as a data quality issue

### Requirement 8: Outlier Detection

**User Story:** As a data analyst, I want to identify outliers in numeric columns, so that I can investigate anomalies.

#### Acceptance Criteria

1. WHEN a numeric column is analyzed THEN the system SHALL detect outliers using IQR method
2. WHEN outliers are detected THEN the system SHALL report count, percentage, and specific values
3. WHEN analyzing outliers THEN the system SHALL use Z-score method as alternative (|z| > 3)
4. WHEN outliers are found THEN the system SHALL visualize them in distribution data
5. IF outliers exceed 10% THEN the system SHALL suggest reviewing data collection process

### Requirement 9: Correlation Analysis

**User Story:** As a data scientist, I want to understand relationships between numeric columns, so that I can identify multicollinearity and feature dependencies.

#### Acceptance Criteria

1. WHEN multiple numeric columns exist THEN the system SHALL calculate Pearson correlation matrix
2. WHEN high correlation is detected THEN the system SHALL flag pairs with |r| > 0.8
3. WHEN analyzing correlations THEN the system SHALL identify potential feature redundancy
4. WHEN goal is ML preparation THEN the system SHALL warn about multicollinearity
5. IF perfect correlation exists THEN the system SHALL suggest removing duplicate features

### Requirement 10: Overall Data Quality Score

**User Story:** As a user, I want a single quality score, so that I can quickly assess dataset health.

#### Acceptance Criteria

1. WHEN analysis completes THEN the system SHALL calculate overall quality score (0-100)
2. WHEN calculating quality score THEN the system SHALL consider null percentage, duplicate percentage, outlier percentage, and type consistency
3. WHEN quality score is below 70 THEN the system SHALL flag as "needs improvement"
4. WHEN quality score is 70-85 THEN the system SHALL flag as "acceptable"
5. WHEN quality score is above 85 THEN the system SHALL flag as "good"

### Requirement 11: Goal-Based Analysis for ML Preparation

**User Story:** As a machine learning engineer, I want ML-specific checks, so that I can prepare data for modeling.

#### Acceptance Criteria

1. WHEN goal is ML preparation THEN the system SHALL check for data leakage (target in features)
2. WHEN goal is ML preparation THEN the system SHALL detect high cardinality categorical features (>100 unique)
3. WHEN goal is ML preparation THEN the system SHALL check for class imbalance in target variable
4. WHEN goal is ML preparation THEN the system SHALL identify constant or near-constant features
5. IF issues are found THEN the system SHALL provide specific ML recommendations

### Requirement 12: Goal-Based Analysis for Business Reporting

**User Story:** As a business analyst, I want business-specific checks, so that I can ensure data consistency for reporting.

#### Acceptance Criteria

1. WHEN goal is business reporting THEN the system SHALL check for standard date formats
2. WHEN goal is business reporting THEN the system SHALL verify categorical values match expected lists
3. WHEN goal is business reporting THEN the system SHALL check for negative values in amount fields
4. WHEN goal is business reporting THEN the system SHALL detect inconsistent naming conventions
5. IF issues are found THEN the system SHALL provide business-focused recommendations

### Requirement 13: Goal-Based Analysis for Anomaly Detection

**User Story:** As a data engineer, I want anomaly-specific checks, so that I can identify unusual patterns.

#### Acceptance Criteria

1. WHEN goal is anomaly detection THEN the system SHALL flag unusual distributions (high skewness)
2. WHEN goal is anomaly detection THEN the system SHALL detect sudden changes in time series
3. WHEN goal is anomaly detection THEN the system SHALL identify rare categorical values (<1% frequency)
4. WHEN goal is anomaly detection THEN the system SHALL detect unexpected value ranges
5. IF anomalies are found THEN the system SHALL provide context and severity

### Requirement 14: Chunked Processing for Large Files

**User Story:** As a system, I need to process large files efficiently, so that memory usage stays within limits.

#### Acceptance Criteria

1. WHEN a file exceeds 100MB THEN the system SHALL use chunked processing with 10,000 row chunks
2. WHEN processing chunks THEN the system SHALL aggregate statistics incrementally
3. WHEN processing chunks THEN the system SHALL maintain memory usage below 2GB
4. WHEN processing large files THEN the system SHALL provide progress updates
5. IF processing exceeds 5 minutes THEN the system SHALL timeout and return partial results

### Requirement 15: Background Job Execution

**User Story:** As a user, I want analysis to run in the background, so that I can continue working while data is processed.

#### Acceptance Criteria

1. WHEN analysis is triggered THEN the system SHALL queue a background job using Celery
2. WHEN job starts THEN the system SHALL update analysis status to "running"
3. WHEN job completes THEN the system SHALL update status to "completed" and store results
4. WHEN job fails THEN the system SHALL update status to "failed" and store error message
5. IF job is queued THEN the system SHALL provide estimated completion time

### Requirement 16: Analysis Results Storage

**User Story:** As a system, I need to store analysis results efficiently, so that they can be retrieved quickly.

#### Acceptance Criteria

1. WHEN analysis completes THEN the system SHALL store results as JSON in the analysis table
2. WHEN storing results THEN the system SHALL include overall summary, column profiles, and quality issues
3. WHEN storing results THEN the system SHALL compress large JSON objects
4. WHEN results are retrieved THEN the system SHALL decompress and parse JSON
5. IF results exceed 10MB THEN the system SHALL store in S3 and reference by URL

### Requirement 17: Performance Requirements

**User Story:** As a user, I want fast analysis, so that I can get insights quickly.

#### Acceptance Criteria

1. WHEN analyzing a 100MB file THEN the system SHALL complete in under 30 seconds
2. WHEN analyzing a 1GB file THEN the system SHALL complete in under 5 minutes
3. WHEN memory usage is measured THEN the system SHALL stay below 2GB per job
4. WHEN multiple analyses run THEN the system SHALL support concurrent processing
5. IF performance degrades THEN the system SHALL log metrics for optimization

### Requirement 18: Error Handling and Validation

**User Story:** As a system, I need robust error handling, so that failures are graceful and informative.

#### Acceptance Criteria

1. WHEN a file cannot be parsed THEN the system SHALL return specific error message
2. WHEN analysis fails mid-process THEN the system SHALL save partial results
3. WHEN invalid data types are encountered THEN the system SHALL skip and log the issue
4. WHEN timeout occurs THEN the system SHALL return results processed so far
5. IF critical error occurs THEN the system SHALL notify user and log for debugging

### Requirement 19: Profiling Results Output Format

**User Story:** As a frontend developer, I need consistent JSON output, so that I can display results predictably.

#### Acceptance Criteria

1. WHEN results are returned THEN the system SHALL use standardized JSON structure
2. WHEN results include statistics THEN the system SHALL round to 2 decimal places
3. WHEN results include distributions THEN the system SHALL limit to top 20 items
4. WHEN results include recommendations THEN the system SHALL prioritize by severity
5. IF results are empty THEN the system SHALL return empty arrays, not null

### Requirement 20: Recommendation Generation

**User Story:** As a user, I want actionable recommendations, so that I know how to improve data quality.

#### Acceptance Criteria

1. WHEN quality issues are detected THEN the system SHALL generate specific recommendations
2. WHEN recommendations are generated THEN the system SHALL include severity (critical, high, medium, low)
3. WHEN recommendations are generated THEN the system SHALL include affected columns
4. WHEN recommendations are generated THEN the system SHALL suggest specific actions
5. IF multiple issues exist THEN the system SHALL prioritize recommendations by impact
