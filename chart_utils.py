from __future__ import annotations

import io
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, BinaryIO

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pandas.api.types import is_bool_dtype, is_datetime64_any_dtype, is_numeric_dtype


SUPPORTED_CHART_TYPES = ("bar", "line", "pie")
SUPPORTED_AGGREGATIONS = ("sum", "mean", "count")
DATE_COLUMN_HINTS = ("date", "time", "month", "year", "quarter", "day")
METRIC_COLUMN_HINTS = ("sales", "revenue", "amount", "price", "value", "profit", "quantity", "total")
LINE_HINTS = ("line chart", "line graph", "line plot", "trend", "over time", "time series", "timeline", "monthly", "daily", "evolution")
PIE_HINTS = ("pie chart", "pizza", "sector chart", "share of total", "percentage share")
BAR_HINTS = ("bar chart", "bar graph", "bars", "column chart", "column graph", "compare", "comparison")
MEAN_HINTS = ("average", "mean", "avg", "media", "média")
COUNT_HINTS = ("count", "number of", "how many", "frequency", "quantidade de")
COLOR_HINTS = ("split by", "grouped by", "group by", "grouping by", "colored by", "breakdown by", "segmented by", "composition of")


@dataclass
class VisualizationDataSpec:
    dimension: str
    metric: str
    aggregation: str
    color: str | None = None

    def to_dict(self) -> dict[str, Any]:
        payload = {
            "dimension": self.dimension,
            "metric": self.metric,
            "aggregation": self.aggregation,
        }

        if self.color:
            payload["color"] = self.color

        return payload


@dataclass
class VisualizationSpec:
    chart_type: str
    data: VisualizationDataSpec
    title: str
    description: str
    explanation: str

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> "VisualizationSpec":
        data = payload["data"]
        return cls(
            chart_type=payload["type"],
            data=VisualizationDataSpec(
                dimension=data["dimension"],
                metric=data["metric"],
                aggregation=data["aggregation"],
                color=data.get("color"),
            ),
            title=payload["title"],
            description=payload["description"],
            explanation=payload["explanation"],
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "type": self.chart_type,
            "data": self.data.to_dict(),
            "title": self.title,
            "description": self.description,
            "explanation": self.explanation,
        }


def _normalize_text(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", value.lower()).strip()


def _compact_text(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "", value.lower())


def _contains_phrase(text: str, phrases: tuple[str, ...]) -> bool:
    lowered = text.lower()
    return any(re.search(rf"\b{re.escape(phrase)}\b", lowered) for phrase in phrases)


def _clean_optional_string(value: Any) -> str | None:
    if value is None:
        return None

    cleaned = str(value).strip()
    if not cleaned or cleaned.lower() == "none":
        return None

    return cleaned


def _safe_value(value: Any) -> Any:
    if pd.isna(value):
        return None

    if isinstance(value, pd.Timestamp):
        return value.isoformat()

    if hasattr(value, "item"):
        try:
            value = value.item()
        except Exception:
            pass

    return value


def _dataframe_to_records(frame: pd.DataFrame) -> list[dict[str, Any]]:
    records = frame.to_dict(orient="records")
    safe_records: list[dict[str, Any]] = []

    for row in records:
        safe_records.append({key: _safe_value(value) for key, value in row.items()})

    return safe_records


def _read_csv(source: str | Path | bytes | BinaryIO, encoding: str) -> pd.DataFrame:
    if isinstance(source, (str, Path)):
        return pd.read_csv(source, encoding=encoding, sep=None, engine="python")

    if isinstance(source, bytes):
        buffer = io.BytesIO(source)
        return pd.read_csv(buffer, encoding=encoding, sep=None, engine="python")

    if hasattr(source, "seek"):
        source.seek(0)

    return pd.read_csv(source, encoding=encoding, sep=None, engine="python")


def _coerce_datetime_columns(frame: pd.DataFrame) -> pd.DataFrame:
    converted = frame.copy()

    for column in converted.columns:
        series = converted[column]

        if is_datetime64_any_dtype(series) or is_numeric_dtype(series) or is_bool_dtype(series):
            continue

        normalized_name = _normalize_text(str(column))
        if not any(token in normalized_name for token in DATE_COLUMN_HINTS):
            continue

        parsed = pd.to_datetime(series, errors="coerce")
        parse_ratio = float(parsed.notna().mean()) if len(parsed) else 0.0

        if parse_ratio >= 0.8:
            converted[column] = parsed

    return converted


def load_csv_dataset(source: str | Path | bytes | BinaryIO) -> pd.DataFrame:
    last_error: Exception | None = None

    for encoding in ("utf-8", "utf-8-sig", "latin1"):
        try:
            frame = _read_csv(source, encoding=encoding)
            if frame.empty:
                raise ValueError("The dataset is empty.")

            frame.columns = [str(column).strip() for column in frame.columns]
            return _coerce_datetime_columns(frame)
        except Exception as exc:
            last_error = exc

    raise ValueError("Could not read the CSV dataset. Check the file format and encoding.") from last_error


def _classify_column(series: pd.Series) -> str:
    if is_datetime64_any_dtype(series):
        return "datetime"
    if is_numeric_dtype(series) and not is_bool_dtype(series):
        return "numeric"
    return "categorical"


def get_column_groups(frame: pd.DataFrame) -> dict[str, list[str]]:
    numeric: list[str] = []
    categorical: list[str] = []
    datetime_columns: list[str] = []

    for column in frame.columns:
        column_type = _classify_column(frame[column])
        if column_type == "numeric":
            numeric.append(column)
        elif column_type == "datetime":
            datetime_columns.append(column)
        else:
            categorical.append(column)

    return {
        "numeric": numeric,
        "categorical": categorical,
        "datetime": datetime_columns,
    }


def summarize_dataframe(frame: pd.DataFrame, max_rows: int = 5, max_values: int = 4) -> dict[str, Any]:
    groups = get_column_groups(frame)
    columns_summary: list[dict[str, Any]] = []

    for column in frame.columns:
        series = frame[column]
        semantic_type = _classify_column(series)
        non_null = series.dropna()
        column_summary = {
            "name": column,
            "dtype": str(series.dtype),
            "semantic_type": semantic_type,
            "non_null": int(series.notna().sum()),
            "unique_values": int(series.nunique(dropna=True)),
            "sample_values": [_safe_value(value) for value in non_null.head(max_values).tolist()],
        }

        if semantic_type == "numeric" and not non_null.empty:
            column_summary["min"] = _safe_value(non_null.min())
            column_summary["max"] = _safe_value(non_null.max())

        columns_summary.append(column_summary)

    return {
        "row_count": int(len(frame)),
        "column_count": int(len(frame.columns)),
        "numeric_columns": groups["numeric"],
        "categorical_columns": groups["categorical"],
        "datetime_columns": groups["datetime"],
        "columns": columns_summary,
        "sample_rows": _dataframe_to_records(frame.head(max_rows)),
    }


def _resolve_column_name(requested: str, columns: list[str]) -> str | None:
    if requested in columns:
        return requested

    compact_requested = _compact_text(requested)
    normalized_requested = _normalize_text(requested)

    if not compact_requested and not normalized_requested:
        return None

    compact_matches = [column for column in columns if _compact_text(column) == compact_requested]
    if len(compact_matches) == 1:
        return compact_matches[0]

    normalized_matches = [column for column in columns if _normalize_text(column) == normalized_requested]
    if len(normalized_matches) == 1:
        return normalized_matches[0]

    contains_matches = [column for column in columns if compact_requested and compact_requested in _compact_text(column)]
    if len(contains_matches) == 1:
        return contains_matches[0]

    return None


def _default_title(chart_type: str, aggregation: str, metric: str, dimension: str) -> str:
    return f"{aggregation.title()} of {metric} by {dimension} ({chart_type.title()})"


def normalize_visualization_payload(payload: dict[str, Any]) -> dict[str, Any]:
    data = payload.get("data", {})
    if not isinstance(data, dict):
        data = {}

    chart_type = str(payload.get("type", "")).strip().lower()
    dimension = str(data.get("dimension", "")).strip()
    metric = str(data.get("metric", "")).strip()
    aggregation = str(data.get("aggregation", "sum")).strip().lower() or "sum"
    color = _clean_optional_string(data.get("color"))
    title = _clean_optional_string(payload.get("title")) or ""
    description = _clean_optional_string(payload.get("description")) or ""
    explanation = _clean_optional_string(payload.get("explanation")) or ""

    return {
        "type": chart_type,
        "data": {
            "dimension": dimension,
            "metric": metric,
            "aggregation": aggregation,
            "color": color,
        },
        "title": title,
        "description": description,
        "explanation": explanation,
    }


def resolve_and_validate_visualization_payload(
    payload: dict[str, Any],
    frame: pd.DataFrame,
) -> tuple[dict[str, Any] | None, str | None]:
    normalized = normalize_visualization_payload(payload)
    columns = list(frame.columns)

    if normalized["type"] not in SUPPORTED_CHART_TYPES:
        return None, "Chart type must be one of: bar, line or pie."

    dimension = _resolve_column_name(normalized["data"]["dimension"], columns)
    if not dimension:
        return None, f"Invalid dimension column: {normalized['data']['dimension']}"

    metric = _resolve_column_name(normalized["data"]["metric"], columns)
    if not metric:
        return None, f"Invalid metric column: {normalized['data']['metric']}"

    aggregation = normalized["data"]["aggregation"]
    if aggregation not in SUPPORTED_AGGREGATIONS:
        return None, "Aggregation must be one of: sum, mean or count."

    color = normalized["data"]["color"]
    resolved_color = None
    if color:
        resolved_color = _resolve_column_name(color, columns)
        if not resolved_color:
            return None, f"Invalid color column: {color}"

    if dimension == metric:
        return None, "dimension and metric must be different columns."

    if resolved_color and resolved_color in {dimension, metric}:
        return None, "color must be different from dimension and metric."

    metric_series = frame[metric]
    if aggregation in {"sum", "mean"} and not is_numeric_dtype(metric_series):
        return None, f"Metric must be numeric for aggregation '{aggregation}'."

    if normalized["type"] == "pie" and resolved_color:
        return None, "Pie charts do not support the color field."

    normalized["data"]["dimension"] = dimension
    normalized["data"]["metric"] = metric
    normalized["data"]["color"] = resolved_color

    if not normalized["title"]:
        normalized["title"] = _default_title(normalized["type"], aggregation, metric, dimension)

    if not normalized["description"]:
        normalized["description"] = f"Shows {aggregation} of {metric} grouped by {dimension}."

    if not normalized["explanation"]:
        normalized["explanation"] = (
            f"The {normalized['type']} chart matches the requested comparison using existing dataset columns."
        )

    return normalized, None


def aggregate_for_visualization(frame: pd.DataFrame, spec: VisualizationSpec) -> pd.DataFrame:
    dimension = spec.data.dimension
    metric = spec.data.metric
    color = spec.data.color
    aggregation = spec.data.aggregation

    selected_columns = [dimension, metric]
    if color:
        selected_columns.append(color)

    plot_frame = frame[selected_columns].copy()
    group_columns = [dimension]
    if color:
        group_columns.append(color)

    if aggregation == "sum":
        plot_frame = plot_frame.groupby(group_columns, dropna=False)[metric].sum().reset_index()
    elif aggregation == "mean":
        plot_frame = plot_frame.groupby(group_columns, dropna=False)[metric].mean().reset_index()
    else:
        plot_frame = plot_frame.groupby(group_columns, dropna=False)[metric].count().reset_index()

    if is_datetime64_any_dtype(plot_frame[dimension]) or is_numeric_dtype(plot_frame[dimension]):
        plot_frame = plot_frame.sort_values(dimension)
    elif spec.chart_type == "pie":
        plot_frame = plot_frame.sort_values(metric, ascending=False)

    return plot_frame.reset_index(drop=True)


def build_plotly_figure(plot_frame: pd.DataFrame, spec: VisualizationSpec) -> go.Figure:
    dimension = spec.data.dimension
    metric = spec.data.metric
    color = spec.data.color

    if spec.chart_type == "bar":
        figure = px.bar(
            plot_frame,
            x=dimension,
            y=metric,
            color=color,
            barmode="group",
            title=spec.title,
        )
    elif spec.chart_type == "line":
        figure = px.line(
            plot_frame,
            x=dimension,
            y=metric,
            color=color,
            markers=True,
            title=spec.title,
        )
    else:
        figure = px.pie(
            plot_frame,
            names=dimension,
            values=metric,
            title=spec.title,
            hole=0.25,
        )

    figure.update_layout(template="plotly_white", margin={"l": 24, "r": 24, "t": 60, "b": 24})
    return figure


def build_matplotlib_figure(plot_frame: pd.DataFrame, spec: VisualizationSpec):
    import matplotlib.pyplot as plt

    dimension = spec.data.dimension
    metric = spec.data.metric
    color = spec.data.color

    fig, ax = plt.subplots(figsize=(10, 6))

    if spec.chart_type == "bar":
        if color:
            pivot = plot_frame.pivot(index=dimension, columns=color, values=metric).fillna(0)
            pivot.plot(kind="bar", ax=ax)
            ax.legend(title=color)
        else:
            ax.bar(plot_frame[dimension].astype(str), plot_frame[metric], color="#2563eb")
    elif spec.chart_type == "line":
        if color:
            for group_name, group in plot_frame.groupby(color):
                group = group.sort_values(dimension)
                ax.plot(group[dimension], group[metric], marker="o", linewidth=2.2, label=str(group_name))
            ax.legend(title=color)
        else:
            ax.plot(plot_frame[dimension], plot_frame[metric], marker="o", linewidth=2.4, color="#0f766e")
    else:
        ax.pie(plot_frame[metric], labels=plot_frame[dimension].astype(str), autopct="%1.1f%%", startangle=90)
        ax.axis("equal")

    ax.set_title(spec.title)
    if spec.chart_type in {"bar", "line"}:
        ax.set_xlabel(dimension)
        ax.set_ylabel(metric)
        ax.grid(alpha=0.25, axis="y")

    if spec.chart_type == "line" and is_datetime64_any_dtype(plot_frame[dimension]):
        fig.autofmt_xdate()

    plt.tight_layout()
    return fig


def build_frontend_records(plot_frame: pd.DataFrame) -> list[dict[str, Any]]:
    return _dataframe_to_records(plot_frame)


def _infer_chart_type(prompt: str) -> str:
    if _contains_phrase(prompt, PIE_HINTS):
        return "pie"
    if _contains_phrase(prompt, LINE_HINTS):
        return "line"
    if _contains_phrase(prompt, BAR_HINTS):
        return "bar"

    return "bar"


def _infer_aggregation(prompt: str) -> str:
    if _contains_phrase(prompt, MEAN_HINTS):
        return "mean"
    if _contains_phrase(prompt, COUNT_HINTS):
        return "count"

    return "sum"


def _column_score(prompt: str, column: str) -> int:
    prompt_compact = _compact_text(prompt)
    prompt_tokens = set(_normalize_text(prompt).split())
    column_compact = _compact_text(column)
    column_tokens = set(_normalize_text(column).split())

    score = 0
    if column_compact and column_compact in prompt_compact:
        score += 100

    score += 15 * len(column_tokens & prompt_tokens)

    return score


def _find_explicit_mentions(prompt: str, columns: list[str]) -> list[str]:
    compact_prompt = _compact_text(prompt)
    matches: list[tuple[int, str]] = []

    for column in columns:
        compact_column = _compact_text(column)
        index = compact_prompt.find(compact_column)
        if compact_column and index != -1:
            matches.append((index, column))

    matches.sort(key=lambda item: item[0])
    return [column for _, column in matches]


def _preferred_metric_columns(columns: list[str]) -> list[str]:
    scored = []

    for column in columns:
        bonus = 0
        normalized = _normalize_text(column)
        if any(token in normalized for token in METRIC_COLUMN_HINTS):
            bonus += 20
        if "id" in normalized:
            bonus -= 10
        scored.append((bonus, column))

    scored.sort(key=lambda item: item[0], reverse=True)
    return [column for _, column in scored]


def _choose_metric(frame: pd.DataFrame, prompt: str, aggregation: str) -> str:
    groups = get_column_groups(frame)
    candidates = groups["numeric"][:]

    if aggregation == "count" and not candidates:
        candidates = [column for column in frame.columns if column not in groups["datetime"]]

    mentioned = _find_explicit_mentions(prompt, candidates)
    if mentioned:
        return max(mentioned, key=lambda column: _column_score(prompt, column))

    preferred = _preferred_metric_columns(candidates)
    if preferred:
        best_score = max(_column_score(prompt, column) for column in preferred)
        if best_score > 0:
            return max(preferred, key=lambda column: _column_score(prompt, column))
        return preferred[0]

    return frame.columns[0]


def _date_like_candidates(frame: pd.DataFrame) -> list[str]:
    groups = get_column_groups(frame)
    candidates = groups["datetime"][:]

    for column in frame.columns:
        normalized = _normalize_text(column)
        if any(token in normalized for token in DATE_COLUMN_HINTS) and column not in candidates:
            candidates.append(column)

    return candidates


def _choose_dimension(frame: pd.DataFrame, prompt: str, chart_type: str, metric: str) -> str:
    groups = get_column_groups(frame)
    explicit = [column for column in _find_explicit_mentions(prompt, list(frame.columns)) if column != metric]
    date_candidates = [column for column in _date_like_candidates(frame) if column != metric]
    categorical_candidates = [column for column in groups["categorical"] if column != metric]

    if chart_type == "line":
        explicit_date = [column for column in explicit if column in date_candidates]
        if explicit_date:
            return explicit_date[0]
        if explicit:
            return explicit[0]
        if date_candidates:
            return date_candidates[0]
        if categorical_candidates:
            return categorical_candidates[0]

    if explicit:
        return explicit[0]
    if categorical_candidates:
        return categorical_candidates[0]
    if date_candidates:
        return date_candidates[0]

    for column in frame.columns:
        if column != metric:
            return column

    return metric


def _choose_color(frame: pd.DataFrame, prompt: str, chart_type: str, metric: str, dimension: str) -> str | None:
    if chart_type == "pie":
        return None

    groups = get_column_groups(frame)
    explicit = [
        column
        for column in _find_explicit_mentions(prompt, groups["categorical"])
        if column not in {metric, dimension}
    ]

    if explicit and _contains_phrase(prompt, COLOR_HINTS):
        return explicit[0]

    if len(explicit) >= 2:
        return explicit[1]

    return None


def infer_visualization_spec(frame: pd.DataFrame, prompt: str) -> VisualizationSpec:
    chart_type = _infer_chart_type(prompt)
    aggregation = _infer_aggregation(prompt)
    metric = _choose_metric(frame, prompt, aggregation)
    dimension = _choose_dimension(frame, prompt, chart_type, metric)
    color = _choose_color(frame, prompt, chart_type, metric, dimension)

    payload = {
        "type": chart_type,
        "data": {
            "dimension": dimension,
            "metric": metric,
            "aggregation": aggregation,
            "color": color,
        },
        "title": _default_title(chart_type, aggregation, metric, dimension),
        "description": f"Shows {aggregation} of {metric} grouped by {dimension}.",
        "explanation": "Fallback heuristic selected the closest valid columns from the uploaded dataset.",
    }

    normalized, error = resolve_and_validate_visualization_payload(payload, frame)
    if normalized is None:
        raise ValueError(error or "Could not infer a valid visualization spec.")

    return VisualizationSpec.from_dict(normalized)
