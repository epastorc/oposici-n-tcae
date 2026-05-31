#!/usr/bin/env python3
"""Import manually researched answers into the auditable review queue."""

from __future__ import annotations

import json
from pathlib import Path


def main() -> None:
    review_path = Path("data/answer-review.json")
    seeds = json.loads(Path("data/legal-answer-seeds.json").read_text(encoding="utf-8"))
    review = json.loads(review_path.read_text(encoding="utf-8"))
    answers = seeds["answers"]
    updated = 0
    for item in review["items"]:
        for variant in item["variants"]:
            if variant["source"] != seeds["source"]:
                continue
            seeded = answers.get(str(variant["number"]))
            if not seeded:
                continue
            item["variantAnswers"][variant["id"]] = seeded[0]
            item["status"] = "verified"
            item["confidence"] = "high"
            item["sourceUrl"] = seeds["sourceUrl"]
            item["sourceDetail"] = seeded[1]
            item["reviewedAt"] = seeds["reviewedAt"]
            updated += 1
    review_path.write_text(json.dumps(review, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Importadas {updated} respuestas jurídicas verificadas.")


if __name__ == "__main__":
    main()
