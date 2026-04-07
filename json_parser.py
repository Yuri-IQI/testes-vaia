from __future__ import annotations

import json
from typing import Any


def extract_json(text: str) -> str | None:
    start = text.find("{")

    while start != -1:
        depth = 0
        in_string = False
        escaping = False

        for index in range(start, len(text)):
            char = text[index]

            if in_string:
                if escaping:
                    escaping = False
                elif char == "\\":
                    escaping = True
                elif char == '"':
                    in_string = False
                continue

            if char == '"':
                in_string = True
            elif char == "{":
                depth += 1
            elif char == "}":
                depth -= 1

                if depth == 0:
                    candidate = text[start : index + 1]
                    try:
                        json.loads(candidate)
                        return candidate
                    except json.JSONDecodeError:
                        break

        start = text.find("{", start + 1)

    return None


def parse_json(response: str) -> dict[str, Any] | None:
    try:
        return json.loads(response)
    except json.JSONDecodeError as exc:
        print(f"Error parsing JSON: {exc}")
        return None
