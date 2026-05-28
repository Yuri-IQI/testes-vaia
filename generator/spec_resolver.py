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
    metric = _clean_optional_string(data.get("metric"))
    metric_secondary = _clean_optional_string(data.get("metric_secondary"))

    aggregation = _clean_optional_string(data.get("aggregation"))
    if aggregation:
        aggregation = aggregation.lower()

    color = _clean_optional_string(data.get("color"))

    filters = _normalize_filters(data.get("filters"))

    title = _clean_optional_string(payload.get("title")) or ""
    description = _clean_optional_string(payload.get("description")) or ""
    explanation = _clean_optional_string(payload.get("explanation")) or ""

    raw_options = payload.get("render_options")
    render_options = raw_options if isinstance(raw_options, dict) else {}

    return {
        "type": chart_type,
        "data": {
            "dimension": dimension,
            "metric": metric,
            "metric_secondary": metric_secondary,
            "aggregation": aggregation,
            "color": color,
            "filters": filters,
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
        return None, (
            f"Chart type must be one of: "
            f"{', '.join(SUPPORTED_CHART_TYPES)}."
        )

    dimension = None

    if chart_type != "histogram":
        dimension = _resolve_column_name(
            normalized["data"]["dimension"] or "",
            columns,
        )

        if not dimension:
            return None, (
                f"Invalid dimension column: "
                f"{normalized['data']['dimension']}"
            )

    metric = _resolve_column_name(
        normalized["data"]["metric"] or "",
        columns,
    )

    if not metric:
        return None, (
            f"Invalid metric column: "
            f"{normalized['data']['metric']}"
        )

    if chart_type in {"bar", "line", "pie"}:
        if aggregation not in SUPPORTED_AGGREGATIONS:
            return None, (
                f"Aggregation must be one of: "
                f"{', '.join(SUPPORTED_AGGREGATIONS)}."
            )
    else:
        aggregation = None

    color = normalized["data"]["color"]

    resolved_color = None

    if color:
        if chart_type in {"pie", "histogram"}:
            return None, (
                f"{chart_type.title()} charts "
                f"do not support the color field."
            )

        resolved_color = _resolve_column_name(color, columns)

        if not resolved_color:
            return None, f"Invalid color column: {color}"

    if dimension and dimension == metric:
        return None, (
            "dimension and metric must be different columns."
        )

    if resolved_color and resolved_color in {dimension, metric}:
        return None, (
            "color must be different from dimension and metric."
        )

    if aggregation in {"sum", "mean"}:
        if not is_numeric_dtype(frame[metric]):
            return None, (
                f"Metric must be numeric "
                f"for aggregation '{aggregation}'."
            )

    if chart_type == "pie" and not dimension:
        return None, "Pie charts require a dimension column."

    metric_secondary = None

    if chart_type == "scatter":
        raw_sec = normalized["data"].get("metric_secondary")

        if not raw_sec:
            return None, (
                "Scatter charts require a "
                "metric_secondary column."
            )

        metric_secondary = _resolve_column_name(
            raw_sec,
            columns,
        )

        if not metric_secondary:
            return None, (
                f"Invalid metric_secondary column: {raw_sec}"
            )

        if not is_numeric_dtype(frame[metric_secondary]):
            return None, (
                "metric_secondary must be numeric "
                "for scatter charts."
            )

    resolved_filters, filter_error = _resolve_filters(
        normalized["data"]["filters"],
        frame,
    )

    if filter_error:
        return None, filter_error

    normalized["data"]["dimension"] = dimension
    normalized["data"]["metric"] = metric
    normalized["data"]["metric_secondary"] = metric_secondary
    normalized["data"]["aggregation"] = aggregation
    normalized["data"]["color"] = resolved_color
    normalized["data"]["filters"] = resolved_filters

    if not normalized["title"]:
        normalized["title"] = _default_title(
            chart_type,
            aggregation,
            metric,
            dimension,
        )

    if not normalized["description"]:
        normalized["description"] = _default_title(
            chart_type,
            aggregation,
            metric,
            dimension,
        )

    if not normalized["explanation"]:
        normalized["explanation"] = (
            f"The {chart_type} chart matches the requested "
            f"comparison using existing dataset columns."
        )

    return normalized, None

def _normalize_filters(value: Any) -> dict[str, list[str]]:
    if not isinstance(value, dict):
        return {}

    normalized_filters: dict[str, list[str]] = {}

    for key, values in value.items():
        clean_key = _clean_optional_string(key)

        if not clean_key:
            continue

        if isinstance(values, list):
            clean_values = [
                str(v).strip()
                for v in values
                if _clean_optional_string(v)
            ]
        else:
            clean_value = _clean_optional_string(values)
            clean_values = [clean_value] if clean_value else []

        if clean_values:
            normalized_filters[clean_key] = clean_values

    return normalized_filters


def _resolve_filters(
    filters: dict[str, list[str]],
    frame: pd.DataFrame,
) -> tuple[dict[str, list[str]], str | None]:

    resolved_filters: dict[str, list[str]] = {}

    columns = list(frame.columns)

    for raw_column, raw_values in filters.items():

        resolved_column = _resolve_column_name(
            raw_column,
            columns,
        )

        if not resolved_column:
            return None, (
                f"Invalid filter column: {raw_column}"
            )

        series = frame[resolved_column].astype(str)

        existing_values = {
            normalize_text(v)
            for v in series.dropna().unique()
        }

        resolved_values: list[str] = []

        for value in raw_values:
            normalized_value = normalize_text(value)

            if normalized_value not in existing_values:
                return None, (
                    f"Invalid filter value '{value}' "
                    f"for column '{resolved_column}'."
                )

            resolved_values.append(value)

        resolved_filters[resolved_column] = resolved_values

    return resolved_filters, None

def _resolve_column_name( requested: str, columns: list[str], ) -> str | None: 
    if requested in columns: 
        return requested 
    
    compact_requested = compact_text(requested) 
    normalized_requested = normalize_text(requested) 
    
    if not compact_requested and not normalized_requested: 
        return None 
    
    compact_matches = [ column for column in columns if compact_text(column) == compact_requested ] 
    if len(compact_matches) == 1: 
        return compact_matches[0] 
    
    normalized_matches = [ column for column in columns if normalize_text(column) == normalized_requested ] 
    if len(normalized_matches) == 1: 
        return normalized_matches[0] 
    
    contains_matches = [ column for column in columns if compact_requested and compact_requested in compact_text(column) ] 
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
