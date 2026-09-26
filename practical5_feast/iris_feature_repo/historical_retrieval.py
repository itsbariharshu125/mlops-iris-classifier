import pandas as pd
from feast import FeatureStore

store = FeatureStore(repo_path="feature_repo")

entity_df = pd.read_parquet("feature_repo/data/iris_features.parquet")[
    ["sample_id", "event_timestamp"]
].head(5)

historical_df = store.get_historical_features(
    entity_df=entity_df,
    features=[
        "iris_measurements:sepal length (cm)",
        "iris_measurements:sepal width (cm)",
        "iris_measurements:petal length (cm)",
        "iris_measurements:petal width (cm)",
        "iris_measurements:species",
        "iris_engineered:sepal_area",
        "iris_engineered:petal_area",
        "iris_engineered:sepal_to_petal_length_ratio",
        "iris_engineered:petal_length_bin",
    ],
).to_df()

print("Historical retrieval results:")
print(historical_df)
