#!/usr/bin/env python3
"""Convert an Academia Opolis correction PDF into an auditable answer seed file."""

from __future__ import annotations

import argparse
import io
import json
import re
import unicodedata
from datetime import date
from pathlib import Path
from urllib.parse import urlparse
from urllib.request import urlopen

from pypdf import PdfReader


def normalize(text: str) -> str:
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode()
    return re.sub(r"\W+", " ", text.lower()).strip()


def read_pdf(source: str) -> PdfReader:
    if urlparse(source).scheme in {"http", "https"}:
        with urlopen(source) as response:
            return PdfReader(io.BytesIO(response.read()))
    return PdfReader(source)


def parse_answers(source: str) -> list[tuple[str, str]]:
    text = "\n".join(page.extract_text() or "" for page in read_pdf(source).pages)
    pattern = re.compile(
        r"(?ms)^\s*\d+\.\s+([a-d])\)\s*(.*?)(?=^\s*\d+\.\s+(?:[a-d]\)|\S)|\Z)"
    )
    return [(match.group(1), " ".join(match.group(2).split())) for match in pattern.finditer(text)]


def answer_matches_option(answer_text: str, option_text: str) -> bool:
    answer = normalize(answer_text)
    option = normalize(option_text)
    prefix_length = min(45, len(answer), len(option))
    return not prefix_length or answer[:prefix_length] == option[:prefix_length]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("question_source", help="Source name in questions.json, for example 'TCAE_EXAMEN 2.pdf'")
    parser.add_argument("correction_pdf", help="Local path or public URL for the correction PDF")
    parser.add_argument("--source-url", help="Public correction-sheet URL to expose in the web app")
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--include-existing", action="store_true")
    args = parser.parse_args()

    bank = json.loads(Path("web/data/questions.json").read_text(encoding="utf-8"))
    questions = sorted(
        (question for question in bank["questions"] if question["source"] == args.question_source),
        key=lambda question: question["number"],
    )
    answers = parse_answers(args.correction_pdf)
    if len(answers) != len(questions):
        raise SystemExit(
            f"La plantilla contiene {len(answers)} respuestas y el examen {len(questions)} preguntas."
        )

    seeds = {}
    for question, (answer, answer_text) in zip(questions, answers):
        option = next((option for option in question["options"] if option["key"] == answer), None)
        if not option or not answer_matches_option(answer_text, option["text"]):
            raise SystemExit(
                f"No coincide la pregunta {question['number']}: {answer}) {answer_text}"
            )
        if args.include_existing or not question.get("correctAnswer"):
            seeds[str(question["number"])] = [
                answer,
                f"Plantilla de corrección Academia Opolis, pregunta {question['number']}",
            ]

    output = {
        "source": args.question_source,
        "sourceUrl": args.source_url or "",
        "sourceKind": "author-key",
        "reviewedAt": date.today().isoformat(),
        "answers": seeds,
    }
    args.output.write_text(json.dumps(output, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Generado {args.output}: {len(seeds)} respuestas tomadas de la plantilla del autor.")


if __name__ == "__main__":
    main()
