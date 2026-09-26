# Feature Store Analysis

## Overview

This practical uses Feast to centralize and manage the Iris feature pipeline for both offline training and online inference. The feature definitions are registered once in the repository and then consumed by training, batch, and serving workflows without redefining the feature logic in multiple places.

## Key benefits

- Feature reusability: the same feature views are reused for multiple retrieval flows instead of being duplicated in separate training and inference scripts.
- Centralized feature management: the feature definitions live in one Feast repository and are versioned through the registry.
- Consistency between training and serving: the same data schema is exposed through both offline and online retrieval paths.
- Reduced duplication: the engineered feature logic is defined once in the feature store rather than copied into individual training or inference notebooks/scripts.
- Online and offline retrieval: Feast supports low-latency online retrieval for serving and historical retrieval for training and backfills.
- Point-in-time historical retrieval: the event timestamp on the source data supports time-aware historical feature extraction for ML training.

## Registered feature views

- iris_measurements
  - sepal length (cm)
  - sepal width (cm)
  - petal length (cm)
  - petal width (cm)
  - species
- iris_engineered
  - sepal_area
  - petal_area
  - sepal_to_petal_length_ratio
  - petal_length_bin

## Feature service

- iris_feature_service
  - combines the measurement features and engineered features into a single reusable service interface.

## Practical impact

Feast reduces the risk of schema drift between the raw training data and serving data because both systems read from the same registered feature definitions. It also makes feature logic easier to maintain by moving feature logic into a single managed layer rather than scattering feature engineering code across multiple scripts.

## Retrieval patterns used

- Online retrieval using FeatureStore and entity rows for sample_id values such as 1 and 2.
- Historical retrieval using get_historical_features() with the Parquet source and event_timestamp.
- Feature service retrieval using iris_feature_service to show that the same registered features can be requested without rewriting the feature engineering code.

## Conclusion

The Feast implementation in this practical demonstrates a production-style feature pipeline: features are defined once, stored centrally, reused consistently, and retrieved through both online and offline access patterns.
