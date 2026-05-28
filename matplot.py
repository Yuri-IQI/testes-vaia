from __future__ import annotations

import argparse
import json
import os
from pathlib import Path

import matplotlib

from generator.chart_pipeline import ChartPipeline
from generator.renderer import build_matplotlib_figure

try:
    matplotlib.use("TkAgg")
except Exception:
    matplotlib.use("Agg")

import matplotlib.pyplot as plt
import pandas as pd

from peft import PeftModel

from code_assistant import CodeAssistant


PROJECT_DIR = Path(__file__).resolve().parent

DEFAULT_DATASET = (
    PROJECT_DIR
    / "sample_data"
    / os.getenv("DEFAULT_DATASET_NAME", "finance_economics_dataset.csv")
)

DEFAULT_PROMPT = (
    "Show trends in the dataset using the best possible visualization."
)

DEFAULT_ADAPTER = os.getenv("DEFAULT_ADAPTER", "financial_adapter")

DEFAULT_MODEL_NAME = os.getenv(
    "BASE_MODEL",
    "Qwen/Qwen2.5-0.5B-Instruct"
)


class FineTunedAssistant(CodeAssistant):
    def __init__(
        self,
        adapter_path: str | None = None,
        model_name: str = DEFAULT_MODEL_NAME
    ) -> None:
        super().__init__(model_name=model_name)
        self.adapter_path = adapter_path

    def _ensure_loaded(self) -> None:
        super()._ensure_loaded()

        if (
            self.adapter_path
            and Path(self.adapter_path).exists()
        ):
            print(f"Loading adapter: {self.adapter_path}")

            self._model = PeftModel.from_pretrained(
                self._model,
                self.adapter_path
            )

            self._model = self._model.merge_and_unload()

            print("Adapter merged successfully.")

        else:
            print("No adapter found. Using base model.")


def auto_load_dataset(path: str) -> pd.DataFrame:
    """
    Generic CSV loader that:
    - detects separator automatically
    - parses dates automatically
    - converts numeric columns automatically
    """

    try:
        df = pd.read_csv(
            path,
            sep=None,
            engine="python"
        )
    except Exception:
        df = pd.read_csv(path)

    df.columns = [str(col).strip() for col in df.columns]

    for col in df.columns:
        col_lower = col.lower()

        if any(
            keyword in col_lower
            for keyword in [
                "date",
                "data",
                "time",
                "timestamp",
                "period"
            ]
        ):
            try:
                df[col] = pd.to_datetime(
                    df[col],
                    errors="ignore"
                )
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

                numeric = pd.to_numeric(
                    cleaned,
                    errors="coerce"
                )

                if numeric.notna().mean() > 0.7:
                    df[col] = numeric

            except Exception:
                pass

    return df


def main() -> None:

    parser = argparse.ArgumentParser(
        description=(
            "Generate charts from CSV datasets "
            "using a fine-tuned LLM."
        )
    )

    parser.add_argument(
        "--dataset",
        default=str(DEFAULT_DATASET),
        help="Path to CSV dataset"
    )

    parser.add_argument(
        "--prompt",
        default=DEFAULT_PROMPT,
        help="Visualization request prompt"
    )

    parser.add_argument(
        "--adapter",
        default=DEFAULT_ADAPTER,
        help="LoRA adapter path"
    )

    parser.add_argument(
        "--model",
        default=DEFAULT_MODEL_NAME,
        dest="model_name",
        help="Base model name"
    )

    parser.add_argument(
        "--save",
        default=None,
        help="Save figure to file"
    )

    args = parser.parse_args()

    dataset_path = Path(args.dataset)

    if not dataset_path.exists():
        raise FileNotFoundError(
            f"Dataset not found: {dataset_path}"
        )

    print(f"Loading dataset: {dataset_path}")

    frame = auto_load_dataset(str(dataset_path))

    print(f"Rows: {len(frame)}")
    print(f"Columns: {len(frame.columns)}")

    assistant = FineTunedAssistant(
        adapter_path=args.adapter,
        model_name=args.model_name
    )

    pipeline = ChartPipeline(
        assistant=assistant
    )

    print("\nGenerating visualization...\n")

    result = pipeline.generate_visualization(
        frame,
        args.prompt
    )

    print(result)
    print(result.spec)
    print(result.plot_frame.columns.tolist())
    print(result.plot_frame.head())
    print(result.spec.data.dimension, result.spec.data.metric)

    figure = build_matplotlib_figure(
        result.plot_frame,
        result.spec
    )

    print(f"\nSpecification source: {result.source}\n")

    print(
        json.dumps(
            result.spec.to_dict(),
            indent=2,
            ensure_ascii=False,
            default=str
        )
    )

    if args.save:
        plt.savefig(args.save, bbox_inches="tight")
        print(f"\nFigure saved to: {args.save}")

    plt.show()


if __name__ == "__main__":
    main()