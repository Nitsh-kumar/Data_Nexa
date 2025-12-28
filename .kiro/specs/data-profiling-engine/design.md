# Design Document

## Overview

This design document outlines the implementation of the Core Data Profiling Engine for DataInsight Pro Backend. The profiling engine analyzes datasets to generate comprehensive reports including statistical analysis, data quality metrics, pattern detection, and goal-based recommendations. The engine uses Pandas for data manipulation, NumPy for calculations, and supports chunked processing for large files with background job execution via Celery.

## Architecture

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Analysis Workflow                         │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
                    ┌──────────────────┐
                    │  API Endpoint    │
                    │  POST /analysis  │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │ AnalysisService  │
                    │ - Create record  │
                    │ - Queue job      │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │  Celery Worker   │
                    │  (Background)    │
                    └────────┬─────────┘
                             │
                             ▼
            ┌────────────────────────────────┐
            │     ProfilerEngine             │
            │  ┌──────────────────────────┐  │
            │  │  1. Load Data            │  │
            │  │     - Chunked reading    │  │
            │  │     - Type inference     │  │
            │  └──────────────────────────┘  │
            │  ┌──────────────────────────┐  │
            │  │  2. Column Analysis      │  │
            │  │     - Type detection     │  │
            │  │     - Statistics         │  │
            │  │     - Null analysis      │  │
            │  └──────────────────────────┘  │
            │  ┌──────────────────────────┐  │
            │  │  3. Quality Checks       │  │
            │  │     - Duplicates         │  │
            │  │     - Outliers           │  │
            │  │     - Correlations       │  │
            │  └──────────────────────────┘  │
            │  ┌──────────────────────────┐  │
            │  │  4. Goal-Based Analysis  │  │
            │  │     - ML checks          │  │
            │  │     - Business checks    │  │
            │  │     - Anomaly checks     │  │
            │  └──────────────────────────┘  │
            │  ┌──────────────────────────┐  │
            │  │  5. Generate Report      │  │
            │  │     - Quality score      │  │
            │  │     - Recommendations    │  │
            │  │     - JSON output        │  │
            │  └──────────────────────────┘  │
            └────────────────────────────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │   PostgreSQL     │
                    │  Store results   │
                    └──────────────────┘
```

### Component Architecture

```
app/core/profiler/
├── __init__.py
├── base_profiler.py          # Main profiling orchestrator
├── column_analyzer.py        # Column-level analysis
├── type_detector.py          # Data type detection
├── statistics_calculator.py  # Statistical calculations
├── quality_scorer.py         # Quality score calculation
├── pattern_detector.py       # Pattern detection
├── null_analyzer.py          # Missing data analysis
├── outlier_detector.py       # Outlier detection
├── correlation_analyzer.py   # Correlation analysis
└── goal_analyzers/
    ├── ml_analyzer.py        # ML-specific checks
    ├── business_analyzer.py  # Business-specific checks
    └── anomaly_analyzer.py   # Anomaly-specific checks
```

## Components and Interfaces

### 1. ProfilerEngine (Base Profiler)

**Purpose:** Orchestrate the entire profiling workflow.

**Interface:**

```python
class ProfilerEngine:
    """Main profiling engine that coordinates all analysis components."""
    
    def __init__(
        self,
        column_analyzer: ColumnAnalyzer,
        quality_scorer: QualityScorer,
        goal_analyzer_factory: GoalAnalyzerFactory,
    ):
        self.column_analyzer = column_analyzer
        self.quality_scorer = quality_scorer
        self.goal_analyzer_factory = goal_analyzer_factory
    
    async def profile_dataset(
        self,
        dataset_id: int,
        goal_type: AnalysisGoalType,
        chunk_size: int = 10000,
    ) -> ProfileResult:
        """Profile a dataset and generate comprehensive report.
        
        Args:
            dataset_id: ID of dataset to profile
            goal_type: Analysis goal (ML, business, anomaly)
            chunk_size: Number of rows per chunk for large files
            
        Returns:
            Complete profiling results
            
        Raises:
            ProfilingException: If profiling fails
        """
        try:
            # Load dataset metadata
            dataset = await self._load_dataset(dataset_id)
            
            # Load data with chunking for large files
            df = await self._load_data(dataset, chunk_size)
            
            # Analyze each column
            column_profiles = await self._analyze_columns(df)
            
            # Perform quality checks
            quality_metrics = await self._check_quality(df, column_profiles)
            
            # Run goal-specific analysis
            goal_analyzer = self.goal_analyzer_factory.create(goal_type)
            goal_insights = await goal_analyzer.analyze(df, column_profiles)
            
            # Calculate overall quality score
            quality_score = self.quality_scorer.calculate(quality_metrics)
            
            # Generate recommendations
            recommendations = await self._generate_recommendations(
                column_profiles,
                quality_metrics,
                goal_insights,
            )
            
            # Build result
            result = ProfileResult(
                dataset_id=dataset_id,
                row_count=len(df),
                column_count=len(df.columns),
                quality_score=quality_score,
                column_profiles=column_profiles,
                quality_metrics=quality_metrics,
                goal_insights=goal_insights,
                recommendations=recommendations,
            )
            
            return result
            
        except Exception as e:
            raise ProfilingException(f"Profiling failed: {str(e)}")
    
    async def _load_data(
        self,
        dataset: Dataset,
        chunk_size: int,
    ) -> pd.DataFrame:
        """Load dataset from storage with chunking support."""
        file_path = dataset.file_path
        file_ext = Path(dataset.name).suffix.lower()
        
        # Download from S3
        file_content = await self.storage.download_file(file_path)
        
        # Load based on file type
        if file_ext == ".csv":
            # Use chunking for large CSV files
            if dataset.file_size > 100 * 1024 * 1024:  # 100MB
                return await self._load_csv_chunked(file_content, chunk_size)
            else:
                return pd.read_csv(io.BytesIO(file_content))
        
        elif file_ext in {".xlsx", ".xls"}:
            return pd.read_excel(io.BytesIO(file_content), sheet_name=0)
        
        elif file_ext == ".json":
            data = json.loads(file_content.decode("utf-8"))
            if isinstance(data, list):
                return pd.DataFrame(data)
            else:
                return pd.DataFrame([data])
        
        else:
            raise ProfilingException(f"Unsupported file type: {file_ext}")
    
    async def _load_csv_chunked(
        self,
        file_content: bytes,
        chunk_size: int,
    ) -> pd.DataFrame:
        """Load large CSV in chunks and aggregate."""
        chunks = []
        reader = pd.read_csv(
            io.BytesIO(file_content),
            chunksize=chunk_size,
        )
        
        for chunk in reader:
            chunks.append(chunk)
            
            # Memory check
            if len(chunks) * chunk_size > 1_000_000:  # 1M rows
                break
        
        return pd.concat(chunks, ignore_index=True)
    
    async def _analyze_columns(
        self,
        df: pd.DataFrame,
    ) -> list[ColumnProfile]:
        """Analyze each column in the dataset."""
        profiles = []
        
        for column in df.columns:
            profile = await self.column_analyzer.analyze(df[column])
            profiles.append(profile)
        
        return profiles
    
    async def _check_quality(
        self,
        df: pd.DataFrame,
        column_profiles: list[ColumnProfile],
    ) -> QualityMetrics:
        """Perform dataset-level quality checks."""
        return QualityMetrics(
            duplicate_count=df.duplicated().sum(),
            duplicate_percentage=df.duplicated().sum() / len(df) * 100,
            total_null_count=df.isnull().sum().sum(),
            total_null_percentage=df.isnull().sum().sum() / df.size * 100,
            outlier_count=sum(p.outlier_count for p in column_profiles),
            correlation_matrix=self._calculate_correlations(df),
        )
    
    def _calculate_correlations(
        self,
        df: pd.DataFrame,
    ) -> dict[str, dict[str, float]]:
        """Calculate correlation matrix for numeric columns."""
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        
        if len(numeric_cols) < 2:
            return {}
        
        corr_matrix = df[numeric_cols].corr()
        
        # Convert to dict and find high correlations
        result = {}
        for col1 in numeric_cols:
            result[col1] = {}
            for col2 in numeric_cols:
                if col1 != col2:
                    corr_value = corr_matrix.loc[col1, col2]
                    if abs(corr_value) > 0.8:
                        result[col1][col2] = round(corr_value, 2)
        
        return result
    
    async def _generate_recommendations(
        self,
        column_profiles: list[ColumnProfile],
        quality_metrics: QualityMetrics,
        goal_insights: list[GoalInsight],
    ) -> list[Recommendation]:
        """Generate actionable recommendations."""
        recommendations = []
        
        # High null percentage
        for profile in column_profiles:
            if profile.null_percentage > 50:
                recommendations.append(Recommendation(
                    severity="critical",
                    type="missing_data",
                    description=f"Column '{profile.column_name}' has {profile.null_percentage:.1f}% missing values",
                    recommendation="Consider dropping this column or investigating why data is missing",
                    affected_columns=[profile.column_name],
                ))
        
        # Duplicates
        if quality_metrics.duplicate_percentage > 5:
            recommendations.append(Recommendation(
                severity="high",
                type="duplicates",
                description=f"Dataset contains {quality_metrics.duplicate_percentage:.1f}% duplicate rows",
                recommendation="Remove duplicate rows using df.drop_duplicates()",
                affected_columns=[],
            ))
        
        # High correlation
        for col1, correlations in quality_metrics.correlation_matrix.items():
            for col2, corr_value in correlations.items():
                if abs(corr_value) > 0.9:
                    recommendations.append(Recommendation(
                        severity="medium",
                        type="quality_issue",
                        description=f"High correlation ({corr_value}) between '{col1}' and '{col2}'",
                        recommendation="Consider removing one of these features to reduce multicollinearity",
                        affected_columns=[col1, col2],
                    ))
        
        # Add goal-specific recommendations
        for insight in goal_insights:
            if insight.severity in {"critical", "high"}:
                recommendations.append(Recommendation(
                    severity=insight.severity,
                    type=insight.type,
                    description=insight.description,
                    recommendation=insight.recommendation,
                    affected_columns=insight.affected_columns,
                ))
        
        # Sort by severity
        severity_order = {"critical": 0, "high": 1, "medium": 2, "low": 3}
        recommendations.sort(key=lambda r: severity_order[r.severity])
        
        return recommendations
```

### 2. ColumnAnalyzer

**Purpose:** Analyze individual columns for type, statistics, and patterns.

**Interface:**

```python
class ColumnAnalyzer:
    """Analyze individual columns."""
    
    def __init__(
        self,
        type_detector: TypeDetector,
        statistics_calculator: StatisticsCalculator,
        null_analyzer: NullAnalyzer,
        outlier_detector: OutlierDetector,
        pattern_detector: PatternDetector,
    ):
        self.type_detector = type_detector
        self.statistics_calculator = statistics_calculator
        self.null_analyzer = null_analyzer
        self.outlier_detector = outlier_detector
        self.pattern_detector = pattern_detector
    
    async def analyze(self, series: pd.Series) -> ColumnProfile:
        """Analyze a single column.
        
        Args:
            series: Pandas series to analyze
            
        Returns:
            Column profile with all statistics
        """
        # Detect type
        data_type, semantic_type = self.type_detector.detect(series)
        
        # Calculate statistics based on type
        if data_type == "numeric":
            stats = self.statistics_calculator.calculate_numeric(series)
            outliers = self.outlier_detector.detect(series)
        elif data_type == "categorical":
            stats = self.statistics_calculator.calculate_categorical(series)
            outliers = []
        elif data_type == "datetime":
            stats = self.statistics_calculator.calculate_datetime(series)
            outliers = []
        elif data_type == "text":
            stats = self.statistics_calculator.calculate_text(series)
            outliers = []
        else:
            stats = {}
            outliers = []
        
        # Analyze nulls
        null_info = self.null_analyzer.analyze(series)
        
        # Detect patterns
        patterns = self.pattern_detector.detect(series)
        
        return ColumnProfile(
            column_name=series.name,
            data_type=data_type,
            semantic_type=semantic_type,
            null_count=null_info.count,
            null_percentage=null_info.percentage,
            unique_count=series.nunique(),
            statistics=stats,
            outliers=outliers,
            patterns=patterns,
        )
```

### 3. TypeDetector

**Purpose:** Detect basic and semantic data types.

**Interface:**

```python
class TypeDetector:
    """Detect column data types."""
    
    def detect(self, series: pd.Series) -> tuple[str, str | None]:
        """Detect basic and semantic types.
        
        Args:
            series: Column to analyze
            
        Returns:
            Tuple of (basic_type, semantic_type)
        """
        # Remove nulls for type detection
        non_null = series.dropna()
        
        if len(non_null) == 0:
            return "unknown", None
        
        # Detect basic type
        if pd.api.types.is_numeric_dtype(series):
            basic_type = "numeric"
        elif pd.api.types.is_datetime64_any_dtype(series):
            basic_type = "datetime"
        elif pd.api.types.is_bool_dtype(series):
            basic_type = "boolean"
        elif series.nunique() / len(series) < 0.5:
            basic_type = "categorical"
        else:
            basic_type = "text"
        
        # Detect semantic type for text columns
        semantic_type = None
        if basic_type == "text":
            semantic_type = self._detect_semantic_type(non_null)
        
        return basic_type, semantic_type
    
    def _detect_semantic_type(self, series: pd.Series) -> str | None:
        """Detect semantic type for text columns."""
        sample = series.head(100).astype(str)
        
        # Email pattern
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if sample.str.match(email_pattern).mean() > 0.8:
            return "email"
        
        # Phone pattern
        phone_pattern = r'^\+?1?\d{9,15}$'
        if sample.str.match(phone_pattern).mean() > 0.8:
            return "phone"
        
        # URL pattern
        url_pattern = r'^https?://[^\s]+$'
        if sample.str.match(url_pattern).mean() > 0.8:
            return "url"
        
        # Check if all unique (potential ID)
        if series.nunique() == len(series):
            return "identifier"
        
        return None
```

### 4. StatisticsCalculator

**Purpose:** Calculate type-specific statistics.

**Interface:**

```python
class StatisticsCalculator:
    """Calculate statistics for different data types."""
    
    def calculate_numeric(self, series: pd.Series) -> dict[str, Any]:
        """Calculate statistics for numeric columns."""
        return {
            "min": float(series.min()),
            "max": float(series.max()),
            "mean": float(series.mean()),
            "median": float(series.median()),
            "std_dev": float(series.std()),
            "q1": float(series.quantile(0.25)),
            "q2": float(series.quantile(0.50)),
            "q3": float(series.quantile(0.75)),
            "iqr": float(series.quantile(0.75) - series.quantile(0.25)),
            "skewness": float(series.skew()),
            "kurtosis": float(series.kurtosis()),
            "histogram": self._calculate_histogram(series),
        }
    
    def calculate_categorical(self, series: pd.Series) -> dict[str, Any]:
        """Calculate statistics for categorical columns."""
        value_counts = series.value_counts()
        
        return {
            "unique_count": int(series.nunique()),
            "mode": str(series.mode()[0]) if len(series.mode()) > 0 else None,
            "top_values": [
                {"value": str(val), "count": int(count), "percentage": round(count / len(series) * 100, 2)}
                for val, count in value_counts.head(20).items()
            ],
            "cardinality": "high" if series.nunique() / len(series) > 0.5 else "low",
        }
    
    def calculate_datetime(self, series: pd.Series) -> dict[str, Any]:
        """Calculate statistics for datetime columns."""
        return {
            "min_date": str(series.min()),
            "max_date": str(series.max()),
            "date_range_days": (series.max() - series.min()).days,
            "frequency": self._detect_frequency(series),
        }
    
    def calculate_text(self, series: pd.Series) -> dict[str, Any]:
        """Calculate statistics for text columns."""
        lengths = series.astype(str).str.len()
        
        return {
            "min_length": int(lengths.min()),
            "max_length": int(lengths.max()),
            "avg_length": round(lengths.mean(), 2),
            "common_patterns": self._find_common_patterns(series),
        }
    
    def _calculate_histogram(self, series: pd.Series, bins: int = 10) -> list[dict]:
        """Calculate histogram data."""
        counts, bin_edges = np.histogram(series.dropna(), bins=bins)
        
        histogram = []
        for i in range(len(counts)):
            histogram.append({
                "bin_start": round(float(bin_edges[i]), 2),
                "bin_end": round(float(bin_edges[i + 1]), 2),
                "count": int(counts[i]),
            })
        
        return histogram
    
    def _detect_frequency(self, series: pd.Series) -> str:
        """Detect time series frequency."""
        if len(series) < 2:
            return "unknown"
        
        diffs = series.sort_values().diff().dropna()
        median_diff = diffs.median()
        
        if median_diff.days == 1:
            return "daily"
        elif 6 <= median_diff.days <= 8:
            return "weekly"
        elif 28 <= median_diff.days <= 31:
            return "monthly"
        else:
            return "irregular"
    
    def _find_common_patterns(self, series: pd.Series) -> list[str]:
        """Find common text patterns."""
        # Sample for performance
        sample = series.head(1000).astype(str)
        
        patterns = []
        
        # Check for common formats
        if sample.str.match(r'^\d{3}-\d{3}-\d{4}$').mean() > 0.5:
            patterns.append("XXX-XXX-XXXX")
        
        if sample.str.match(r'^\d{5}$').mean() > 0.5:
            patterns.append("XXXXX (ZIP code)")
        
        return patterns
```

### 5. OutlierDetector

**Purpose:** Detect outliers in numeric columns.

**Interface:**

```python
class OutlierDetector:
    """Detect outliers using IQR and Z-score methods."""
    
    def detect(self, series: pd.Series) -> list[dict]:
        """Detect outliers in numeric series.
        
        Args:
            series: Numeric series to analyze
            
        Returns:
            List of outlier information
        """
        if not pd.api.types.is_numeric_dtype(series):
            return []
        
        # IQR method
        q1 = series.quantile(0.25)
        q3 = series.quantile(0.75)
        iqr = q3 - q1
        
        lower_bound = q1 - 1.5 * iqr
        upper_bound = q3 + 1.5 * iqr
        
        outliers_iqr = series[(series < lower_bound) | (series > upper_bound)]
        
        # Z-score method
        z_scores = np.abs((series - series.mean()) / series.std())
        outliers_zscore = series[z_scores > 3]
        
        # Combine results
        outlier_values = set(outliers_iqr.values) | set(outliers_zscore.values)
        
        return {
            "count": len(outlier_values),
            "percentage": round(len(outlier_values) / len(series) * 100, 2),
            "method": "IQR and Z-score",
            "bounds": {
                "lower": round(float(lower_bound), 2),
                "upper": round(float(upper_bound), 2),
            },
            "sample_values": [round(float(v), 2) for v in list(outlier_values)[:10]],
        }
```

### 6. QualityScorer

**Purpose:** Calculate overall data quality score.

**Interface:**

```python
class QualityScorer:
    """Calculate overall data quality score."""
    
    def calculate(self, quality_metrics: QualityMetrics) -> float:
        """Calculate quality score (0-100).
        
        Args:
            quality_metrics: Quality metrics from analysis
            
        Returns:
            Quality score between 0 and 100
        """
        score = 100.0
        
        # Deduct for nulls (max -30 points)
        null_penalty = min(quality_metrics.total_null_percentage * 0.5, 30)
        score -= null_penalty
        
        # Deduct for duplicates (max -20 points)
        duplicate_penalty = min(quality_metrics.duplicate_percentage * 2, 20)
        score -= duplicate_penalty
        
        # Deduct for outliers (max -15 points)
        outlier_penalty = min(quality_metrics.outlier_count / 100 * 15, 15)
        score -= outlier_penalty
        
        # Ensure score is between 0 and 100
        return max(0.0, min(100.0, round(score, 2)))
```

### 7. Goal Analyzers

**Purpose:** Perform goal-specific analysis.

**ML Analyzer Interface:**

```python
class MLAnalyzer:
    """ML-specific analysis."""
    
    async def analyze(
        self,
        df: pd.DataFrame,
        column_profiles: list[ColumnProfile],
    ) -> list[GoalInsight]:
        """Perform ML-specific checks."""
        insights = []
        
        # Check for high cardinality
        for profile in column_profiles:
            if profile.data_type == "categorical" and profile.unique_count > 100:
                insights.append(GoalInsight(
                    severity="high",
                    type="quality_issue",
                    description=f"Column '{profile.column_name}' has high cardinality ({profile.unique_count} unique values)",
                    recommendation="Consider encoding or grouping rare categories",
                    affected_columns=[profile.column_name],
                ))
        
        # Check for constant features
        for profile in column_profiles:
            if profile.unique_count == 1:
                insights.append(GoalInsight(
                    severity="medium",
                    type="quality_issue",
                    description=f"Column '{profile.column_name}' has constant value",
                    recommendation="Remove this feature as it provides no information",
                    affected_columns=[profile.column_name],
                ))
        
        return insights
```

## Data Models

### ProfileResult

```python
@dataclass
class ProfileResult:
    """Complete profiling result."""
    dataset_id: int
    row_count: int
    column_count: int
    quality_score: float
    column_profiles: list[ColumnProfile]
    quality_metrics: QualityMetrics
    goal_insights: list[GoalInsight]
    recommendations: list[Recommendation]
    
    def to_json(self) -> dict[str, Any]:
        """Convert to JSON-serializable dict."""
        return {
            "dataset_id": self.dataset_id,
            "summary": {
                "row_count": self.row_count,
                "column_count": self.column_count,
                "quality_score": self.quality_score,
            },
            "columns": [asdict(p) for p in self.column_profiles],
            "quality": asdict(self.quality_metrics),
            "insights": [asdict(i) for i in self.goal_insights],
            "recommendations": [asdict(r) for r in self.recommendations],
        }
```

### ColumnProfile

```python
@dataclass
class ColumnProfile:
    """Column-level profile."""
    column_name: str
    data_type: str
    semantic_type: str | None
    null_count: int
    null_percentage: float
    unique_count: int
    statistics: dict[str, Any]
    outliers: dict[str, Any]
    patterns: list[str]
```

## Error Handling

```python
class ProfilingException(AppException):
    """Profiling operation failed."""
    def __init__(self, detail: str):
        super().__init__(status_code=500, detail=detail, error_code="PROFILING_ERROR")
```

## Testing Strategy

### Unit Tests
- Test each analyzer component independently
- Mock data with known characteristics
- Verify statistical calculations
- Test edge cases (empty columns, all nulls, etc.)

### Integration Tests
- Test complete profiling workflow
- Test chunked processing
- Test goal-specific analysis
- Test performance with large datasets

## Performance Considerations

1. **Chunked Processing**: Process large files in 10K row chunks
2. **Sampling**: For very large files, sample for pattern detection
3. **Parallel Processing**: Analyze columns in parallel
4. **Caching**: Cache intermediate results
5. **Memory Management**: Monitor and limit memory usage

## Dependencies

```
pandas==2.2.0
numpy==1.26.0
scipy==1.11.0
celery==5.3.0
redis==5.0.0
```

This design provides a comprehensive, modular profiling engine that can analyze datasets efficiently and generate actionable insights.
