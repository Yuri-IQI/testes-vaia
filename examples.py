from __future__ import annotations

import json


VISUALIZATION_EXAMPLES = [
    {
        "request": "Show how crude oil prices evolved over time.",
        "response": {
            "type": "line",
            "data": {
                "dimension": "Date",
                "metric": "Crude Oil Price (USD per Barrel)",
                "aggregation": "mean",
                "color": None,
            },
            "title": "Crude oil price evolution over time",
            "description": "Tracks the mean crude oil price across the full dataset timeline.",
            "explanation": "A line chart is the natural choice for a single numeric indicator evolving over a datetime dimension.",
        },
    },
    {
        "request": "Compare average consumer spending by stock index.",
        "response": {
            "type": "bar",
            "data": {
                "dimension": "Stock Index",
                "metric": "Consumer Spending (Billion USD)",
                "aggregation": "mean",
                "color": None,
            },
            "title": "Average consumer spending by stock index",
            "description": "Compares mean consumer spending levels across stock indexes.",
            "explanation": "A bar chart with mean aggregation is the standard choice for comparing a numeric metric across a categorical dimension.",
        },
    },
    {
        "request": "Show the share of total retail sales by stock index.",
        "response": {
            "type": "pie",
            "data": {
                "dimension": "Stock Index",
                "metric": "Retail Sales (Billion USD)",
                "aggregation": "sum",
                "color": None,
            },
            "title": "Share of total retail sales by stock index",
            "description": "Shows each stock index's proportional contribution to total retail sales.",
            "explanation": "Pie charts communicate part-of-whole relationships for low-cardinality categorical dimensions.",
        },
    }
]


def build_examples_block() -> str:
    lines: list[str] = []

    for example in VISUALIZATION_EXAMPLES:
        lines.append(f"User request: {example['request']}")
        lines.append("JSON response:")
        lines.append(json.dumps(example["response"], indent=2, ensure_ascii=False))
        lines.append("")

    return "\n".join(lines).strip()
