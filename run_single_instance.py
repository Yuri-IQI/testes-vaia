import pandas as pd
from chart_pipeline import ChartPipeline
from code_assistant import CodeAssistant
from peft import PeftModel

class DesenrolaAssistant(CodeAssistant):
    def _ensure_loaded(self) -> None:
        super()._ensure_loaded()
        self._model = PeftModel.from_pretrained(self._model, "./desenrola_model_1.5B")
        self._model = self._model.merge_and_unload()

DATASET_PATH = "./sample_data/dados_desenrola.csv"

df = pd.read_csv(DATASET_PATH, sep=";", decimal=",")
df["DATA_BASE"] = pd.to_datetime(df["DATA_BASE"].astype(str), format="%Y%m")
df["COD_CONGLOMERADO_FINANCEIRO"] = df["COD_CONGLOMERADO_FINANCEIRO"].astype(str)

pipeline = ChartPipeline(assistant=DesenrolaAssistant())
result = pipeline.generate_visualization(df, "Qual banco tem maior volume?")

print(result.spec)
print(result.frontend_records())