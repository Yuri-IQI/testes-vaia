from typing import Any

import pandas as pd

from pandas.api.types import is_numeric_dtype

from generator.constants import SUPPORTED_AGGREGATIONS, SUPPORTED_CHART_TYPES, compact_text, normalize_text

def normalize_visualization_payload(payload: dict[str, Any]) -> dict[str, Any]:
    data = payload.get("data", {})
    if not isinstance(data, dict):
        data = {}

    chart_type = str(payload.get("type", "")).strip().lower()
    dimension = _clean_optional_string(data.get("dimension"))
    metric = str(data.get("metric", "")).strip()
    aggregation = _clean_optional_string(data.get("aggregation"))
    if aggregation:
        aggregation = aggregation.lower()
    color = _clean_optional_string(data.get("color"))
    metric_secondary = _clean_optional_string(data.get("metric_secondary"))
    title = _clean_optional_string(payload.get("title")) or ""
    description = _clean_optional_string(payload.get("description")) or ""
    explanation = _clean_optional_string(payload.get("explanation")) or ""

    raw_options = payload.get("render_options")
    if isinstance(raw_options, dict):
        render_options = raw_options
    else:
        render_options = {}

    return {
        "type": chart_type,
        "data": {
            "dimension": dimension,
            "metric": metric,
            "metric_secondary": metric_secondary,
            "aggregation": aggregation,
            "color": color,
        },
        "render_options": render_options,
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
    chart_type = normalized["type"]
    aggregation = normalized["data"]["aggregation"]

    if chart_type not in SUPPORTED_CHART_TYPES:
        return None, f"Chart type must be one of: {', '.join(SUPPORTED_CHART_TYPES)}."

    dimension = None
    if chart_type != "histogram":
        dimension = _resolve_column_name(normalized["data"]["dimension"] or "", columns)
        if not dimension:
            return None, f"Invalid dimension column: {normalized['data']['dimension']}"

    metric = _resolve_column_name(normalized["data"]["metric"], columns)
    if not metric:
        return None, f"Invalid metric column: {normalized['data']['metric']}"

    if chart_type in {"bar", "line", "pie"}:
        if aggregation not in SUPPORTED_AGGREGATIONS:
            return None, f"Aggregation must be one of: {', '.join(SUPPORTED_AGGREGATIONS)}."
    else:
        aggregation = None

    color = normalized["data"]["color"]
    resolved_color = None
    if color:
        if chart_type in {"pie", "histogram"}:
            return None, f"{chart_type.title()} charts do not support the color field."
        resolved_color = _resolve_column_name(color, columns)
        if not resolved_color:
            return None, f"Invalid color column: {color}"

    if dimension and dimension == metric:
        return None, "dimension and metric must be different columns."

    if resolved_color and resolved_color in {dimension, metric}:
        return None, "color must be different from dimension and metric."

    if aggregation in {"sum", "mean"} and not is_numeric_dtype(frame[metric]):
        return None, f"Metric must be numeric for aggregation '{aggregation}'."

    if chart_type == "pie" and not dimension:
        return None, "Pie charts require a dimension column."

    metric_secondary = None
    if chart_type == "scatter":
        raw_sec = normalized["data"].get("metric_secondary")
        if not raw_sec:
            return None, "Scatter charts require a metric_secondary column."
        metric_secondary = _resolve_column_name(raw_sec, columns)
        if not metric_secondary:
            return None, f"Invalid metric_secondary column: {raw_sec}"
        if not is_numeric_dtype(frame[metric_secondary]):
            return None, "metric_secondary must be numeric for scatter charts."

    normalized["data"]["dimension"] = dimension
    normalized["data"]["metric"] = metric
    normalized["data"]["metric_secondary"] = metric_secondary
    normalized["data"]["aggregation"] = aggregation
    normalized["data"]["color"] = resolved_color

    if not normalized["title"]:
        normalized["title"] = _default_title(chart_type, aggregation, metric, dimension)
    if not normalized["description"]:
        normalized["description"] = _default_title(chart_type, aggregation, metric, dimension)
    if not normalized["explanation"]:
        normalized["explanation"] = (
            f"The {chart_type} chart matches the requested comparison using existing dataset columns."
        )

    return normalized, None

def _resolve_column_name(requested: str, columns: list[str]) -> str | None:
    if requested in columns:
        return requested

    compact_requested = compact_text(requested)
    normalized_requested = normalize_text(requested)

    if not compact_requested and not normalized_requested:
        return None

    compact_matches = [column for column in columns if compact_text(column) == compact_requested]
    if len(compact_matches) == 1:
        return compact_matches[0]

    normalized_matches = [column for column in columns if normalize_text(column) == normalized_requested]
    if len(normalized_matches) == 1:
        return normalized_matches[0]

    contains_matches = [column for column in columns if compact_requested and compact_requested in compact_text(column)]
    if len(contains_matches) == 1:
        return contains_matches[0]

    return None

def _clean_optional_string(value: Any) -> str | None:
    if value is None:
        return None

    cleaned = str(value).strip()
    if not cleaned or cleaned.lower() == "none":
        return None

    return cleaned

def _default_title(
    chart_type: str,
    aggregation: str | None,
    metric: str,
    dimension: str | None,
) -> str:
    if chart_type == "histogram":
        return f"Distribution of {metric} ({chart_type.title()})"
    if chart_type == "box":
        return f"Spread of {metric} by {dimension} ({chart_type.title()})"
    if chart_type == "scatter":
        return f"{metric} vs {dimension} ({chart_type.title()})"
    return f"{aggregation.title()} of {metric} by {dimension} ({chart_type.title()})"
