#!/usr/bin/env python3
"""Import manually researched answers into the auditable review queue."""

from __future__ import annotations

import json
from pathlib import Path


def main() -> None:
    review_path = Path("data/answer-review.json")
    seed_files = [
        Path("data/legal-answer-seeds.json"),
        Path("data/legal-answer-seeds-37.json"),
        Path("data/legal-answer-seeds-39.json"),
        Path("data/legal-answer-seeds-36.json"),
        Path("data/legal-answer-seeds-35.json"),
        Path("data/legal-answer-seeds-38.json"),
        Path("data/legal-answer-seeds-09.json"),
        Path("data/legal-answer-seeds-16.json"),
        Path("data/legal-answer-seeds-21.json"),
        Path("data/legal-answer-seeds-17.json"),
        Path("data/clinical-answer-seeds-01.json"),
        Path("data/clinical-answer-seeds-10.json"),
        Path("data/clinical-answer-seeds-03.json"),
    ]
    review = json.loads(review_path.read_text(encoding="utf-8"))
    updated = 0
    for seed_file in seed_files:
        seeds = json.loads(seed_file.read_text(encoding="utf-8"))
        answers = seeds["answers"]
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
                for source_prefix, source_url in seeds.get("sourceUrls", {}).items():
                    if seeded[1].startswith(source_prefix):
                        item["sourceUrl"] = source_url
                        break
                item["sourceDetail"] = seeded[1]
                item["reviewedAt"] = seeds["reviewedAt"]
                updated += 1
    review_path.write_text(json.dumps(review, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Importadas {updated} respuestas jurídicas verificadas.")


if __name__ == "__main__":
    main()
