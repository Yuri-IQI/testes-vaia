from __future__ import annotations

import re
from dataclasses import dataclass, field

from chart_utils import (
    ChartSpec,
    chart_spec_to_d3_javascript,
    chart_spec_to_matplotlib_code,
    infer_chart_spec,
    validate_chart_payload,
)
from code_assistant import CodeAssistant
from examples import build_examples_block
from json_parser import extract_json, parse_json


JSON_SYSTEM_PROMPT = """
You convert chart requests into a single JSON object.

Return only valid JSON.
No markdown.
No code fences.
No explanations.
The response must start with { and end with }.

Schema:
{
  "type": "bar" | "line" | "pie",
  "labels": ["label 1", "label 2"],
  "values": [1, 2],
  "title": "Chart title"
}
""".strip()

MATPLOTLIB_SYSTEM_PROMPT = """
You write executable Python code that uses matplotlib.

Return only Python code.
No markdown.
No code fences.
The script must:
- create a variable named fig
- use matplotlib.pyplot as plt
- save the figure to output_path when output_path is defined
- call plt.show() only when output_path is empty
""".strip()


@dataclass
class ChartGenerationResult:
    chart: ChartSpec
    source: str
    raw_response: str = ""
    warnings: list[str] = field(default_factory=list)


@dataclass
class CodeGenerationResult:
    code: str
    source: str
    raw_response: str = ""
    warnings: list[str] = field(default_factory=list)


@dataclass
class D3GenerationResult:
    chart: ChartSpec
    javascript: str
    source: str
    raw_response: str = ""
    warnings: list[str] = field(default_factory=list)


class ChartPipeline:
    def __init__(self, assistant: CodeAssistant | None = None) -> None:
        self.assistant = assistant or CodeAssistant()

    def generate_chart(self, user_prompt: str, retries: int = 2) -> ChartGenerationResult:
        warnings: list[str] = []
        raw_response = ""

        for attempt in range(1, retries + 2):
            feedback = warnings[-1] if warnings else ""
            prompt = self._build_json_prompt(user_prompt, feedback)

            try:
                raw_response = self.assistant.generate_text(
                    JSON_SYSTEM_PROMPT,
                    prompt,
                    max_new_tokens=350,
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

            valid, error = validate_chart_payload(parsed)
            if not valid:
                warnings.append(f"Attempt {attempt}: {error}")
                continue

            return ChartGenerationResult(
                chart=ChartSpec.from_dict(parsed),
                source="model",
                raw_response=raw_response,
                warnings=warnings,
            )

        fallback_chart = infer_chart_spec(user_prompt)
        warnings.append("Using heuristic fallback to keep the application functional.")

        return ChartGenerationResult(
            chart=fallback_chart,
            source="fallback",
            raw_response=raw_response,
            warnings=warnings,
        )

    def generate_matplotlib_code(
        self,
        user_prompt: str,
        *,
        retries: int = 2,
        execution_error: str = "",
    ) -> CodeGenerationResult:
        warnings: list[str] = []
        raw_response = ""

        for attempt in range(1, retries + 2):
            prompt = self._build_matplotlib_prompt(user_prompt, execution_error, warnings)

            try:
                raw_response = self.assistant.generate_text(
                    MATPLOTLIB_SYSTEM_PROMPT,
                    prompt,
                    max_new_tokens=500,
                    temperature=0.1,
                )
            except RuntimeError as exc:
                warnings.append(f"Model unavailable: {exc}")
                break

            code = self._extract_python_code(raw_response)

            try:
                compile(code, "<vaia-generated>", "exec")
            except SyntaxError as exc:
                warnings.append(f"Attempt {attempt}: generated code has syntax error: {exc}")
                continue

            return CodeGenerationResult(
                code=code,
                source="model",
                raw_response=raw_response,
                warnings=warnings,
            )

        chart_result = self.generate_chart(user_prompt, retries=1)
        template_code = chart_spec_to_matplotlib_code(chart_result.chart)

        warnings.extend(chart_result.warnings)
        warnings.append("Using template-based matplotlib code.")

        return CodeGenerationResult(
            code=template_code,
            source="template",
            raw_response=raw_response,
            warnings=warnings,
        )

    def generate_d3_payload(self, user_prompt: str, retries: int = 2) -> D3GenerationResult:
        chart_result = self.generate_chart(user_prompt, retries=retries)
        javascript = chart_spec_to_d3_javascript(chart_result.chart)

        return D3GenerationResult(
            chart=chart_result.chart,
            javascript=javascript,
            source="model" if chart_result.source == "model" else "template",
            raw_response=chart_result.raw_response,
            warnings=chart_result.warnings,
        )

    def _build_json_prompt(self, user_prompt: str, feedback: str) -> str:
        prompt = [
            "Generate a chart JSON object for the next request.",
            build_examples_block(),
            f"Request: {user_prompt}",
        ]

        if feedback:
            prompt.append("Fix the previous problem before answering again.")
            prompt.append(f"Previous problem: {feedback}")

        return "\n\n".join(prompt)

    def _build_matplotlib_prompt(
        self,
        user_prompt: str,
        execution_error: str,
        warnings: list[str],
    ) -> str:
        prompt = [
            "Generate a complete Python script that renders the requested chart with matplotlib.",
            "The code must be self-contained and executable.",
            f"Request: {user_prompt}",
        ]

        if execution_error:
            prompt.append("The previous execution failed. Fix the issue and try again.")
            prompt.append(f"Execution error: {execution_error}")

        if warnings:
            prompt.append(f"Previous generation warning: {warnings[-1]}")

        return "\n\n".join(prompt)

    @staticmethod
    def _extract_python_code(raw_response: str) -> str:
        block_match = re.search(r"```(?:python)?\s*(.*?)```", raw_response, re.DOTALL)
        if block_match:
            return block_match.group(1).strip()

        return raw_response.strip()
