from __future__ import annotations

from typing import Any

import pandas as pd
from pandas.api.types import is_datetime64_any_dtype, is_numeric_dtype

from generator.dataset import _dataframe_to_records
from generator.models import VisualizationSpec

def _apply_filters(frame: pd.DataFrame, filters: dict) -> pd.DataFrame:
    for column, values in filters.items():
        if column in frame.columns:
            frame = frame[frame[column].isin(values)]
    return frame

def aggregate_for_visualization(frame: pd.DataFrame, spec: VisualizationSpec) -> pd.DataFrame:
    frame = _apply_filters(frame, spec.data.filters)
    
    chart_type = spec.chart_type
    dimension = spec.data.dimension
    metric = spec.data.metric
    color = spec.data.color
    aggregation = spec.data.aggregation

    if chart_type == "scatter":
        cols = [c for c in [dimension, metric, spec.data.metric_secondary, color] if c]
        return frame[cols].dropna().reset_index(drop=True)

    if chart_type == "histogram": 
        cols = [c for c in [metric, color] if c]
        return frame[cols].dropna().reset_index(drop=True)

    if chart_type == "box":
        cols = [c for c in [dimension, metric, color] if c]
        return frame[cols].dropna().reset_index(drop=True)

    group_columns = [c for c in [dimension, color] if c]
    plot_frame = frame[group_columns + [metric]].copy()

    if aggregation == "sum":
        plot_frame = plot_frame.groupby(group_columns, dropna=False)[metric].sum().reset_index()
    elif aggregation == "mean":
        plot_frame = plot_frame.groupby(group_columns, dropna=False)[metric].mean().reset_index()
    else:
        plot_frame = plot_frame.groupby(group_columns, dropna=False)[metric].count().reset_index()

    top_n = getattr(spec.render_options, "top_n", None)
    if top_n and chart_type == "bar":
        plot_frame = plot_frame.nlargest(top_n, metric)

    if is_datetime64_any_dtype(plot_frame[dimension]) or is_numeric_dtype(plot_frame[dimension]):
        plot_frame = plot_frame.sort_values(dimension)
    elif chart_type == "pie":
        plot_frame = plot_frame.sort_values(metric, ascending=False)

    return plot_frame.reset_index(drop=True)

def build_frontend_records(plot_frame: pd.DataFrame) -> list[dict[str, Any]]:
    return _dataframe_to_records(plot_frame)