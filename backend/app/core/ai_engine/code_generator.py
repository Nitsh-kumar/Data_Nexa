"""Code generator for creating Python and SQL snippets."""

import logging
from typing import Any

logger = logging.getLogger(__name__)


class CodeGenerator:
    """Generate code snippets for recommendations."""

    async def generate(
        self,
        insight: Any,
        language: str = "python",
    ) -> str | None:
        """Generate code snippet for insight.

        Args:
            insight: Insight with recommendation
            language: Target language (python, sql, r)

        Returns:
            Code snippet or None
        """
        logger.info(f"Generating {language} code for insight type: {insight.type}")

        if language == "python":
            return self._generate_python(insight)
        elif language == "sql":
            return self._generate_sql(insight)
        elif language == "r":
            return self._generate_r(insight)
        else:
            logger.warning(f"Unsupported language: {language}")
            return None

    def _generate_python(self, insight: Any) -> str | None:
        """Generate Python code snippet.

        Args:
            insight: Insight object

        Returns:
            Python code snippet
        """
        insight_type = insight.type
        affected_cols = insight.affected_columns

        if insight_type == "missing_data":
            if affected_cols:
                col = affected_cols[0]
                return f"""# Handle missing values in '{col}'
import pandas as pd

# Option 1: Remove rows with missing values
df = df.dropna(subset=['{col}'])

# Option 2: Fill with median (for numeric columns)
df['{col}'].fillna(df['{col}'].median(), inplace=True)

# Option 3: Fill with mode (for categorical columns)
df['{col}'].fillna(df['{col}'].mode()[0], inplace=True)

# Option 4: Forward fill
df['{col}'].fillna(method='ffill', inplace=True)"""
            else:
                return """# Handle missing values
import pandas as pd

# Remove all rows with any missing values
df = df.dropna()

# Or remove rows where all values are missing
df = df.dropna(how='all')

# Fill all numeric columns with median
numeric_cols = df.select_dtypes(include=['number']).columns
df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].median())"""

        elif insight_type == "duplicates":
            return """# Remove duplicate rows
import pandas as pd

# Remove all duplicate rows
df = df.drop_duplicates()

# Keep first occurrence
df = df.drop_duplicates(keep='first')

# Keep last occurrence
df = df.drop_duplicates(keep='last')

# Remove duplicates based on specific columns
# df = df.drop_duplicates(subset=['column1', 'column2'])"""

        elif insight_type == "outliers":
            if affected_cols:
                col = affected_cols[0]
                return f"""# Remove outliers from '{col}' using IQR method
import pandas as pd
import numpy as np

# Calculate IQR
Q1 = df['{col}'].quantile(0.25)
Q3 = df['{col}'].quantile(0.75)
IQR = Q3 - Q1

# Define outlier bounds
lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR

# Remove outliers
df = df[(df['{col}'] >= lower_bound) & (df['{col}'] <= upper_bound)]

# Or cap outliers instead of removing
df['{col}'] = df['{col}'].clip(lower=lower_bound, upper=upper_bound)"""
            else:
                return """# Remove outliers using Z-score method
import pandas as pd
import numpy as np

# Calculate Z-scores for numeric columns
numeric_cols = df.select_dtypes(include=['number']).columns
z_scores = np.abs((df[numeric_cols] - df[numeric_cols].mean()) / df[numeric_cols].std())

# Remove rows where any column has |z-score| > 3
df = df[(z_scores < 3).all(axis=1)]"""

        elif insight_type == "data_type_mismatch":
            if affected_cols:
                col = affected_cols[0]
                return f"""# Convert data type for '{col}'
import pandas as pd

# Convert to numeric (coerce errors to NaN)
df['{col}'] = pd.to_numeric(df['{col}'], errors='coerce')

# Convert to datetime
df['{col}'] = pd.to_datetime(df['{col}'], errors='coerce')

# Convert to string
df['{col}'] = df['{col}'].astype(str)

# Convert to category (for categorical data)
df['{col}'] = df['{col}'].astype('category')"""
            else:
                return """# Fix data type mismatches
import pandas as pd

# Infer and convert data types automatically
df = df.infer_objects()

# Convert specific columns
# df['numeric_col'] = pd.to_numeric(df['numeric_col'], errors='coerce')
# df['date_col'] = pd.to_datetime(df['date_col'], errors='coerce')"""

        elif insight_type == "pattern_violation":
            if affected_cols:
                col = affected_cols[0]
                return f"""# Standardize format for '{col}'
import pandas as pd
import re

# Remove special characters
df['{col}'] = df['{col}'].str.replace(r'[^a-zA-Z0-9\\s]', '', regex=True)

# Convert to lowercase
df['{col}'] = df['{col}'].str.lower()

# Trim whitespace
df['{col}'] = df['{col}'].str.strip()

# Apply custom pattern (example: phone numbers)
# df['{col}'] = df['{col}'].str.replace(r'(\\d{{3}})(\\d{{3}})(\\d{{4}})', r'\\1-\\2-\\3', regex=True)"""
            else:
                return """# Standardize text formatting
import pandas as pd

# Standardize all text columns
text_cols = df.select_dtypes(include=['object']).columns
for col in text_cols:
    df[col] = df[col].str.strip().str.lower()"""

        elif insight_type == "quality_issue":
            # Check if it's about high correlation
            if "correlation" in insight.description.lower():
                if affected_cols and len(affected_cols) >= 2:
                    col1, col2 = affected_cols[0], affected_cols[1]
                    return f"""# Handle high correlation between '{col1}' and '{col2}'
import pandas as pd

# Option 1: Remove one of the correlated features
df = df.drop(columns=['{col2}'])

# Option 2: Create a combined feature
df['{col1}_{col2}_combined'] = df['{col1}'] + df['{col2}']
df = df.drop(columns=['{col1}', '{col2}'])

# Option 3: Use PCA to reduce dimensionality
from sklearn.decomposition import PCA
pca = PCA(n_components=1)
df['{col1}_{col2}_pca'] = pca.fit_transform(df[['{col1}', '{col2}']])
df = df.drop(columns=['{col1}', '{col2}'])"""

            # Check if it's about high cardinality
            elif "cardinality" in insight.description.lower():
                if affected_cols:
                    col = affected_cols[0]
                    return f"""# Reduce high cardinality in '{col}'
import pandas as pd

# Option 1: Keep only top N categories
top_n = 10
top_categories = df['{col}'].value_counts().head(top_n).index
df['{col}'] = df['{col}'].apply(lambda x: x if x in top_categories else 'Other')

# Option 2: Group rare categories
min_frequency = 0.01  # 1%
value_counts = df['{col}'].value_counts(normalize=True)
rare_categories = value_counts[value_counts < min_frequency].index
df['{col}'] = df['{col}'].apply(lambda x: 'Other' if x in rare_categories else x)"""

        return None

    def _generate_sql(self, insight: Any) -> str | None:
        """Generate SQL code snippet.

        Args:
            insight: Insight object

        Returns:
            SQL code snippet
        """
        insight_type = insight.type
        affected_cols = insight.affected_columns

        if insight_type == "duplicates":
            return """-- Remove duplicate rows (PostgreSQL)
DELETE FROM table_name
WHERE ctid NOT IN (
    SELECT MIN(ctid)
    FROM table_name
    GROUP BY column1, column2, column3  -- specify all columns
);

-- Or using ROW_NUMBER (works in most databases)
WITH ranked AS (
    SELECT *,
           ROW_NUMBER() OVER (PARTITION BY column1, column2 ORDER BY id) AS rn
    FROM table_name
)
DELETE FROM table_name
WHERE id IN (SELECT id FROM ranked WHERE rn > 1);"""

        elif insight_type == "missing_data":
            if affected_cols:
                col = affected_cols[0]
                return f"""-- Handle NULL values in '{col}'

-- Option 1: Remove rows with NULL
DELETE FROM table_name
WHERE {col} IS NULL;

-- Option 2: Update with default value
UPDATE table_name
SET {col} = 0  -- or appropriate default
WHERE {col} IS NULL;

-- Option 3: Update with average (for numeric columns)
UPDATE table_name
SET {col} = (SELECT AVG({col}) FROM table_name WHERE {col} IS NOT NULL)
WHERE {col} IS NULL;"""
            else:
                return """-- Handle NULL values

-- Remove rows where any key column is NULL
DELETE FROM table_name
WHERE column1 IS NULL
   OR column2 IS NULL
   OR column3 IS NULL;

-- Update NULLs with defaults
UPDATE table_name
SET column1 = COALESCE(column1, 'default_value');"""

        elif insight_type == "outliers":
            if affected_cols:
                col = affected_cols[0]
                return f"""-- Remove outliers from '{col}' using IQR method

-- Calculate quartiles
WITH quartiles AS (
    SELECT
        PERCENTILE_CONT(0.25) WITHIN GROUP (ORDER BY {col}) AS q1,
        PERCENTILE_CONT(0.75) WITHIN GROUP (ORDER BY {col}) AS q3
    FROM table_name
),
bounds AS (
    SELECT
        q1 - 1.5 * (q3 - q1) AS lower_bound,
        q3 + 1.5 * (q3 - q1) AS upper_bound
    FROM quartiles
)
-- Remove outliers
DELETE FROM table_name
WHERE {col} < (SELECT lower_bound FROM bounds)
   OR {col} > (SELECT upper_bound FROM bounds);"""

        return None

    def _generate_r(self, insight: Any) -> str | None:
        """Generate R code snippet.

        Args:
            insight: Insight object

        Returns:
            R code snippet
        """
        insight_type = insight.type
        affected_cols = insight.affected_columns

        if insight_type == "missing_data":
            if affected_cols:
                col = affected_cols[0]
                return f"""# Handle missing values in '{col}'
library(dplyr)

# Option 1: Remove rows with missing values
df <- df %>% filter(!is.na({col}))

# Option 2: Fill with median
df <- df %>%
  mutate({col} = ifelse(is.na({col}), median({col}, na.rm = TRUE), {col}))

# Option 3: Fill with mode
mode_value <- names(sort(table(df${col}), decreasing = TRUE))[1]
df${col}[is.na(df${col})] <- mode_value"""

        elif insight_type == "duplicates":
            return """# Remove duplicate rows
library(dplyr)

# Remove all duplicates
df <- df %>% distinct()

# Remove duplicates based on specific columns
# df <- df %>% distinct(column1, column2, .keep_all = TRUE)"""

        elif insight_type == "outliers":
            if affected_cols:
                col = affected_cols[0]
                return f"""# Remove outliers from '{col}' using IQR method
library(dplyr)

# Calculate IQR
Q1 <- quantile(df${col}, 0.25, na.rm = TRUE)
Q3 <- quantile(df${col}, 0.75, na.rm = TRUE)
IQR <- Q3 - Q1

# Define bounds
lower_bound <- Q1 - 1.5 * IQR
upper_bound <- Q3 + 1.5 * IQR

# Remove outliers
df <- df %>%
  filter({col} >= lower_bound & {col} <= upper_bound)"""

        return None
