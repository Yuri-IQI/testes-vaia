from __future__ import annotations

import json


VISUALIZATION_EXAMPLES = [
    {
        "request": "Compare total sales by country in a bar chart and split the bars by product line.",
        "response": {
            "type": "bar",
            "data": {
                "dimension": "COUNTRY",
                "metric": "SALES",
                "aggregation": "sum",
                "color": "PRODUCTLINE",
            },
            "title": "Total sales by country and product line",
            "description": "Compares total sales across countries while separating each product line.",
            "explanation": "A bar chart works well for category comparisons, and color separates product lines within each country.",
        },
    },
    {
        "request": "Show the sales trend over time in a line chart.",
        "response": {
            "type": "line",
            "data": {
                "dimension": "ORDERDATE",
                "metric": "SALES",
                "aggregation": "sum",
            },
            "title": "Sales trend over time",
            "description": "Shows how total sales evolve over time.",
            "explanation": "A line chart is appropriate for time-based trends using the existing date and sales columns.",
        },
    },
    {
        "request": "Show how each product line contributes to total sales in a pie chart.",
        "response": {
            "type": "pie",
            "data": {
                "dimension": "PRODUCTLINE",
                "metric": "SALES",
                "aggregation": "sum",
            },
            "title": "Sales share by product line",
            "description": "Displays the proportion of total sales for each product line.",
            "explanation": "A pie chart emphasizes part-to-whole composition when grouping sales by product line.",
        },
    },
]


def build_examples_block() -> str:
    lines: list[str] = []

    for example in VISUALIZATION_EXAMPLES:
        lines.append(f"User request: {example['request']}")
        lines.append("JSON response:")
        lines.append(json.dumps(example["response"], indent=2, ensure_ascii=False))
        lines.append("")

    return "\n".join(lines).strip()
