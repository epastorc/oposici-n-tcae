#!/usr/bin/env python3
"""Import official SES answer sheets and safely propagate equivalent variants."""

from __future__ import annotations

import io
import json
import re
import unicodedata
from pathlib import Path
from urllib.request import urlopen

from pypdf import PdfReader

SHEETS = [
    {
        "questionSource": "TCAE_EXAMEN 30.pdf",
        "answerUrl": "https://saludextremadura.ses.es/bolsa/documentos/2019_04_29_002.pdf",
        "sourceDetail": "Plantilla SES tipo 1, turno libre y discapacidad, 27 de abril de 2019",
        "reviewedAt": "2026-05-31",
    },
    {
        "questionSource": "TCAE_EXAMEN 32.pdf",
        "answerUrl": "https://www.juntaex.es/documents/77055/314190/1212%2BRESPUESTAS_E1_1212_1.pdf/42fa2448-cef5-4249-a7ad-f66c829422ba?t=1414688042010&version=1.0",
        "sourceDetail": "Plantilla Junta de Extremadura, auxiliar de enfermería, examen tipo 1, 19 de diciembre de 2009",
        "reviewedAt": "2026-05-31",
    },
    {
        "questionSource": "TCAE_EXAMEN 33.pdf",
        "answerUrl": "https://www.juntaex.es/documents/77055/314190/1212%2BRESPUESTAS_E1_1212_2.pdf/1cd30681-f7a1-439c-a1d0-9fcc17811f86?t=1414688045790&version=1.0",
        "sourceDetail": "Plantilla Junta de Extremadura, auxiliar de enfermería, examen tipo 2, 19 de diciembre de 2009",
        "reviewedAt": "2026-05-31",
    }
]


def normalize(text: str) -> str:
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode()
    return re.sub(r"\W+", " ", text.lower()).strip()


def parse_sheet(url: str) -> dict[int, str]:
    with urlopen(url) as response:
        pdf = PdfReader(io.BytesIO(response.read()))
    text = " ".join(page.extract_text() or "" for page in pdf.pages)
    return {int(number): answer.lower() for number, answer in re.findall(r"\b(\d{1,3})[.\s-]+([A-D])\b", text)}


def propagate_equivalent_variants(items: list[dict]) -> int:
    propagated = 0
    for item in items:
        answer_text = None
        for variant in item["variants"]:
            answer = item["variantAnswers"].get(variant["id"])
            if answer:
                answer_text = normalize(next(option["text"] for option in variant["options"] if option["key"] == answer))
                break
        if not answer_text:
            continue
        for variant in item["variants"]:
            if variant["id"] in item["variantAnswers"]:
                continue
            matches = [option["key"] for option in variant["options"] if normalize(option["text"]) == answer_text]
            if len(matches) == 1:
                item["variantAnswers"][variant["id"]] = matches[0]
                propagated += 1
    return propagated


def main() -> None:
    review_path = Path("data/answer-review.json")
    review = json.loads(review_path.read_text(encoding="utf-8"))
    imported = 0
    for sheet in SHEETS:
        answers = parse_sheet(sheet["answerUrl"])
        for item in review["items"]:
            for variant in item["variants"]:
                if variant["source"] != sheet["questionSource"]:
                    continue
                answer = answers.get(variant["number"])
                if not answer:
                    continue
                item["variantAnswers"][variant["id"]] = answer
                item["status"] = "verified"
                item["confidence"] = "high"
                item["sourceUrl"] = sheet["answerUrl"]
                item["sourceDetail"] = sheet["sourceDetail"]
                item["sourceKind"] = "official"
                item["reviewedAt"] = sheet["reviewedAt"]
                imported += 1
    propagated = propagate_equivalent_variants(review["items"])
    review_path.write_text(json.dumps(review, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Importadas {imported} respuestas SES; propagadas {propagated} variantes equivalentes.")


if __name__ == "__main__":
    main()
