#!/usr/bin/env python3
"""Build a stable, deduplicated review queue from the extracted question bank."""

from __future__ import annotations

import json
import re
import unicodedata
from collections import defaultdict
from pathlib import Path


def normalize(text: str) -> str:
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode()
    return re.sub(r"\W+", " ", text.lower()).strip()


def main() -> None:
    bank_path = Path("web/data/questions.json")
    review_path = Path("data/answer-review.json")
    questions = json.loads(bank_path.read_text(encoding="utf-8"))["questions"]
    groups: dict[str, list[dict]] = defaultdict(list)
    for question in questions:
        signature = normalize(question["prompt"])
        groups[signature].append(question)

    existing = {}
    if review_path.exists():
        existing = {
            item["signature"]: item
            for item in json.loads(review_path.read_text(encoding="utf-8"))["items"]
        }

    items = []
    for signature, variants in sorted(groups.items()):
        first = variants[0]
        prior = existing.get(signature, {})
        items.append(
            {
                "signature": signature,
                "prompt": first["prompt"],
                "variants": [
                    {
                        "id": variant["id"],
                        "source": variant["source"],
                        "number": variant["number"],
                        "options": variant["options"],
                    }
                    for variant in variants
                ],
                "answer": prior.get("answer"),
                "variantAnswers": prior.get("variantAnswers", {}),
                "status": prior.get("status", "pending"),
                "confidence": prior.get("confidence"),
                "sourceUrl": prior.get("sourceUrl"),
                "sourceDetail": prior.get("sourceDetail"),
                "reviewedAt": prior.get("reviewedAt"),
                "notes": prior.get("notes"),
            }
        )

    review_path.parent.mkdir(parents=True, exist_ok=True)
    review_path.write_text(
        json.dumps({"items": items}, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(f"Cola de revisión: {len(items)} enunciados únicos para {len(questions)} preguntas.")


if __name__ == "__main__":
    main()
