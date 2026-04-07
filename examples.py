CHART_EXAMPLES = [
    {
        "request": "bar chart with values sales: 12, support: 7, product: 15",
        "response": {
            "type": "bar",
            "labels": ["sales", "support", "product"],
            "values": [12, 7, 15],
            "title": "Bar chart",
        },
    },
    {
        "request": "line chart with values jan: 5, feb: 8, mar: 13",
        "response": {
            "type": "line",
            "labels": ["jan", "feb", "mar"],
            "values": [5, 8, 13],
            "title": "Line chart",
        },
    },
    {
        "request": "pie chart with values cats: 4, dogs: 6, birds: 2",
        "response": {
            "type": "pie",
            "labels": ["cats", "dogs", "birds"],
            "values": [4, 6, 2],
            "title": "Pie chart",
        },
    },
]


def build_examples_block() -> str:
    lines = []

    for example in CHART_EXAMPLES:
        lines.append(f"Input: {example['request']}")
        lines.append(f"Output: {example['response']}")
        lines.append("")

    return "\n".join(lines).strip()
