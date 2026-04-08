from __future__ import annotations

import argparse
import json
from pathlib import Path

import matplotlib

from chart_pipeline import ChartPipeline
from chart_utils import build_matplotlib_figure, load_csv_dataset


matplotlib.use("Agg")

PROJECT_DIR = Path(__file__).resolve().parent
DEFAULT_DATASET = PROJECT_DIR / "sample_data" / "sample_sales_data.csv"
DEFAULT_PROMPT = "Compare total sales by country in a bar chart and split by product line."


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate a chart from a real CSV dataset using a natural language prompt."
    )
    parser.add_argument(
        "--dataset",
        default=str(DEFAULT_DATASET),
        help="Path to the CSV dataset.",
    )
    parser.add_argument(
        "--prompt",
        default=DEFAULT_PROMPT,
        help="Natural language visualization request.",
    )
    parser.add_argument(
        "--output",
        default="outputs/dataset_chart.png",
        help="Path of the output image.",
    )
    args = parser.parse_args()

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    frame = load_csv_dataset(args.dataset)
    pipeline = ChartPipeline()
    result = pipeline.generate_visualization(frame, args.prompt)
    figure = build_matplotlib_figure(result.plot_frame, result.spec)
    figure.savefig(output_path, dpi=150, bbox_inches="tight")

    print(f"Chart saved to: {output_path.resolve()}")
    print(f"Specification source: {result.source}")
    print("\nVisualization spec:\n")
    print(json.dumps(result.spec.to_dict(), indent=2, ensure_ascii=False))

    if result.warnings:
        print("\nWarnings:")
        for warning in result.warnings:
            print(f"- {warning}")


if __name__ == "__main__":
    main()
