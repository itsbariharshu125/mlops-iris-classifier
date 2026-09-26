from feast import FeatureStore

store = FeatureStore(repo_path="feature_repo")

entity_rows = [{"sample_id": 1}, {"sample_id": 2}]
features = [
    "iris_measurements:sepal length (cm)",
    "iris_measurements:sepal width (cm)",
    "iris_measurements:petal length (cm)",
    "iris_measurements:petal width (cm)",
    "iris_measurements:species",
    "iris_engineered:sepal_area",
    "iris_engineered:petal_area",
    "iris_engineered:sepal_to_petal_length_ratio",
    "iris_engineered:petal_length_bin",
]

online_features = store.get_online_features(
    features=features,
    entity_rows=entity_rows,
).to_dict()

print("Online retrieval using direct feature view references:")
for key, value in sorted(online_features.items()):
    print(f"{key}: {value}")

feature_service = store.get_feature_service("iris_feature_service")
service_features = store.get_online_features(
    features=feature_service,
    entity_rows=entity_rows,
).to_dict()

print("\nOnline retrieval using iris_feature_service:")
for key, value in sorted(service_features.items()):
    print(f"{key}: {value}")
