import os
import pandas as pd
import json
from chart_utils import summarize_dataframe

dataset_name = input("Caminho para o dataset: \n")

if not os.path.isabs(dataset_name):
    raiz_projeto = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    caminho_final = os.path.join(raiz_projeto, dataset_name)
else:
    caminho_final = dataset_name

df = pd.read_csv(dataset_name, sep=";", decimal=",")
df["DATA_BASE"] = pd.to_datetime(df["DATA_BASE"].astype(str), format="%Y%m")
df["COD_CONGLOMERADO_FINANCEIRO"] = df["COD_CONGLOMERADO_FINANCEIRO"].astype(str)

summary = summarize_dataframe(df)
print(json.dumps(summary, indent=2, ensure_ascii=False))

base_name = os.path.splitext(os.path.basename(dataset_name))[0]

output_filename = f"summary_{base_name}.py"
output_path = os.path.join(os.path.dirname(__file__), "summaries", output_filename)

os.makedirs(os.path.dirname(output_path), exist_ok=True)

with open(output_path, "w", encoding="utf-8") as f:
    f.write(f"desenrola_summary = {json.dumps(summary, indent=2, ensure_ascii=False)}")

print(f"\nResumo salvo como arquivo Python em: {output_path}")