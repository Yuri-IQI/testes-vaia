import io
from pathlib import Path
from typing import Any, BinaryIO

import pandas as pd
from pandas.api.types import is_bool_dtype, is_datetime64_any_dtype, is_numeric_dtype

from generator.constants import DATE_COLUMN_HINTS, normalize_text

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

def _coerce_datetime_columns(frame: pd.DataFrame) -> pd.DataFrame:
    converted = frame.copy()

    for column in converted.columns:
        series = converted[column]

        if is_datetime64_any_dtype(series) or is_numeric_dtype(series) or is_bool_dtype(series):
            continue

        normalized_name = normalize_text(str(column))
        if not any(token in normalized_name for token in DATE_COLUMN_HINTS):
            continue

        parsed = pd.to_datetime(series, errors="coerce")
        parse_ratio = float(parsed.notna().mean()) if len(parsed) else 0.0

        if parse_ratio >= 0.8:
            converted[column] = parsed

    return converted

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
    
def _read_csv(source: str | Path | bytes | BinaryIO, encoding: str) -> pd.DataFrame:
    if isinstance(source, (str, Path)):
        return pd.read_csv(source, encoding=encoding, sep=None, engine="python")

    if isinstance(source, bytes):
        buffer = io.BytesIO(source)
        return pd.read_csv(buffer, encoding=encoding, sep=None, engine="python")

    if hasattr(source, "seek"):
        source.seek(0)

    return pd.read_csv(source, encoding=encoding, sep=None, engine="python")

def _classify_column(series: pd.Series) -> str:
    if is_datetime64_any_dtype(series):
        return "datetime"
    if is_numeric_dtype(series) and not is_bool_dtype(series):
        return "numeric"
    return "categorical"