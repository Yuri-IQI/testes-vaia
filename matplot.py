from __future__ import annotations

import argparse
import json
import os
from pathlib import Path

import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt

import pandas as pd
from peft import PeftModel

from chart_pipeline import ChartPipeline
from chart_utils import build_matplotlib_figure, load_csv_dataset
from code_assistant import CodeAssistant

PROJECT_DIR = Path(__file__).resolve().parent
DEFAULT_DATASET = PROJECT_DIR / "sample_data" / "sample_sales_data.csv"
DEFAULT_PROMPT = "Compare total sales by country in a bar chart and split by product line."
DEFAULT_ADAPTER = PROJECT_DIR / "desenrola_model_1.5B"
DEFAULT_MODEL_NAME = os.getenv("VAIA_MODEL_NAME", "Qwen/Qwen2.5-1.5B-Instruct")


class FineTunedAssistant(CodeAssistant):
    def __init__(self, adapter_path: str, model_name: str = DEFAULT_MODEL_NAME) -> None:
        super().__init__(model_name=model_name)
        self.adapter_path = adapter_path

    def _ensure_loaded(self) -> None:
        super()._ensure_loaded()
        if self.adapter_path and Path(self.adapter_path).exists():
            self._model = PeftModel.from_pretrained(self._model, self.adapter_path)
            self._model = self._model.merge_and_unload()
            print(f"Adapter loaded from: {self.adapter_path}")
        else:
            print("No adapter found, using base model.")


def load_desenrola(path: str) -> pd.DataFrame:
    df = pd.read_csv(path, sep=";", decimal=",")
    df["DATA_BASE"] = pd.to_datetime(df["DATA_BASE"].astype(str), format="%Y%m")
    df["COD_CONGLOMERADO_FINANCEIRO"] = df["COD_CONGLOMERADO_FINANCEIRO"].astype(str)
    return df


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate a chart from a CSV dataset using a fine-tuned model."
    )
    parser.add_argument("--dataset", default=str(DEFAULT_DATASET))
    parser.add_argument("--prompt", default=DEFAULT_PROMPT)
    parser.add_argument("--adapter", default=str(DEFAULT_ADAPTER))
    parser.add_argument("--desenrola", action="store_true")
    parser.add_argument("--model", default=DEFAULT_MODEL_NAME, dest="model_name")

    args = parser.parse_args()

    frame = load_desenrola(args.dataset) if args.desenrola else load_csv_dataset(args.dataset)

    assistant = FineTunedAssistant(adapter_path=args.adapter, model_name=args.model_name)
    pipeline = ChartPipeline(assistant=assistant)

    result = pipeline.generate_visualization(frame, args.prompt)
    figure = build_matplotlib_figure(result.plot_frame, result.spec)

    print(f"Specification source: {result.source}")
    print(json.dumps(result.spec.to_dict(), indent=2, ensure_ascii=False))

    plt.show()


if __name__ == "__main__":
    main()