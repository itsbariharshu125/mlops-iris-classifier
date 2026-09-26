import os

import mlflow
import mlflow.sklearn
from mlflow.tracking import MlflowClient

MLFLOW_TRACKING_URI = os.getenv("MLFLOW_TRACKING_URI", "http://127.0.0.1:5000")
EXPERIMENT_NAME = "iris-classification-baseline"
MODEL_NAME = "iris-classifier-prod"

mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
client = MlflowClient()
experiment = client.get_experiment_by_name(EXPERIMENT_NAME)

if experiment is None:
    raise RuntimeError(f"Experiment not found: {EXPERIMENT_NAME}")

runs = client.search_runs(
    experiment_ids=[experiment.experiment_id],
    order_by=["metrics.f1_macro DESC"],
    max_results=10,
)

if not runs:
    raise RuntimeError(f"No runs found in experiment: {EXPERIMENT_NAME}")

best_run = runs[0]
best_run_id = best_run.info.run_id
best_f1 = best_run.data.metrics.get("f1_macro")
model_uri = f"runs:/{best_run_id}/model"

print(f"Best run ID: {best_run_id}")
print(f"Best F1: {best_f1}")
print(f"Model URI: {model_uri}")
print(f"Registered model name: {MODEL_NAME}")

existing_model = None
try:
    existing_model = mlflow.pyfunc.get_model_version(model_name=MODEL_NAME, version="latest")
except Exception:
    existing_model = None

if existing_model is not None:
    print(f"Model already exists with latest version: {existing_model.version}")

registered_model = mlflow.register_model(model_uri=model_uri, name=MODEL_NAME)
print(f"Registered version: {registered_model.version}")

client.transition_model_version_stage(
    name=MODEL_NAME,
    version=registered_model.version,
    stage="Staging",
    archive_existing_versions=True,
)

version = client.get_model_version(name=MODEL_NAME, version=registered_model.version)
print(f"Stage: {version.current_stage}")
print(f"Model URI for Staging: models:/{MODEL_NAME}/Staging")
