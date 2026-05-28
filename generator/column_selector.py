import re

import pandas as pd

from generator.constants import COLOR_HINTS, DATE_COLUMN_HINTS, METRIC_COLUMN_HINTS, compact_text, contains_phrase, normalize_text
from generator.dataset import get_column_groups

def _column_score(prompt: str, column: str) -> int:
    prompt_compact = compact_text(prompt)
    prompt_tokens = set(normalize_text(prompt).split())
    column_compact = compact_text(column)
    column_tokens = set(normalize_text(column).split())

    score = 0
    if column_compact and column_compact in prompt_compact:
        score += 100

    score += 15 * len(column_tokens & prompt_tokens)

    return score

def _find_explicit_mentions(prompt: str, columns: list[str]) -> list[str]:
    compact_prompt = compact_text(prompt)
    matches: list[tuple[int, str]] = []

    for column in columns:
        compact_column = compact_text(column)
        index = compact_prompt.find(compact_column)
        if compact_column and index != -1:
            matches.append((index, column))

    matches.sort(key=lambda item: item[0])
    return [column for _, column in matches]

def _preferred_metric_columns(columns: list[str]) -> list[str]:
    scored = []

    for column in columns:
        bonus = 0
        normalized = normalize_text(column)
        if any(token in normalized for token in METRIC_COLUMN_HINTS):
            bonus += 20
        if "id" in normalized:
            bonus -= 10
        scored.append((bonus, column))

    scored.sort(key=lambda item: item[0], reverse=True)
    return [column for _, column in scored]


def choose_metric(frame: pd.DataFrame, prompt: str, aggregation: str) -> str:
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

def choose_dimension(frame: pd.DataFrame, prompt: str, chart_type: str, metric: str) -> str:
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

def _date_like_candidates(frame: pd.DataFrame) -> list[str]:
    groups = get_column_groups(frame)
    candidates = groups["datetime"][:]

    for column in frame.columns:
        normalized = normalize_text(column)
        if any(token in normalized for token in DATE_COLUMN_HINTS) and column not in candidates:
            candidates.append(column)

    return candidates

def choose_color(frame: pd.DataFrame, prompt: str, chart_type: str, metric: str, dimension: str) -> str | None:
    if chart_type == "pie":
        return None

    groups = get_column_groups(frame)
    explicit = [
        column
        for column in _find_explicit_mentions(prompt, groups["categorical"])
        if column not in {metric, dimension}
    ]

    if explicit and contains_phrase(prompt, COLOR_HINTS):
        return explicit[0]

    if len(explicit) >= 2:
        return explicit[1]

    return None