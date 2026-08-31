import pandas as pd

data = {
    "sepal length (cm)": [5.1, 4.9, 4.7, 4.6, 5.0] * 30,
    "sepal width (cm)": [3.5, 3.0, 3.2, 3.1, 3.6] * 30,
    "petal length (cm)": [1.4, 1.4, 1.3, 1.5, 1.4] * 30,
    "petal width (cm)": [0.2, 0.2, 0.2, 0.2, 0.2] * 30,
    "target": [0, 0, 0, 0, 0] * 30
}

df = pd.DataFrame(data)
df.to_csv("data/raw/iris_v1.csv", index=False)

print(f"Saved {len(df)} rows to data/raw/iris_v1.csv")