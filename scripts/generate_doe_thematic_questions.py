#!/usr/bin/env python3
"""Generate the independent thematic bank from DOE 250/2024."""

from __future__ import annotations

import json
import random
from pathlib import Path

DOE_URL = "https://doe.juntaex.es/pdfs/doe/2024/2500o/24050220.pdf"
OUTPUT = Path("web/data/thematic-questions.json")

# topic, reference, page, subject, correct value, distractors
FACTS = [
    ("Convocatoria Grupo V", "Base Primera.1", 1, "número total de plazas convocadas", "118 plazas", ["108 plazas", "120 plazas", "128 plazas"]),
    ("Convocatoria Grupo V", "Base Primera.1", 1, "plazas del turno libre", "108 plazas", ["10 plazas", "118 plazas", "98 plazas"]),
    ("Convocatoria Grupo V", "Base Primera.1", 1, "plazas reservadas a discapacidad", "10 plazas", ["8 plazas", "12 plazas", "18 plazas"]),
    ("Convocatoria Grupo V", "Base Primera.1", 1, "grado mínimo de discapacidad para el turno reservado", "igual o superior al 33 %", ["superior al 25 %", "igual o superior al 40 %", "superior al 50 %"]),
    ("Convocatoria Grupo V", "Base Primera.3", 2, "destino de las plazas vacantes del turno de discapacidad", "se acumulan al turno libre", ["quedan desiertas", "se convocan al año siguiente", "se cubren por promoción interna"]),
    ("Requisitos", "Base Segunda.1.b", 3, "edad mínima para participar", "16 años cumplidos", ["18 años cumplidos", "21 años cumplidos", "15 años cumplidos"]),
    ("Requisitos", "Base Segunda.1.b", 3, "límite máximo de edad", "no exceder la edad máxima de jubilación forzosa", ["no exceder 60 años", "no exceder 65 años en todo caso", "no exceder 55 años"]),
    ("Requisitos", "Base Segunda.1.c", 3, "requisito adicional de la categoría Ordenanza", "permiso de conducción B", ["permiso de conducción A", "permiso de conducción C", "carné de manipulador de alimentos"]),
    ("Requisitos", "Base Segunda.1.d", 3, "capacidad exigida a las personas aspirantes", "capacidad funcional necesaria para el puesto", ["capacidad deportiva acreditada", "experiencia mínima de dos años", "disponibilidad geográfica absoluta"]),
    ("Requisitos", "Base Segunda.1.f", 4, "personal laboral fijo que no puede presentarse", "el de la misma categoría y especialidad", ["todo el personal temporal", "todo empleado público", "quien trabaje en otra especialidad"]),
    ("Requisitos", "Base Segunda.2", 4, "momento de acreditar la discapacidad para el turno reservado", "último día del plazo de solicitudes", ["día del examen", "día de publicación de la lista definitiva", "día de toma de posesión exclusivamente"]),
    ("Requisitos", "Base Segunda.3", 4, "acreditación previa para puestos con contacto habitual con menores", "no haber sido condenado por delitos contra la libertad e indemnidad sexual", ["carecer de sanciones de tráfico", "tener permiso B", "haber realizado un curso de primeros auxilios"]),
    ("Solicitudes", "Base Tercera.1", 5, "duración del plazo de presentación de solicitudes", "20 días hábiles", ["10 días hábiles", "15 días naturales", "30 días hábiles"]),
    ("Solicitudes", "Base Tercera.1", 5, "fecha a partir de la que se cuenta el plazo de solicitudes", "16 de enero de 2025", ["27 de diciembre de 2024", "1 de enero de 2025", "16 de febrero de 2025"]),
    ("Solicitudes", "Base Tercera.2.a", 5, "soporte válido para la solicitud gestionada íntegramente por sede electrónica", "soporte digital", ["papel presentado por duplicado", "fax", "correo electrónico sin registro"]),
    ("Solicitudes", "Base Tercera.2.b.1", 6, "efecto de la simple cumplimentación por internet en la aplicación", "no sustituye su presentación en registro", ["equivale al registro", "exime de firmar", "exime del pago de tasas"]),
    ("Solicitudes", "Base Tercera.2.b.1", 6, "órgano al que se dirigen las solicitudes", "Servicio de Selección de la Dirección General de Función Pública", ["Tribunal Superior de Justicia", "Instituto de la Mujer de Extremadura", "Servicio Extremeño de Salud"]),
    ("Solicitudes", "Base Tercera.2.b.2", 7, "unidad DIR3 para el registro electrónico", "A11019084. Serv. de Selección", ["A11019084. Tesorería", "A11019084. Registro Civil", "A11019084. Inspección Médica"]),
    ("Solicitudes", "Base Tercera.2.b.2", 8, "forma de presentar una solicitud mediante Correos", "en sobre abierto para ser fechada y sellada", ["en sobre cerrado sin sellar", "por correo ordinario sin registro", "únicamente mediante burofax"]),
    ("Solicitudes", "Base Tercera.3", 9, "quién puede solicitar adaptación de tiempo y medios", "cualquier aspirante con discapacidad", ["solo quien concurra por turno reservado", "solo quien tenga discapacidad superior al 65 %", "únicamente el personal laboral temporal"]),
    ("Solicitudes", "Base Tercera.3", 9, "efecto del reconocimiento posterior de discapacidad con efectos retroactivos", "no permite la admisión en el turno de discapacidad", ["obliga a cambiar el turno", "anula la convocatoria", "permite elegir turno tras el examen"]),
    ("Listas de espera", "Base Tercera.4", 9, "efecto de no señalar zonas para la lista de espera", "se entiende que se opta a todas", ["se renuncia a todas", "se elige solo Mérida", "la solicitud queda excluida"]),
    ("Solicitudes", "Base Tercera.5", 10, "solicitudes necesarias para concurrir a varias especialidades", "una solicitud por cada especialidad", ["una única solicitud conjunta", "una solicitud por cada turno y provincia", "dos solicitudes por especialidad"]),
    ("Tasas", "Base Tercera.6", 10, "importe de la tasa por derechos de examen", "15,43 euros", ["10,43 euros", "15,00 euros", "25,43 euros"]),
    ("Tasas", "Base Tercera.6", 10, "código de la tasa por derechos de examen", "100161", ["100116", "101061", "110061"]),
    ("Tasas", "Base Tercera.7", 11, "bonificación parcial por desempleo", "50 %", ["25 %", "75 %", "100 %"]),
    ("Tasas", "Base Tercera.7", 11, "periodo mínimo previo de desempleo para la bonificación", "tres meses", ["un mes", "seis meses", "doce meses"]),
    ("Tasas", "Base Tercera.7", 11, "documento válido para acreditar desempleo", "informe de vida laboral de la Tesorería General de la Seguridad Social", ["tarjeta de demanda de empleo", "declaración jurada sin documentos", "certificado bancario"]),
    ("Tasas", "Base Tercera.8.a", 11, "discapacidad que exime del pago de la tasa", "igual o superior al 33 %", ["igual o superior al 20 %", "superior al 40 %", "igual o superior al 65 % exclusivamente"]),
    ("Admisión", "Base Cuarta.1", 12, "plazo máximo para aprobar la lista provisional", "dos meses", ["diez días", "un mes", "seis meses"]),
    ("Admisión", "Base Cuarta.1", 12, "plazo de subsanación tras la lista provisional", "10 días hábiles", ["5 días hábiles", "10 días naturales", "15 días hábiles"]),
    ("Admisión", "Base Cuarta.2", 12, "plazo para publicar listas definitivas tras finalizar la subsanación", "15 días hábiles", ["5 días hábiles", "10 días naturales", "20 días hábiles"]),
    ("Tribunales", "Base Quinta.1", 13, "quién nombra los Tribunales de Selección", "la persona titular de la Consejería de Hacienda y Administración Pública", ["la Dirección General de Tributos", "el Consejo de Gobierno en pleno", "las organizaciones sindicales"]),
    ("Tribunales", "Base Quinta.2", 13, "periodo de incompatibilidad por preparar aspirantes", "cinco años anteriores", ["un año anterior", "dos años anteriores", "diez años anteriores"]),
    ("Tribunales", "Base Quinta.4", 13, "quórum mínimo del Tribunal", "Presidencia, Secretaría y al menos la mitad de sus miembros", ["solo Presidencia", "todos los miembros sin excepción", "Secretaría y un vocal"]),
    ("Tribunales", "Base Quinta.7", 14, "función de las personas asesoras especialistas", "colaborar en sus especialidades técnicas", ["calificar con voto de calidad", "sustituir a la Presidencia", "aprobar las listas definitivas"]),
    ("Sistema selectivo", "Base Sexta.1", 14, "procedimiento de selección", "concurso-oposición", ["oposición libre sin concurso", "concurso de méritos exclusivamente", "entrevista personal"]),
    ("Sistema selectivo", "Base Sexta.1", 14, "orden de las fases", "oposición y después concurso", ["concurso y después oposición", "entrevista y después concurso", "concurso únicamente"]),
    ("Sistema selectivo", "Base Sexta.1", 14, "puntuación máxima de la oposición", "10 puntos", ["3 puntos", "5 puntos", "13 puntos"]),
    ("Sistema selectivo", "Base Sexta.1", 14, "puntuación máxima del concurso", "3 puntos", ["5 puntos", "10 puntos", "13 puntos"]),
    ("Sistema selectivo", "Base Sexta.2", 15, "número de preguntas del cuestionario", "37 preguntas", ["35 preguntas", "40 preguntas", "50 preguntas"]),
    ("Sistema selectivo", "Base Sexta.2", 15, "número de preguntas adicionales de reserva", "5 preguntas", ["2 preguntas", "3 preguntas", "10 preguntas"]),
    ("Sistema selectivo", "Base Sexta.2", 15, "tiempo máximo para contestar el ejercicio", "70 minutos", ["45 minutos", "60 minutos", "90 minutos"]),
    ("Sistema selectivo", "Base Sexta.2", 15, "puntuación mínima para aprobar oposición", "5 puntos", ["3 puntos", "6 puntos", "7,5 puntos"]),
    ("Sistema selectivo", "Base Sexta.2", 15, "penalización por respuesta errónea", "un tercio del valor de una respuesta correcta", ["no penaliza", "la mitad del valor de una correcta", "el valor completo de una correcta"]),
    ("Sistema selectivo", "Base Sexta.2", 15, "efecto de una pregunta en blanco", "no se valora", ["resta un tercio", "suma medio punto", "resta una respuesta correcta"]),
    ("Sistema selectivo", "Base Sexta.2", 15, "momento para acceder al concurso", "tras superar la fase de oposición", ["antes de realizar la oposición", "tras presentar la solicitud", "solo tras la toma de posesión"]),
    ("Méritos", "Base Sexta.3", 16, "méritos valorables en el concurso", "servicios prestados", ["títulos académicos adicionales exclusivamente", "entrevista personal", "domicilio en Extremadura"]),
    ("Méritos", "Base Sexta.3", 16, "fecha límite para valorar servicios prestados", "fecha de finalización del plazo de solicitudes", ["fecha del examen", "fecha de toma de posesión", "fecha de publicación de aprobados"]),
    ("Desarrollo", "Base Séptima.4", 18, "plazo máximo para celebrar el ejercicio desde la lista provisional", "5 meses", ["2 meses", "8 meses", "12 meses"]),
    ("Desarrollo", "Base Séptima.4", 19, "mes declarado inhábil para cómputo de plazos", "agosto", ["julio", "diciembre", "enero"]),
    ("Desarrollo", "Base Séptima.4", 19, "plazo máximo de resolución del proceso selectivo", "12 meses", ["5 meses", "18 meses", "24 meses"]),
    ("Superación", "Base Octava.1", 19, "plazo para presentar méritos tras superar oposición", "10 días hábiles", ["5 días hábiles", "15 días naturales", "20 días hábiles"]),
    ("Superación", "Base Octava.2", 19, "plazo para reclamar la puntuación provisional del concurso", "5 días hábiles", ["3 días hábiles", "10 días hábiles", "15 días naturales"]),
    ("Superación", "Base Octava.3", 20, "primer criterio de desempate", "mayor puntuación en la fase de oposición", ["mayor edad", "orden de presentación de solicitudes", "sorteo individual"]),
    ("Superación", "Base Octava.3", 20, "segundo criterio de desempate", "mayor puntuación en la fase de concurso", ["menor edad", "mayor antigüedad como demandante de empleo", "orden de registro"]),
    ("Superación", "Base Octava.3", 20, "letra inicial aplicable si persiste el empate", "S", ["A", "M", "Z"]),
    ("Superación", "Base Octava.4", 20, "plazo de alegaciones a la relación provisional de aprobados", "10 días hábiles", ["5 días hábiles", "15 días naturales", "un mes"]),
    ("Documentación", "Base Novena.1", 21, "plazo para presentar documentación tras la relación definitiva", "10 días hábiles", ["5 días hábiles", "15 días hábiles", "20 días naturales"]),
    ("Documentación", "Base Novena.1.a", 21, "alternativa a presentar copia auténtica del DNI", "autorizar consulta mediante SVDI", ["presentar una fotografía", "aportar el permiso de conducir", "declarar verbalmente la identidad"]),
    ("Documentación", "Base Novena.1.e", 22, "documento específico que presenta Ordenanza", "copia auténtica del permiso de conducción B", ["certificado de manipulador", "permiso de conducción C", "título de bachillerato"]),
    ("Documentación", "Base Novena.2", 23, "carácter del informe médico", "confidencial", ["público", "opcional para la Administración", "reutilizable para cualquier finalidad"]),
    ("Documentación", "Base Novena.4", 23, "alternativa ante imposibilidad justificada de presentar documentos", "cualquier medio de prueba admitido en Derecho", ["ninguna alternativa", "solo declaración telefónica", "únicamente certificado notarial"]),
    ("Adjudicación", "Base Décima.1", 24, "plazo para solicitar adjudicación de puesto", "5 días hábiles", ["10 días hábiles", "15 días naturales", "un mes"]),
    ("Adjudicación", "Base Décima.2", 24, "criterio general de adjudicación", "puntuación obtenida y orden indicado en la solicitud", ["sorteo", "edad", "orden alfabético exclusivamente"]),
    ("Adjudicación", "Base Décima.3", 24, "efecto de no solicitar puestos en plazo", "adjudicación de oficio de un puesto no adjudicado", ["pérdida automática de la plaza", "nuevo examen", "elección preferente posterior"]),
    ("Contratación", "Base Undécima", 25, "tipo de contrato tras la adjudicación", "contrato como personal laboral fijo", ["nombramiento como funcionario interino", "contrato temporal de seis meses", "contrato mercantil"]),
    ("Listas de espera", "Base Duodécima", 25, "puntuación considerada para listas de espera", "la obtenida en la fase de oposición", ["solo la del concurso", "la suma de oposición y entrevista", "únicamente la antigüedad"]),
    ("Recursos", "Base Decimotercera", 25, "plazo del recurso potestativo de reposición", "un mes", ["10 días hábiles", "dos meses", "seis meses"]),
    ("Recursos", "Base Decimotercera", 26, "plazo del recurso contencioso-administrativo directo", "dos meses", ["un mes", "10 días hábiles", "seis meses"]),
    ("Anexo I", "Anexo I", 27, "plazas totales de Ayudante de cocina", "39 plazas", ["36 plazas", "35 plazas", "30 plazas"]),
    ("Anexo I", "Anexo I", 27, "plazas totales de Camarero/a-Limpiador/a", "39 plazas", ["35 plazas", "36 plazas", "40 plazas"]),
    ("Anexo I", "Anexo I", 27, "plazas totales de Ordenanza", "39 plazas", ["36 plazas", "35 plazas", "42 plazas"]),
    ("Anexo I", "Anexo I", 27, "plazas libres de Ayudante de cocina", "36 plazas", ["3 plazas", "35 plazas", "39 plazas"]),
    ("Anexo I", "Anexo I", 27, "plazas libres de Camarero/a-Limpiador/a", "35 plazas", ["4 plazas", "36 plazas", "39 plazas"]),
    ("Anexo I", "Anexo I", 27, "plazas libres de Ordenanza", "36 plazas", ["3 plazas", "35 plazas", "39 plazas"]),
    ("Anexo II", "Anexo II.1", 28, "versión mínima de Autofirma indicada", "1.7.2", ["1.5.0", "2.0.0", "1.6.1"]),
    ("Anexo II", "Anexo II.3", 28, "número de tipos de tramitación online", "cuatro", ["dos", "tres", "cinco"]),
    ("Anexo II", "Anexo II.4", 28, "medios de verificación de identidad indicados", "Certificado Digital o DNI Electrónico", ["SMS sin identificación", "correo ordinario", "llamada telefónica"]),
    ("Anexo II", "Anexo II.6.3", 29, "dato de contacto obligatorio", "número de teléfono", ["correo electrónico", "fax", "perfil de red social"]),
    ("Anexo II", "Anexo II.6.4", 30, "efecto de no marcar zona para lista de espera", "se entiende que opta a todas", ["queda fuera de la lista", "opta solo a Cáceres", "debe subsanar siempre"]),
    ("Anexo II", "Anexo II.8", 30, "efecto de faltar un documento acreditativo", "aparición en excluidos y necesidad de subsanar", ["admisión definitiva automática", "devolución inmediata de la tasa", "archivo sin posibilidad de subsanar"]),
    ("Anexo II", "Anexo II.11", 31, "documento que confirma la presentación telemática", "justificante de registro telemático", ["borrador de solicitud", "modelo 050 vacío", "captura de pantalla"]),
    ("Temario Ayudante de cocina", "Anexo IV. Ayudante de cocina. Tema 6", 33, "tema que incluye alteración y contaminación de alimentos", "Tema 6", ["Tema 2", "Tema 8", "Tema 10"]),
    ("Temario Ayudante de cocina", "Anexo IV. Ayudante de cocina. Tema 7", 33, "tema que incluye APPCC", "Tema 7", ["Tema 3", "Tema 5", "Tema 9"]),
    ("Temario Ayudante de cocina", "Anexo IV. Ayudante de cocina. Tema 8", 33, "tema que incluye alimentación, nutrición y dietas", "Tema 8", ["Tema 4", "Tema 6", "Tema 10"]),
    ("Temario Ayudante de cocina", "Anexo IV. Ayudante de cocina. Tema 9", 33, "tema dedicado a prevención de riesgos laborales", "Tema 9", ["Tema 1", "Tema 5", "Tema 10"]),
    ("Temario Camarero/a-Limpiador/a", "Anexo IV. Camarero/a-Limpiador/a. Tema 2", 34, "tema que incluye dosificación y símbolos de etiquetas", "Tema 2", ["Tema 4", "Tema 7", "Tema 9"]),
    ("Temario Camarero/a-Limpiador/a", "Anexo IV. Camarero/a-Limpiador/a. Tema 6", 34, "tema dedicado a lavado, planchado y conservación de tejidos", "Tema 6", ["Tema 3", "Tema 5", "Tema 8"]),
    ("Temario Camarero/a-Limpiador/a", "Anexo IV. Camarero/a-Limpiador/a. Tema 7", 34, "tema dedicado a aspectos ecológicos de la limpieza", "Tema 7", ["Tema 2", "Tema 6", "Tema 10"]),
    ("Temario Camarero/a-Limpiador/a", "Anexo IV. Camarero/a-Limpiador/a. Tema 8", 34, "tema que incluye manipulación de alimentos", "Tema 8", ["Tema 4", "Tema 6", "Tema 9"]),
    ("Temario Camarero/a-Limpiador/a", "Anexo IV. Camarero/a-Limpiador/a. Tema 9", 34, "tema que incluye emergencias, incendios y evacuación", "Tema 9", ["Tema 3", "Tema 5", "Tema 10"]),
    ("Temario Ordenanza", "Anexo IV. Ordenanza. Tema 1", 34, "tema que incluye fontanería, cerrajería y electricidad", "Tema 1", ["Tema 3", "Tema 6", "Tema 9"]),
    ("Temario Ordenanza", "Anexo IV. Ordenanza. Tema 2", 35, "tema que incluye control de entrada y cierre de edificios", "Tema 2", ["Tema 4", "Tema 7", "Tema 10"]),
    ("Temario Ordenanza", "Anexo IV. Ordenanza. Tema 3", 35, "tema que incluye fotocopiadoras, encuadernadoras y trituradoras", "Tema 3", ["Tema 1", "Tema 5", "Tema 8"]),
    ("Temario Ordenanza", "Anexo IV. Ordenanza. Tema 5", 35, "tema dedicado a información al público", "Tema 5", ["Tema 2", "Tema 7", "Tema 9"]),
    ("Temario Ordenanza", "Anexo IV. Ordenanza. Tema 7", 35, "tema que incluye documentos, notificaciones y envíos postales", "Tema 7", ["Tema 3", "Tema 6", "Tema 8"]),
    ("Temario Ordenanza", "Anexo IV. Ordenanza. Tema 8", 35, "tema que incluye comunicación telefónica y escucha", "Tema 8", ["Tema 1", "Tema 4", "Tema 10"]),
    ("Temario Ordenanza", "Anexo IV. Ordenanza. Tema 9", 35, "tema que incluye prevención de incendios y evacuación", "Tema 9", ["Tema 2", "Tema 5", "Tema 7"]),
    ("Igualdad", "Anexo IV. Tema 10 de las tres categorías", 33, "tema común a las tres categorías", "Ley de Igualdad y violencia de género en Extremadura", ["despiece de carnes", "maquinaria de oficina", "lavandería industrial"]),
]


def build_question(index: int, fact: tuple[str, str, int, str, str, list[str]], variant: int) -> dict:
    topic, reference, page, subject, correct, distractors = fact
    prompts = [
        f"Según la Orden de 23 de diciembre de 2024, indique la opción correcta para: {subject}.",
        f"Señale la opción correcta sobre {subject} en la convocatoria publicada en el DOE.",
    ]
    options = [correct, *distractors]
    random.Random(index).shuffle(options)
    keys = "abcd"
    answer = keys[options.index(correct)]
    return {
        "id": f"doe-grupo-v-{index:03d}",
        "topic": topic,
        "source": "DOE 250/2024",
        "number": index,
        "prompt": prompts[variant],
        "options": [{"key": key, "text": text} for key, text in zip(keys, options)],
        "correctAnswer": answer,
        "explanation": f"La referencia aplicable establece como respuesta correcta: {correct}.",
        "answerSource": DOE_URL,
        "answerSourceDetail": f"{reference}, página {page} del PDF",
        "difficulty": "media" if variant else "baja",
        "audit": {"page": page, "reference": reference, "excerpt": correct},
    }


def main() -> None:
    if len(FACTS) != 100:
        raise SystemExit(f"Se esperaban 100 hechos y hay {len(FACTS)}")
    questions = []
    for fact_index, fact in enumerate(FACTS):
        questions.append(build_question(fact_index * 2 + 1, fact, 0))
        questions.append(build_question(fact_index * 2 + 2, fact, 1))
    payload = {
        "metadata": {
            "title": "Orden de 23 de diciembre de 2024: Grupo V",
            "source": DOE_URL,
            "generatedAt": "2026-06-01",
            "scope": "Bases de la convocatoria, anexos e identificación de epígrafes del temario",
        },
        "questions": questions,
    }
    OUTPUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Generadas {len(questions)} preguntas en {OUTPUT}")


if __name__ == "__main__":
    main()
