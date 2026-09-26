from pathlib import Path

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[2]
SOURCE = PROJECT_ROOT / "data" / "processed" / "iris_features.csv"
OUTPUT = Path(__file__).resolve().parent / "feature_repo" / "data" / "iris_features.parquet"

df = pd.read_csv(SOURCE)
df.insert(0, "sample_id", range(1, len(df) + 1))
df["event_timestamp"] = pd.Timestamp.utcnow()
df["created_timestamp"] = df["event_timestamp"]

OUTPUT.parent.mkdir(parents=True, exist_ok=True)
df.to_parquet(OUTPUT, index=False)

print(f"Prepared {len(df)} rows -> {OUTPUT}")
print("Shape:", df.shape)
print("Columns:")
print(df.columns.tolist())
