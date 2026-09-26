import os

import mlflow
import mlflow.sklearn
import pandas as pd

TRACKING_URI = os.getenv("MLFLOW_TRACKING_URI", "http://127.0.0.1:5000")
MODEL_URI = "models:/iris-classifier-prod/Staging"
FEATURE_COLUMNS = [
    "sepal length (cm)",
    "sepal width (cm)",
    "petal length (cm)",
    "petal width (cm)",
    "sepal_area",
    "petal_area",
    "sepal_to_petal_length_ratio",
]

mlflow.set_tracking_uri(TRACKING_URI)
model = mlflow.sklearn.load_model(MODEL_URI)
print("Loaded model:")
print(model)

sample_row = pd.DataFrame(
    [
        {
            "sepal length (cm)": 5.1,
            "sepal width (cm)": 3.5,
            "petal length (cm)": 1.4,
            "petal width (cm)": 0.2,
            "sepal_area": 17.85,
            "petal_area": 0.28,
            "sepal_to_petal_length_ratio": 3.64,
        }
    ],
    columns=FEATURE_COLUMNS,
)

prediction = model.predict(sample_row)
print("Prediction for sample row:")
print(prediction)
