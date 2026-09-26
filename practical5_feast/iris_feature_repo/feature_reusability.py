from feast import FeatureStore

store = FeatureStore(repo_path="feature_repo")

entity_rows = [{"sample_id": 1}, {"sample_id": 3}]
feature_service = store.get_feature_service("iris_feature_service")

service_result = store.get_online_features(
    features=feature_service,
    entity_rows=entity_rows,
).to_dict()

print("Feature service retrieval (reused registered features):")
for key, value in sorted(service_result.items()):
    print(f"{key}: {value}")

print("\nSame registered features reused without redefining the engineered logic.")
