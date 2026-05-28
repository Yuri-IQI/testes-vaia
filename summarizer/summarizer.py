import os
import sys
import json
import pandas as pd

from generator.dataset import summarize_dataframe

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(ROOT_DIR)

dataset_name = input("Caminho para o dataset:\n").strip()

if not os.path.isabs(dataset_name):
    caminho_final = os.path.join(ROOT_DIR, dataset_name)
else:
    caminho_final = dataset_name

try:
    df = pd.read_csv(caminho_final, sep=None, engine="python")
except Exception:
    df = pd.read_csv(caminho_final)

df.columns = [col.strip() for col in df.columns]

for col in df.columns:
    col_lower = col.lower()

    if any(keyword in col_lower for keyword in ["date", "data", "time"]):
        try:
            df[col] = pd.to_datetime(df[col], errors="ignore")
        except Exception:
            pass

for col in df.columns:
    if df[col].dtype == object:
        try:
            cleaned = (
                df[col]
                .astype(str)
                .str.replace(".", "", regex=False)
                .str.replace(",", ".", regex=False)
            )

            converted = pd.to_numeric(cleaned, errors="coerce")

            if converted.notna().mean() > 0.7:
                df[col] = converted

        except Exception:
            pass

summary = summarize_dataframe(df)

print(json.dumps(summary, indent=2, ensure_ascii=False, default=str))

base_name = os.path.splitext(os.path.basename(dataset_name))[0]

output_filename = f"summary_{base_name}.py"

output_path = os.path.join(
    os.path.dirname(__file__),
    "summaries",
    output_filename
)

os.makedirs(os.path.dirname(output_path), exist_ok=True)

with open(output_path, "w", encoding="utf-8") as f:
    f.write(
        "dataset_summary = "
        + json.dumps(summary, indent=2, ensure_ascii=False, default=str)
    )

print(f"\nResumo salvo em: {output_path}")