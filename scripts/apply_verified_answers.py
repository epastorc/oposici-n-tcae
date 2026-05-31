#!/usr/bin/env python3
"""Apply verified answers from the review queue to the static question bank."""

from __future__ import annotations

import json
from pathlib import Path


def main() -> None:
    bank_path = Path("web/data/questions.json")
    review_path = Path("data/answer-review.json")
    bank = json.loads(bank_path.read_text(encoding="utf-8"))
    items = json.loads(review_path.read_text(encoding="utf-8"))["items"]
    answers = {}
    for item in items:
        if item["status"] != "verified":
            continue
        for variant in item["variants"]:
            answer = item.get("variantAnswers", {}).get(variant["id"], item.get("answer"))
            if answer not in {"a", "b", "c", "d"}:
                continue
            answers[variant["id"]] = {
                "answer": answer,
                "sourceUrl": item["sourceUrl"],
                "sourceDetail": item["sourceDetail"],
                "reviewedAt": item["reviewedAt"],
            }

    for question in bank["questions"]:
        verified = answers.get(question["id"])
        question["correctAnswer"] = verified["answer"] if verified else None
        question["answerSource"] = verified["sourceUrl"] if verified else None
        question["answerSourceDetail"] = verified["sourceDetail"] if verified else None
        question["answerReviewedAt"] = verified["reviewedAt"] if verified else None

    bank_path.write_text(json.dumps(bank, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Aplicadas {len(answers)} respuestas verificadas.")


if __name__ == "__main__":
    main()
