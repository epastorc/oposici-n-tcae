#!/usr/bin/env python3
"""Generate an independent TCAE-only thematic bank from verified exam questions."""

from __future__ import annotations

import json
import re
import unicodedata
from collections import Counter
from pathlib import Path

SOURCE = Path("web/data/questions.json")
OUTPUT = Path("web/data/thematic-questions.json")
QUESTION_LIMIT = 200

TOPICS = [
    ("Anatomía y fisiología", ("anatom", "fisiolog", "cardiovascular", "respirat", "digestiv", "urinari", "sangre", "circulación", "óseo", "muscular")),
    ("Higiene y confort", ("higiene", "aseo", "encamado", "baño", "cuña", "cama", "confort", "piel", "úlcera", "presión")),
    ("Cuidados básicos", ("sonda", "ostom", "diuresis", "incontinencia", "enema", "constantes", "temperatura", "fiebre", "eliminación", "nutrición")),
    ("Prevención e infecciones", ("infecci", "aislamiento", "esteriliz", "desinfec", "lavado de manos", "cauti", "vacuna", "microorgan", "residuo")),
    ("Documentación y organización sanitaria", ("ley", "decreto", "estatuto", "documentación", "historia clínica", "salud pública", "ses", "servicio extremeño")),
]


def normalize(text: str) -> str:
    text = unicodedata.normalize("NFD", text.casefold())
    return "".join(char for char in text if unicodedata.category(char) != "Mn")


def signature(question: dict) -> str:
    return re.sub(r"\W+", " ", normalize(question["prompt"])).strip()


def topic_for(question: dict) -> str:
    haystack = normalize(
        " ".join(
            [
                question.get("prompt", ""),
                question.get("answerSourceDetail", ""),
                *(option.get("text", "") for option in question.get("options", [])),
            ]
        )
    )
    for topic, terms in TOPICS:
        if any(normalize(term) in haystack for term in terms):
            return topic
    return "Atención sanitaria TCAE"


def eligible_questions() -> list[dict]:
    questions = json.loads(SOURCE.read_text(encoding="utf-8"))["questions"]
    selected = []
    seen = set()
    for question in questions:
        question_signature = signature(question)
        answer = question.get("correctAnswer")
        if (
            not isinstance(answer, str)
            or answer not in "abcd"
            or not question.get("answerSource")
            or not question.get("answerSourceDetail")
            or question_signature in seen
        ):
            continue
        seen.add(question_signature)
        selected.append(question)
        if len(selected) == QUESTION_LIMIT:
            return selected
    raise SystemExit(f"Solo se han encontrado {len(selected)} preguntas TCAE verificadas")


def thematic_question(number: int, question: dict) -> dict:
    return {
        "id": f"temario-tcae-{number:03d}",
        "topic": topic_for(question),
        "source": "Banco temático TCAE",
        "number": number,
        "prompt": question["prompt"],
        "options": question["options"],
        "correctAnswer": question["correctAnswer"],
        "answerSource": question["answerSource"],
        "answerSourceDetail": question["answerSourceDetail"],
        "answerReviewedAt": question.get("answerReviewedAt"),
        "originQuestionId": question["id"],
    }


def main() -> None:
    questions = [
        thematic_question(number, question)
        for number, question in enumerate(eligible_questions(), start=1)
    ]
    payload = {
        "metadata": {
            "title": "Banco temático exclusivo TCAE",
            "generatedAt": "2026-06-01",
            "scope": "Preguntas sanitarias TCAE con solución previamente verificada",
            "origin": str(SOURCE),
        },
        "questions": questions,
    }
    OUTPUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Generadas {len(questions)} preguntas TCAE en {OUTPUT}")
    print(f"Temas: {dict(Counter(question['topic'] for question in questions))}")


if __name__ == "__main__":
    main()
