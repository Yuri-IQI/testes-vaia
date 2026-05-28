from __future__ import annotations

import pandas as pd

from generator.column_selector import choose_color, choose_dimension, choose_metric, contains_phrase
from generator.constants import (
    BAR_HINTS, BOX_HINTS, COUNT_HINTS, HISTOGRAM_HINTS,
    LINE_HINTS, MEAN_HINTS, PIE_HINTS, SCATTER_HINTS,
)
from generator.models import VisualizationRenderOptions, VisualizationSpec
from generator.spec_resolver import _default_title, resolve_and_validate_visualization_payload


_PASSTHROUGH_TYPES = {"scatter", "histogram", "box"}


def infer_visualization_spec(frame: pd.DataFrame, prompt: str) -> VisualizationSpec:
    chart_type = _infer_chart_type(prompt)
    aggregation = None if chart_type in _PASSTHROUGH_TYPES else _infer_aggregation(prompt)
    metric = choose_metric(frame, prompt, aggregation)
    dimension = None if chart_type == "histogram" else choose_dimension(frame, prompt, chart_type, metric)
    color = choose_color(frame, prompt, chart_type, metric, dimension)
    render_options = _infer_render_options(prompt, chart_type, metric, frame)

    payload = {
        "type": chart_type,
        "data": {
            "dimension": dimension,
            "metric": metric,
            "metric_secondary": None,
            "aggregation": aggregation,
            "color": color,
        },
        "render_options": {
            "log_scale_y": render_options.log_scale_y,
            "show_trend_line": render_options.show_trend_line,
            "nbins": render_options.nbins,
            "top_n": render_options.top_n,
        },
        "title": _default_title(chart_type, aggregation, metric, dimension),
        "description": _default_description(chart_type, aggregation, metric, dimension),
        "explanation": "Fallback heuristic selected the closest valid columns from the dataset.",
    }

    normalized, error = resolve_and_validate_visualization_payload(payload, frame)
    if normalized is None:
        raise ValueError(error or "Could not infer a valid visualization spec.")

    return VisualizationSpec.from_dict(normalized)


def _infer_chart_type(prompt: str) -> str:
    if contains_phrase(prompt, PIE_HINTS):       return "pie"
    if contains_phrase(prompt, LINE_HINTS):      return "line"
    if contains_phrase(prompt, SCATTER_HINTS):   return "scatter"
    if contains_phrase(prompt, HISTOGRAM_HINTS): return "histogram"
    if contains_phrase(prompt, BOX_HINTS):       return "box"
    if contains_phrase(prompt, BAR_HINTS):       return "bar"
    return "bar"


def _infer_aggregation(prompt: str) -> str:
    if contains_phrase(prompt, MEAN_HINTS):  return "mean"
    if contains_phrase(prompt, COUNT_HINTS): return "count"
    return "sum"


def _infer_render_options(
    prompt: str,
    chart_type: str,
    metric: str,
    frame: pd.DataFrame,
) -> VisualizationRenderOptions:
    from generator.constants import LOG_SCALE_HINTS, TREND_LINE_HINTS, TOP_N_PATTERN
    import re
    from pandas.api.types import is_numeric_dtype

    log_scale_y = False
    if chart_type in {"line", "bar", "scatter"}:
        if contains_phrase(prompt, LOG_SCALE_HINTS):
            log_scale_y = True
        elif is_numeric_dtype(frame[metric]):
            col = frame[metric].dropna()
            if len(col) and col.min() > 0:
                import math
                magnitude = math.log10(col.max()) - math.log10(col.min())
                log_scale_y = magnitude >= 3

    show_trend_line = (
        chart_type == "scatter"
        and contains_phrase(prompt, TREND_LINE_HINTS)
    )

    nbins = None
    if chart_type == "histogram":
        unique = frame[metric].nunique()
        if unique <= 30:
            nbins = 20
        elif unique <= 200:
            nbins = 40
        else:
            nbins = 60

    top_n = None
    if chart_type == "bar":
        match = re.search(TOP_N_PATTERN, prompt, re.IGNORECASE)
        if match:
            top_n = int(match.group(1))

    return VisualizationRenderOptions(
        log_scale_y=log_scale_y,
        show_trend_line=show_trend_line,
        nbins=nbins,
        top_n=top_n,
    )


def _default_description(
    chart_type: str,
    aggregation: str | None,
    metric: str,
    dimension: str | None,
) -> str:
    if chart_type == "histogram":
        return f"Distribution of {metric} values across the dataset."
    if chart_type == "box":
        return f"Spread and outliers of {metric} grouped by {dimension}."
    if chart_type == "scatter":
        return f"Relationship between {dimension} and {metric}."
    return f"Shows {aggregation} of {metric} grouped by {dimension}."