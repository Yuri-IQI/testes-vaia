from __future__ import annotations

import argparse
from pathlib import Path

from chart_pipeline import ChartPipeline


DEFAULT_PROMPT = "bar chart with values sales: 12, support: 7, product: 15"


def execute_code(code: str, output_path: Path) -> None:
    namespace = {
        "__name__": "__main__",
        "output_path": str(output_path),
    }

    compiled = compile(code, "<vaia-matplotlib>", "exec")
    exec(compiled, namespace, namespace)

    if not output_path.exists():
        raise RuntimeError("The generated code did not create the output image.")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate a matplotlib chart from a natural language prompt."
    )
    parser.add_argument("--prompt", default=DEFAULT_PROMPT, help="Natural language chart request.")
    parser.add_argument(
        "--retries",
        type=int,
        default=2,
        help="Maximum number of retries after an execution failure.",
    )
    parser.add_argument(
        "--output",
        default="outputs/matplotlib_chart.png",
        help="Path of the output image.",
    )
    args = parser.parse_args()

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    pipeline = ChartPipeline()
    execution_error = ""
    last_result = None

    for attempt in range(1, args.retries + 2):
        result = pipeline.generate_matplotlib_code(
            args.prompt,
            retries=1,
            execution_error=execution_error,
        )
        last_result = result

        try:
            execute_code(result.code, output_path)
            print(f"Chart generated successfully on attempt {attempt}.")
            print(f"Source: {result.source}")
            print(f"Output image: {output_path.resolve()}")
            print("\nGenerated code:\n")
            print(result.code)
            return
        except Exception as exc:  # pragma: no cover - runtime validation
            execution_error = str(exc)
            print(f"Attempt {attempt} failed: {execution_error}")

    if last_result is not None:
        print("\nLast generated code:\n")
        print(last_result.code)

    raise SystemExit("Could not generate a working matplotlib script after all retries.")


if __name__ == "__main__":
    main()
