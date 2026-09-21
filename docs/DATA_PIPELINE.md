# Data Pipeline Documentation

## Overview

This project implements an automated and reproducible data pipeline using DVC.

## Pipeline Stages

### 1. Collect

**Purpose:** Collect the Iris dataset and store the raw data.

**Input:** Iris dataset from scikit-learn

**Output:**
- `data/raw/iris_raw.csv`

### 2. Preprocess

**Purpose:** Clean the raw dataset.

Operations:
- Remove duplicate rows
- Convert numeric columns to numeric types
- Fill missing numeric values using median
- Remove rows with missing species
- Remove `collected_at`

**Input:**
- `data/raw/iris_raw.csv`

**Output:**
- `data/processed/iris_preprocessed.csv`

### 3. Features

**Purpose:** Create additional features from the preprocessed data.

Features:
- `sepal_area`
- `petal_area`
- `sepal_to_petal_length_ratio`
- `petal_length_bin`

**Input:**
- `data/processed/iris_preprocessed.csv`

**Output:**
- `data/processed/iris_features.csv`

### 4. Validate

**Purpose:** Validate the final dataset before further use.

Validation checks:
- Required columns exist
- No null values
- Valid species values
- Measurement values are within expected ranges

**Input:**
- `data/processed/iris_features.csv`

**Output:**
- Validation result

## Pipeline Flow

```text
Raw Iris Data
      |
      v
   Collect
      |
      v
   Preprocess
      |
      v
   Features
      |
      v
   Validate