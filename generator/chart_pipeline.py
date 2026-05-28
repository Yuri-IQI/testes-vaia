from __future__ import annotations
from dataclasses import dataclass, field
import pandas as pd
from code_assistant import CodeAssistant
from generator.aggregator import aggregate_for_visualization, build_frontend_records
from generator.dataset import summarize_dataframe
from generator.fallback_inferrer import infer_visualization_spec
from generator.models import VisualizationSpec
from generator.prompt_builder import build_prompt
from generator.spec_resolver import resolve_and_validate_visualization_payload
from json_parser import extract_json, parse_json

VISUALIZATION_SYSTEM_PROMPT = """
You are a financial dataset visualization assistant.

Return ONLY valid JSON. No markdown, no code fences, no explanation outside JSON.
Do not invent columns or values. Use ONLY columns from the dataset summary.

Never use "table" as a chart type. If the request is ambiguous, default to bar.
Supported chart types are only: line, bar, pie, scatter, histogram, box.Aggregations: sum, mean, count. Null for scatter, histogram, box.
dimension is null only for histogram.
color must be a column name (e.g. "Stock Index"), never a column value (e.g. "Dow Jones").

DOW JONES ISN'T A COLUMN, IF A SPECIFIC STOCK INDEX IS REQUIRED IT SHOULD BE A FILTER
(e.g. "filters": {"Stock Index": [Dow Jones]})

Use filters to restrict rows to specific column values when the user names a specific entity (e.g. "for Dow Jones", "only S&P 500").
Never put column values in the color field.

{
  "type": "line|bar|pie|scatter|histogram|box",
  "data": {
    "dimension": "column or null",
    "metric": "column",
    "metric_secondary": "column or null",
    "aggregation": "sum|mean|count|null",
    "color": "column or null",
    "filters": {"column": ["value1", "value2"]} or {}
  },
  "render_options": {
    "log_scale_y": false,
    "show_trend_line": false,
    "nbins": null,
    "top_n": null
  },
  "title": "...",
  "description": "...",
  "explanation": "..."
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

        for attempt in range(1, retries):
            feedback = warnings[-1] if warnings else ""
                        
            # TODO: Substituir
            prompt = build_prompt(summary, user_prompt, feedback)

            try:
                raw_response = self.assistant.generate_text(
                    VISUALIZATION_SYSTEM_PROMPT,
                    prompt,
                    max_new_tokens=600,
                    temperature=0.1,
                )
            except RuntimeError as exc:
                warnings.append(f"Model unavailable: {exc}")
                break

            print(raw_response)

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
            
            if spec.chart_type == "histogram" and spec.render_options.nbins is None:
                unique = frame[spec.data.metric].nunique()
                spec.render_options.nbins = 20 if unique <= 30 else 40 if unique <= 200 else 60
            
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