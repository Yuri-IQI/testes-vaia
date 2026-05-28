import json

from examples import build_few_shots_block


def build_prompt(summary: dict[str, object], user_prompt: str, feedback: str) -> str:
    blocks = [
        "Dataset summary:",
        json.dumps(summary, indent=2, ensure_ascii=False),
        "",
        "Examples:",
            build_few_shots_block(),
        "",
        f'User request: "{user_prompt}"',
        "Return a visualization specification JSON using only dataset columns from the summary.",
    ]

    if feedback:
        blocks.extend(
            [
                "",
                "Fix the previous problem before answering again.",
                f"Previous validation error: {feedback}",
            ]
        )

    return "\n".join(blocks).strip()