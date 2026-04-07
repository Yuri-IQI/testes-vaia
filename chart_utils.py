from __future__ import annotations

import json
import re
from dataclasses import dataclass
from typing import Any


SUPPORTED_CHART_TYPES = ("bar", "line", "pie")
MONTH_LABELS = {
    "jan",
    "feb",
    "mar",
    "apr",
    "may",
    "jun",
    "jul",
    "aug",
    "sep",
    "oct",
    "nov",
    "dec",
    "abr",
    "mai",
    "ago",
    "set",
    "out",
    "dez",
}

PAIR_CHUNK_PATTERN = re.compile(
    r"^\s*([A-Za-z][A-Za-z0-9 _/\-]*)\s*[:=]\s*(-?\d+(?:[.,]\d+)?)\s*$"
)
SPACE_PAIR_PATTERN = re.compile(
    r"^\s*([A-Za-z][A-Za-z0-9 _/\-]*)\s+(-?\d+(?:[.,]\d+)?)\s*$"
)
LABELS_WITH_VALUES_PATTERN = re.compile(
    r"([A-Za-z][A-Za-z0-9 _/\-]*(?:\s*,\s*[A-Za-z][A-Za-z0-9 _/\-]*)+)\s*:\s*"
    r"((-?\d+(?:[.,]\d+)?\s*,\s*)+-?\d+(?:[.,]\d+)?)"
)
NUMBER_PATTERN = re.compile(r"-?\d+(?:[.,]\d+)?")


@dataclass
class ChartSpec:
    chart_type: str
    labels: list[str]
    values: list[float]
    title: str

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> "ChartSpec":
        normalized = normalize_chart_payload(payload)
        return cls(
            chart_type=normalized["type"],
            labels=normalized["labels"],
            values=normalized["values"],
            title=normalized["title"],
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "type": self.chart_type,
            "labels": self.labels,
            "values": [_compact_number(value) for value in self.values],
            "title": self.title,
        }


def _compact_number(value: float) -> int | float:
    return int(value) if float(value).is_integer() else value


def _coerce_number(value: Any) -> float:
    if isinstance(value, bool):
        raise ValueError("Boolean values are not valid chart numbers.")

    if isinstance(value, (int, float)):
        return float(value)

    if isinstance(value, str):
        normalized = value.strip().replace("%", "").replace(",", ".")
        return float(normalized)

    raise ValueError(f"Unsupported numeric value: {value!r}")


def _default_labels(count: int) -> list[str]:
    labels = []

    for index in range(count):
        current = index
        label = ""

        while True:
            label = chr(ord("A") + (current % 26)) + label
            current = current // 26 - 1
            if current < 0:
                break

        labels.append(label)

    return labels


def _guess_chart_type(prompt: str) -> str:
    lowered = prompt.lower()

    if "pie" in lowered or "pizza" in lowered:
        return "pie"
    if "line" in lowered or "linha" in lowered:
        return "line"
    if "bar" in lowered or "barra" in lowered:
        return "bar"
    if any(month in lowered for month in MONTH_LABELS):
        return "line"

    return "bar"


def _default_title(chart_type: str) -> str:
    return {
        "bar": "Bar chart",
        "line": "Line chart",
        "pie": "Pie chart",
    }.get(chart_type, "Chart")


def _sanitize_labels(values: list[Any]) -> list[str]:
    return [str(value).strip() for value in values if str(value).strip()]


def normalize_chart_payload(payload: dict[str, Any]) -> dict[str, Any]:
    chart_type = str(payload.get("type", "")).strip().lower()
    labels = _sanitize_labels(payload.get("labels", []))
    values = [_coerce_number(value) for value in payload.get("values", [])]
    title = str(payload.get("title", "")).strip() or _default_title(chart_type or "bar")

    return {
        "type": chart_type,
        "labels": labels,
        "values": values,
        "title": title,
    }


def validate_chart_payload(payload: dict[str, Any]) -> tuple[bool, str | None]:
    required = ("type", "labels", "values", "title")

    for key in required:
        if key not in payload:
            return False, f"Missing key: {key}"

    if payload["type"] not in SUPPORTED_CHART_TYPES:
        return False, "Chart type must be one of: bar, line or pie."

    if not isinstance(payload["labels"], list) or not payload["labels"]:
        return False, "labels must be a non-empty array."

    if not isinstance(payload["values"], list) or not payload["values"]:
        return False, "values must be a non-empty array."

    if len(payload["labels"]) != len(payload["values"]):
        return False, "labels and values must have the same length."

    if any(not isinstance(label, str) or not label.strip() for label in payload["labels"]):
        return False, "Every label must be a non-empty string."

    try:
        [_coerce_number(value) for value in payload["values"]]
    except ValueError as exc:
        return False, str(exc)

    if not str(payload["title"]).strip():
        return False, "title must be a non-empty string."

    return True, None


def _extract_data_section(prompt: str) -> str:
    lowered = prompt.lower()

    for token in ("with values", "valores", "values", "dados"):
        index = lowered.find(token)
        if index != -1:
            return prompt[index + len(token) :].strip(" :,-")

    return prompt


def _extract_pairs(section: str) -> tuple[list[str], list[float]]:
    chunk_labels: list[str] = []
    chunk_values: list[float] = []

    for chunk in re.split(r"[;\n,]+", section):
        cleaned = chunk.strip()
        if not cleaned:
            continue

        match = PAIR_CHUNK_PATTERN.match(cleaned) or SPACE_PAIR_PATTERN.match(cleaned)
        if match:
            chunk_labels.append(match.group(1).strip())
            chunk_values.append(_coerce_number(match.group(2)))

    if chunk_labels and len(chunk_labels) == len(chunk_values):
        return chunk_labels, chunk_values

    list_match = LABELS_WITH_VALUES_PATTERN.search(section)
    if list_match:
        labels = [label.strip() for label in list_match.group(1).split(",")]
        values = [_coerce_number(value) for value in list_match.group(2).split(",")]
        if len(labels) == len(values):
            return labels, values

    return [], []


def _extract_month_labels(prompt: str, expected_count: int) -> list[str]:
    matches = re.findall(r"[A-Za-z]{3,}", prompt.lower())
    labels: list[str] = []

    for match in matches:
        if match in MONTH_LABELS and match not in labels:
            labels.append(match)
        if len(labels) == expected_count:
            break

    return labels


def infer_chart_spec(prompt: str) -> ChartSpec:
    chart_type = _guess_chart_type(prompt)
    section = _extract_data_section(prompt)

    labels, values = _extract_pairs(section)

    if not values:
        values = [_coerce_number(value) for value in NUMBER_PATTERN.findall(section)]

        if values:
            month_labels = _extract_month_labels(section, len(values))
            labels = month_labels if len(month_labels) == len(values) else _default_labels(len(values))

    if not values:
        values = [1.0, 2.0, 3.0]
        labels = ["A", "B", "C"]

    if not labels:
        labels = _default_labels(len(values))

    return ChartSpec(
        chart_type=chart_type,
        labels=labels,
        values=values,
        title=_default_title(chart_type),
    )


def chart_spec_to_matplotlib_code(chart: ChartSpec) -> str:
    labels = json.dumps(chart.labels, ensure_ascii=False)
    values = json.dumps([_compact_number(value) for value in chart.values])
    title = json.dumps(chart.title, ensure_ascii=False)

    if chart.chart_type == "bar":
        body = (
            "fig, ax = plt.subplots(figsize=(8, 5))\n"
            f"ax.bar({labels}, {values}, color='#2563eb')\n"
            f"ax.set_title({title})\n"
            "ax.set_xlabel('Categories')\n"
            "ax.set_ylabel('Values')\n"
            "ax.grid(axis='y', alpha=0.25)\n"
        )
    elif chart.chart_type == "line":
        body = (
            "fig, ax = plt.subplots(figsize=(8, 5))\n"
            f"ax.plot({labels}, {values}, marker='o', linewidth=2.5, color='#0f766e')\n"
            f"ax.set_title({title})\n"
            "ax.set_xlabel('Categories')\n"
            "ax.set_ylabel('Values')\n"
            "ax.grid(alpha=0.25)\n"
        )
    else:
        body = (
            "fig, ax = plt.subplots(figsize=(7, 7))\n"
            f"ax.pie({values}, labels={labels}, autopct='%1.1f%%', startangle=90)\n"
            f"ax.set_title({title})\n"
            "ax.axis('equal')\n"
        )

    return (
        "import matplotlib.pyplot as plt\n\n"
        f"labels = {labels}\n"
        f"values = {values}\n\n"
        f"{body}"
        "plt.tight_layout()\n"
        "if output_path:\n"
        "    fig.savefig(output_path, dpi=150, bbox_inches='tight')\n"
        "else:\n"
        "    plt.show()\n"
    )


def chart_spec_to_d3_javascript(chart: ChartSpec) -> str:
    records = [
        {"label": label, "value": _compact_number(value)}
        for label, value in zip(chart.labels, chart.values)
    ]

    payload = json.dumps(
        {
            "type": chart.chart_type,
            "title": chart.title,
            "data": records,
        },
        indent=2,
        ensure_ascii=False,
    )

    return (
        "const chartPayload = "
        f"{payload};\n"
        "// Use chartPayload.type to decide whether to render a bar, line or pie chart.\n"
        "// Each item in chartPayload.data has the format { label, value }.\n"
    )
