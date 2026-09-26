import os
import tempfile
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import mlflow
import mlflow.sklearn
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
)
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_PATH = PROJECT_ROOT / "data" / "processed" / "iris_features.csv"
FEATURE_COLUMNS = [
    "sepal length (cm)",
    "sepal width (cm)",
    "petal length (cm)",
    "petal width (cm)",
    "sepal_area",
    "petal_area",
    "sepal_to_petal_length_ratio",
]
TARGET_COLUMN = "species"
EXPERIMENT_NAME = "iris-classification-baseline"


def load_dataset():
    df = pd.read_csv(DATA_PATH)

    missing_columns = [col for col in FEATURE_COLUMNS + [TARGET_COLUMN] if col not in df.columns]
    if missing_columns:
        raise ValueError(f"Dataset is missing required columns: {missing_columns}")

    return df


def prepare_features_and_target(df):
    X = df[FEATURE_COLUMNS].copy()
    X = X.fillna(X.median())

    label_encoder = LabelEncoder()
    y = label_encoder.fit_transform(df[TARGET_COLUMN])
    return X, y, label_encoder


def get_model_definitions():
    return [
        {
            "model_name": "LogisticRegression",
            "model": LogisticRegression(max_iter=200, C=1.0),
        },
        {
            "model_name": "RandomForestClassifier_50_3",
            "model": RandomForestClassifier(
                n_estimators=50,
                max_depth=3,
                random_state=42,
            ),
        },
        {
            "model_name": "RandomForestClassifier_200_None",
            "model": RandomForestClassifier(
                n_estimators=200,
                max_depth=None,
                random_state=42,
            ),
        },
    ]


def log_confusion_matrix(y_true, y_pred, label_encoder):
    labels = list(label_encoder.classes_)
    cm = confusion_matrix(y_true, y_pred, labels=range(len(labels)))

    fig, ax = plt.subplots(figsize=(6, 5))
    ax.imshow(cm, interpolation="nearest", cmap="Blues")
    ax.set_title("Confusion Matrix")
    ax.set_xticks(range(len(labels)))
    ax.set_yticks(range(len(labels)))
    ax.set_xticklabels(labels)
    ax.set_yticklabels(labels)
    ax.set_xlabel("Predicted label")
    ax.set_ylabel("True label")

    for i in range(cm.shape[0]):
        for j in range(cm.shape[1]):
            ax.text(j, i, cm[i, j], ha="center", va="center", color="white" if cm[i, j] > cm.max() / 2 else "black")

    fig.tight_layout()

    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as temp_file:
        temp_path = temp_file.name

    fig.savefig(temp_path)
    plt.close(fig)
    return temp_path


def evaluate_model(model, X_test, y_test, label_encoder):
    predictions = model.predict(X_test)

    metrics = {
        "accuracy": accuracy_score(y_test, predictions),
        "precision_macro": precision_score(y_test, predictions, average="macro", zero_division=0),
        "recall_macro": recall_score(y_test, predictions, average="macro", zero_division=0),
        "f1_macro": f1_score(y_test, predictions, average="macro", zero_division=0),
    }

    confusion_matrix_path = log_confusion_matrix(y_test, predictions, label_encoder)
    return metrics, confusion_matrix_path


def main():
    tracking_uri = os.getenv("MLFLOW_TRACKING_URI", "http://127.0.0.1:5000")
    mlflow.set_tracking_uri(tracking_uri)
    mlflow.set_experiment(EXPERIMENT_NAME)

    df = load_dataset()
    X, y, label_encoder = prepare_features_and_target(df)

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.20,
        random_state=42,
        stratify=y,
    )

    results = []

    for model_info in get_model_definitions():
        model_name = model_info["model_name"]
        model = model_info["model"]

        with mlflow.start_run(run_name=model_name) as run:
            model.fit(X_train, y_train)

            metrics, confusion_matrix_path = evaluate_model(model, X_test, y_test, label_encoder)

            params = model.get_params()
            mlflow.log_param("model_name", model_name)
            for param_name, param_value in params.items():
                mlflow.log_param(param_name, str(param_value) if param_value is None else param_value)

            for metric_name, metric_value in metrics.items():
                mlflow.log_metric(metric_name, float(metric_value))

            mlflow.log_artifact(confusion_matrix_path, artifact_path="plots")
            mlflow.sklearn.log_model(model, artifact_path="model")

            os.remove(confusion_matrix_path)

            print(f"\nModel: {model_name}")
            print(f"Run ID: {run.info.run_id}")
            print("Parameters:")
            for param_name, param_value in params.items():
                print(f"  {param_name}: {param_value}")
            print("Metrics:")
            for metric_name, metric_value in metrics.items():
                print(f"  {metric_name}: {metric_value:.4f}")

            result_row = {
                "model_name": model_name,
                "run_id": run.info.run_id,
                **metrics,
            }
            results.append(result_row)

    comparison_df = pd.DataFrame(results)
    print("\nComparison table of all 3 models:")
    print(
        comparison_df[["model_name", "accuracy", "precision_macro", "recall_macro", "f1_macro"]]
        .sort_values("f1_macro", ascending=False)
        .to_string(index=False)
    )

    best_model = comparison_df.loc[comparison_df["f1_macro"].idxmax()]
    print(f"\nBest model by highest f1_macro: {best_model['model_name']} (f1_macro={best_model['f1_macro']:.4f})")


if __name__ == "__main__":
    main()
