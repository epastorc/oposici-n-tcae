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
        Path("data/clinical-answer-seeds-02.json"),
        Path("data/clinical-answer-seeds-05.json"),
        Path("data/clinical-answer-seeds-06.json"),
        Path("data/clinical-answer-seeds-13.json"),
        Path("data/legal-answer-seeds-19.json"),
        Path("data/legal-answer-seeds-34.json"),
        Path("data/clinical-answer-seeds-12.json"),
        Path("data/clinical-answer-seeds-14.json"),
        Path("data/clinical-answer-seeds-15.json"),
        Path("data/legal-answer-seeds-22.json"),
        Path("data/legal-answer-seeds-23.json"),
        Path("data/legal-answer-seeds-24.json"),
        Path("data/legal-answer-seeds-25.json"),
        Path("data/legal-answer-seeds-26.json"),
        Path("data/legal-answer-seeds-27.json"),
        Path("data/legal-answer-seeds-28.json"),
        Path("data/clinical-answer-seeds-29.json"),
        Path("data/legal-answer-seeds-20.json"),
        Path("data/clinical-answer-seeds-08.json"),
        Path("data/clinical-answer-seeds-07.json"),
        Path("data/clinical-answer-seeds-04.json"),
        Path("data/clinical-answer-seeds-18.json"),
    ]
    seed_files.extend(sorted(Path("data").glob("author-answer-seeds-*.json")))
    seed_files.extend(sorted(Path("data").glob("batch-answer-seeds-*.json")))
    seed_files.extend(sorted(Path("data").glob("forced-answer-seeds-*.json")))
    review = json.loads(review_path.read_text(encoding="utf-8"))
    updated = 0
    for seed_file in seed_files:
        seeds = json.loads(seed_file.read_text(encoding="utf-8"))
        answers = seeds["answers"]
        excluded = seeds.get("excluded", {})
        for item in review["items"]:
            excluded_details = []
            for variant in item["variants"]:
                if variant["source"] != seeds["source"]:
                    continue
                if str(variant["number"]) in excluded:
                    item["variantAnswers"].pop(variant["id"], None)
                    excluded_details.append(f"{variant['source']} #{variant['number']}: {excluded[str(variant['number'])]}")
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
                item["sourceKind"] = seeded[2] if len(seeded) > 2 else seeds.get("sourceKind", "official")
                item["reviewedAt"] = seeds["reviewedAt"]
                item["notes"] = None
                updated += 1
            if excluded_details and not item.get("answer") and not item["variantAnswers"]:
                item["status"] = "excluded"
                item["confidence"] = None
                item["sourceUrl"] = seeds["sourceUrl"]
                item["sourceDetail"] = "; ".join(excluded_details)
                item["sourceKind"] = "review-exclusion"
                item["reviewedAt"] = seeds["reviewedAt"]
                item["notes"] = "Excluida tras revisión: " + "; ".join(excluded_details)
    for item in review["items"]:
        if item.get("status") == "excluded":
            continue
        if item.get("answer") or item["variantAnswers"]:
            continue
        item["status"] = "pending"
        item["confidence"] = None
        item["sourceUrl"] = None
        item["sourceDetail"] = None
        item["sourceKind"] = None
        item["reviewedAt"] = None
    review_path.write_text(json.dumps(review, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Importadas {updated} respuestas jurídicas verificadas.")


if __name__ == "__main__":
    main()
