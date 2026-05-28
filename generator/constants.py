import re

SUPPORTED_CHART_TYPES = ("bar", "line", "pie", "scatter", "histogram", "box")
SUPPORTED_AGGREGATIONS = ("sum", "mean", "count")
DATE_COLUMN_HINTS   = ("date", "time", "month", "year", "quarter", "day")
METRIC_COLUMN_HINTS = ("sales", "revenue", "amount", "price", "value", "profit", "quantity", "total")
LINE_HINTS  = ("line chart", "line graph", "line plot", "trend", "over time", "time series", "timeline", "monthly", "daily", "evolution")
PIE_HINTS   = ("pie chart", "pizza", "sector chart", "share of total", "percentage share")
BAR_HINTS   = ("bar chart", "bar graph", "bars", "column chart", "column graph", "compare", "comparison")
SCATTER_HINTS = ("scatter", "correlation", "vs", "versus", "relationship between", "compared to")
HISTOGRAM_HINTS = ("histogram", "distribution", "frequency", "how spread", "spread of")
BOX_HINTS = ("box plot", "boxplot", "box chart", "outliers", "quartile", "spread by", "variance by")
MEAN_HINTS  = ("average", "mean", "avg", "media", "média")
COUNT_HINTS = ("count", "number of", "how many", "frequency", "quantidade de")
COLOR_HINTS = ("split by", "grouped by", "group by", "grouping by", "colored by", "breakdown by", "segmented by", "composition of")
LOG_SCALE_HINTS  = ("log scale", "logarithmic", "log axis", "orders of magnitude")
TREND_LINE_HINTS = ("correlation", "trend", "relationship", "linear", "regression")
TOP_N_PATTERN    = r"\btop\s+(\d+)\b|\bbest\s+(\d+)\b|\bhighest\s+(\d+)\b|\bworst\s+(\d+)\b"

def normalize_text(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", value.lower()).strip()

def compact_text(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "", value.lower())

def contains_phrase(text: str, phrases: tuple[str, ...]) -> bool:
    lowered = text.lower()
    return any(re.search(rf"\b{re.escape(phrase)}\b", lowered) for phrase in phrases)