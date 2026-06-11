#!/usr/bin/env python3
"""Extract multiple-choice questions from TCAE exam PDFs into static JSON."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

from pypdf import PdfReader

QUESTION_RE = re.compile(r"(?m)^\s*([1-9]\d{0,2})(?:(?:º)?\.(?:-)?|º-)\s*")
OPTION_RE = re.compile(r"(?m)^\s*([a-dA-D])(?:\.\)|\)|\.)\s*")
HEADER_RE = re.compile(
    r"(?im)^\s*(?:ACADEMIA OPOLIS.*|TLF\..*|CÁCERES\s*|"
    r"EJERCICIO ELABORADO POR.*|MIGUEL DELCARMEN\s*|\d{1,2}\s*)$"
)


def clean(text: str) -> str:
    text = re.sub(
        r"\s*TRIBUNAL DE SELECCIÓN.*?P\s*á\s*g\s*i\s*n\s*a\s+\d+\s*\|\s*\d+",
        " ",
        text,
        flags=re.IGNORECASE | re.DOTALL,
    )
    text = re.sub(r"\bPREGUNTAS ADICIONALES\s*(?:\(RESERVA\))?", " ", text, flags=re.IGNORECASE)
    text = re.sub(r"\bPARTE\s+(?:TEÓRICA|TEORICA|PRÁCTICA|PRACTICA)\b", " ", text, flags=re.IGNORECASE)
    text = HEADER_RE.sub("", text)
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r" *\n *", "\n", text)
    return re.sub(r"\s+", " ", text).strip()


def extract_pdf(path: Path) -> tuple[list[dict], list[str]]:
    reader = PdfReader(str(path))
    raw = "\n".join(page.extract_text() or "" for page in reader.pages)
    raw = HEADER_RE.sub("", raw)
    matches = list(QUESTION_RE.finditer(raw))
    questions: list[dict] = []
    warnings: list[str] = []

    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(raw)
        block = raw[match.end() : end]
        options = list(OPTION_RE.finditer(block))
        number = int(match.group(1))
        if len(options) != 4:
            warnings.append(f"{path.name}: pregunta {number}: {len(options)} opciones")
            continue
        prompt = clean(block[: options[0].start()])
        answers = []
        for option_index, option in enumerate(options):
            option_end = (
                options[option_index + 1].start()
                if option_index + 1 < len(options)
                else len(block)
            )
            answers.append(
                {"key": "abcd"[option_index], "text": clean(block[option.end() : option_end])}
            )
        questions.append(
            {
                "id": f"{path.stem.lower().replace(' ', '-')}-{len(questions) + 1}",
                "source": path.name,
                "number": number,
                "prompt": prompt,
                "options": answers,
                "correctAnswer": None,
            }
        )
    return questions, warnings


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("pdfs", nargs="+", type=Path)
    parser.add_argument("-o", "--output", type=Path, default=Path("web/data/questions.json"))
    args = parser.parse_args()

    questions: list[dict] = []
    warnings: list[str] = []
    sources: list[dict] = []
    for pdf in sorted(args.pdfs):
        extracted, pdf_warnings = extract_pdf(pdf)
        questions.extend(extracted)
        warnings.extend(pdf_warnings)
        sources.append({"file": pdf.name, "questions": len(extracted)})

    payload = {"questions": questions, "sources": sources, "warnings": warnings}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Extraídas {len(questions)} preguntas de {len(sources)} PDF.")
    if warnings:
        print(f"Avisos: {len(warnings)}. Revisa el campo warnings de {args.output}.")


if __name__ == "__main__":
    main()
