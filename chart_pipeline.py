from __future__ import annotations
import json
from dataclasses import dataclass, field
import pandas as pd
from chart_utils import (
    VisualizationSpec,
    aggregate_for_visualization,
    build_frontend_records,
    infer_visualization_spec,
    resolve_and_validate_visualization_payload,
    summarize_dataframe,
)
from code_assistant import CodeAssistant
from examples import build_examples_block
from json_parser import extract_json, parse_json
from peft import PeftModel

VISUALIZATION_SYSTEM_PROMPT = """
You are a financial dataset visualization assistant.

Return ONLY valid JSON.
Do not use markdown.
Do not use code fences.
Do not explain outside JSON.
Do not invent columns.
Do not invent values.
Use ONLY columns that exist in the provided dataset summary.
Supported chart types: line, bar, pie.
Supported aggregations: sum, mean, count.
Use the color field only for grouped line or bar charts.
Never use color with pie charts.
Prefer date or time columns for line charts when the request is about trends over time.

Required JSON schema:
{
  "type": "line" | "bar" | "pie",
  "data": {
    "dimension": "existing dataset column",
    "metric": "existing dataset column",
    "aggregation": "sum" | "mean" | "count",
    "color": "optional existing dataset column"
  },
  "title": "chart title",
  "description": "short description of what the chart shows",
  "explanation": "short explanation for why the chart fits the request"
}
""".strip()


@dataclass
class VisualizationGenerationResult:
    spec: VisualizationSpec
    plot_frame: pd.DataFrame
    source: str
    summary: dict[str, object]
    raw_response: str = ""
    warnings: list[str] = field(default_factory=list)

    def frontend_records(self) -> list[dict[str, object]]:
        return build_frontend_records(self.plot_frame)

class DesenrolaAssistant(CodeAssistant):
    def _ensure_loaded(self) -> None:
        super()._ensure_loaded()
        self._model = PeftModel.from_pretrained(self._model, "./desenrola_model_1.5B")
        self._model = self._model.merge_and_unload()

class ChartPipeline:
    def __init__(self, assistant: CodeAssistant | None = None) -> None:
        self.assistant = assistant or CodeAssistant()

    def generate_visualization(
        self,
        frame: pd.DataFrame,
        user_prompt: str,
        retries: int = 2,
    ) -> VisualizationGenerationResult:
        summary = summarize_dataframe(frame)
        warnings: list[str] = []
        raw_response = ""

        for attempt in range(1, retries + 2):
            feedback = warnings[-1] if warnings else ""
            prompt = self._build_prompt(summary, user_prompt, feedback)

            try:
                raw_response = self.assistant.generate_text(
                    VISUALIZATION_SYSTEM_PROMPT,
                    prompt,
                    max_new_tokens=500,
                    temperature=0.1,
                )
            except RuntimeError as exc:
                warnings.append(f"Model unavailable: {exc}")
                break

            json_text = extract_json(raw_response)
            if not json_text:
                warnings.append(f"Attempt {attempt}: the response did not contain a valid JSON object.")
                continue

            parsed = parse_json(json_text)
            if parsed is None:
                warnings.append(f"Attempt {attempt}: the JSON could not be parsed.")
                continue

            normalized, error = resolve_and_validate_visualization_payload(parsed, frame)
            if normalized is None:
                warnings.append(f"Attempt {attempt}: {error}")
                continue

            spec = VisualizationSpec.from_dict(normalized)
            plot_frame = aggregate_for_visualization(frame, spec)

            return VisualizationGenerationResult(
                spec=spec,
                plot_frame=plot_frame,
                source="model",
                summary=summary,
                raw_response=raw_response,
                warnings=warnings,
            )

        fallback_spec = infer_visualization_spec(frame, user_prompt)
        plot_frame = aggregate_for_visualization(frame, fallback_spec)
        warnings.append("Using heuristic fallback to keep the application functional.")

        return VisualizationGenerationResult(
            spec=fallback_spec,
            plot_frame=plot_frame,
            source="fallback",
            summary=summary,
            raw_response=raw_response,
            warnings=warnings,
        )

    def _build_prompt(self, summary: dict[str, object], user_prompt: str, feedback: str) -> str:
        blocks = [
            "Dataset summary:",
            json.dumps(summary, indent=2, ensure_ascii=False),
            "",
            "Examples:",
                build_examples_block(),
            "",
            f'User request: "{user_prompt}"',
            "Return a visualization specification JSON using only dataset columns from the summary.",
        ]

        if feedback:
            blocks.extend(
                [
                    "",
                    "Fix the previous problem before answering again.",
                    f"Previous validation error: {feedback}",
                ]
            )

        return "\n".join(blocks).strip()
