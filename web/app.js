const STORAGE = { tests: "tcae-saved-tests", wrong: "tcae-wrong-questions" };
const state = { bank: [], thematicBank: [], test: [], testId: null, index: 0, answers: {}, review: {}, mode: "test" };
const OPPOSITION = { mode: "opposition", totalQuestions: 85, scoredQuestions: 80, reserveQuestions: 5 };
const THEMATIC_MODE = "thematic";
const $ = (id) => document.getElementById(id);

window.setTimeout(() => {
  document.body.classList.remove("is-loading");
  $("loader").setAttribute("aria-hidden", "true");
}, 3000);

function shuffle(items) {
  return [...items].sort(() => Math.random() - 0.5);
}
function readStorage(key, fallback) {
  try { return JSON.parse(localStorage.getItem(key)) || fallback; } catch { return fallback; }
}
function writeStorage(key, value) {
  localStorage.setItem(key, JSON.stringify(value));
}
function savedTests() {
  return readStorage(STORAGE.tests, []);
}
function isOppositionMode() {
  return state.mode === OPPOSITION.mode;
}
function questionById(id) {
  return [...state.bank, ...state.thematicBank].find(question => question.id === id);
}
function escapeHtml(value) {
  return String(value).replace(/[&<>"']/g, character => ({
    "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#039;"
  })[character]);
}
function optionText(question, key) {
  const option = question.options.find(item => item.key === key);
  return option ? `${key.toUpperCase()}) ${option.text}` : "Sin responder";
}
function questionLabel(question) {
  return question.topic || question.source;
}
function sourceLink(question) {
  if (!question.answerSource) return "";
  return ` <a href="${escapeHtml(question.answerSource)}" target="_blank" rel="noopener noreferrer">Consultar fuente</a>.`;
}
function explanation(question) {
  const detail = question.answerSourceDetail
    ? `La referencia verificada corresponde a: ${escapeHtml(question.answerSourceDetail)}.`
    : "La respuesta se ha contrastado con una fuente oficial.";
  return `${detail}${sourceLink(question)}`;
}
function setView(section) {
  ["welcome", "thematic-questions", "quiz", "results", "saved-tests", "wrong-questions"].forEach(id => $(id).hidden = id !== section);
  document.querySelectorAll(".nav-link").forEach(button => button.classList.toggle("active", button.dataset.view === section));
  if (section === "saved-tests") renderSavedTests();
  if (section === "wrong-questions") renderWrongQuestions();
}
function persistCurrentTest(completed = false) {
  if (!state.testId) return;
  const tests = savedTests();
  const existing = tests.find(test => test.id === state.testId);
  if (!existing) return;
  Object.assign(existing, {
    questionIds: state.test.map(question => question.id),
    answers: state.answers,
    review: state.review,
    mode: state.mode,
    index: state.index,
    completed,
    updatedAt: new Date().toISOString()
  });
  writeStorage(STORAGE.tests, tests);
}
function uniqueName(name) {
  return !savedTests().some(test => test.name.toLocaleLowerCase() === name.toLocaleLowerCase());
}
function start() {
  const name = $("test-name").value.trim();
  if (!name) {
    $("start-error").textContent = "Pon un nombre al reto para poder recuperarlo después.";
    return;
  }
  if (!uniqueName(name)) {
    $("start-error").textContent = "Ya existe un reto con ese nombre. Elige otro distinto.";
    return;
  }
  $("start-error").textContent = "";
  const selectedMode = $("test-size").value;
  const size = Math.min(selectedMode === OPPOSITION.mode ? OPPOSITION.totalQuestions : Number(selectedMode), state.bank.length);
  state.test = shuffle(state.bank).slice(0, size);
  state.testId = `${Date.now()}-${Math.random().toString(36).slice(2, 8)}`;
  state.index = 0; state.answers = {}; state.review = {}; state.mode = selectedMode === OPPOSITION.mode ? OPPOSITION.mode : "test";
  const now = new Date().toISOString();
  const tests = savedTests();
  tests.unshift({ id: state.testId, name, questionIds: state.test.map(question => question.id), answers: {}, review: {}, mode: state.mode, index: 0, completed: false, createdAt: now, updatedAt: now });
  writeStorage(STORAGE.tests, tests);
  setView("quiz"); render();
}
function startThematic() {
  const name = $("thematic-test-name").value.trim();
  if (!name) {
    $("thematic-start-error").textContent = "Pon un nombre al reto para poder recuperarlo después.";
    return;
  }
  if (!uniqueName(name)) {
    $("thematic-start-error").textContent = "Ya existe un reto con ese nombre. Elige otro distinto.";
    return;
  }
  if (!state.thematicBank.length) {
    $("thematic-start-error").textContent = "Todavía no hay preguntas nuevas cargadas en el banco por temario.";
    return;
  }
  $("thematic-start-error").textContent = "";
  const selectedSize = $("thematic-test-size").value;
  const size = selectedSize === "all" ? state.thematicBank.length : Math.min(Number(selectedSize), state.thematicBank.length);
  state.test = shuffle(state.thematicBank).slice(0, size);
  state.testId = `${Date.now()}-${Math.random().toString(36).slice(2, 8)}`;
  state.index = 0; state.answers = {}; state.review = {}; state.mode = THEMATIC_MODE;
  const now = new Date().toISOString();
  const tests = savedTests();
  tests.unshift({ id: state.testId, name, questionIds: state.test.map(question => question.id), answers: {}, review: {}, mode: state.mode, index: 0, completed: false, createdAt: now, updatedAt: now });
  writeStorage(STORAGE.tests, tests);
  setView("quiz"); render();
}
function loadTest(id, reviewOnly = false) {
  const saved = savedTests().find(test => test.id === id);
  if (!saved) return;
  state.test = saved.questionIds.map(questionById).filter(Boolean);
  state.testId = saved.id; state.index = saved.index || 0;
  state.answers = saved.answers || {}; state.review = saved.review || {}; state.mode = saved.mode || "test";
  if (reviewOnly) finish(false); else { setView("quiz"); render(); }
}
function render() {
  const question = state.test[state.index];
  if (!question) return;
  $("progress").textContent = `Pregunta ${state.index + 1} de ${state.test.length}`;
  $("answered").textContent = `${Object.keys(state.answers).length} respondidas`;
  $("progress-fill").style.width = `${((state.index + 1) / state.test.length) * 100}%`;
  $("source").textContent = `${questionLabel(question)} · pregunta ${question.number}`;
  $("prompt").textContent = question.prompt;
  $("options").innerHTML = question.options.map(option => `
    <label class="option"><input type="radio" name="answer" value="${option.key}"
      ${state.answers[question.id] === option.key ? "checked" : ""}>
      <strong class="option-key">${option.key.toUpperCase()})</strong><span>${escapeHtml(option.text)}</span></label>`).join("");
  document.querySelectorAll('[name="answer"]').forEach(input => input.addEventListener("change", event => {
    state.answers[question.id] = event.target.value; persistCurrentTest(); render();
  }));
  $("review").checked = Boolean(state.review[question.id]);
  $("previous").disabled = state.index === 0;
  $("next").textContent = state.index === state.test.length - 1 ? "Terminar reto" : "Siguiente";
}
function saveMistakes(mistakes) {
  const wrong = readStorage(STORAGE.wrong, {});
  mistakes.forEach(question => {
    wrong[question.id] = { questionId: question.id, lastAnswer: state.answers[question.id], mode: state.mode, updatedAt: new Date().toISOString() };
  });
  writeStorage(STORAGE.wrong, wrong);
}
function finish(save = true) {
  const answered = Object.keys(state.answers).length;
  const pending = state.test.length - answered;
  const reviews = Object.keys(state.review).length;
  const verified = state.test.filter(question => question.correctAnswer);
  const graded = verified.filter(question => state.answers[question.id]);
  const correct = graded.filter(question => state.answers[question.id] === question.correctAnswer);
  const mistakes = graded.filter(question => state.answers[question.id] !== question.correctAnswer);
  const unverified = state.test.length - verified.length;
  const oppositionPoints = Math.max(0, Math.min(OPPOSITION.scoredQuestions, correct.length - (mistakes.length / 3)));
  const grade = graded.length ? (isOppositionMode()
    ? ((oppositionPoints / OPPOSITION.scoredQuestions) * 10)
    : ((correct.length / graded.length) * 10)).toFixed(2).replace(".", ",") : null;
  const score = graded.length ? `${correct.length} de ${graded.length}` : "Todavía no hay respuestas verificadas contestadas en este test";
  if (save) { saveMistakes(mistakes); persistCurrentTest(true); }
  const oppositionSummary = isOppositionMode() ? `<p><strong>Puntuación de oposición:</strong> ${oppositionPoints.toFixed(2).replace(".", ",")} / ${OPPOSITION.scoredQuestions} puntos.</p>
    <p>Se descuentan <strong>${(mistakes.length / 3).toFixed(2).replace(".", ",")}</strong> puntos por ${mistakes.length} fallos. El reto incluye ${OPPOSITION.reserveQuestions} preguntas de reserva y la puntuación máxima se limita a ${OPPOSITION.scoredQuestions}.</p>` : "";
  $("result-summary").innerHTML = `<p><strong>${answered}</strong> respondidas · <strong>${pending}</strong> sin responder · <strong>${reviews}</strong> marcadas para repasar.</p>
    <p><strong>Resultado verificable:</strong> ${score}.</p>
    <p><strong>Nota:</strong> ${grade === null ? "no disponible" : `${grade} / 10`}.</p>
    ${oppositionSummary}
    <p>La nota se calcula sobre las <strong>${graded.length}</strong> preguntas verificadas que has contestado. Este test contiene <strong>${verified.length}</strong> preguntas con solución investigada en fuentes oficiales y <strong>${unverified}</strong> pendientes de revisión.</p>`;
  $("correct-answers").innerHTML = `<section class="result-block correct-answers"><h3>Preguntas correctas (${correct.length})</h3>
    ${correct.length ? `<ol>${correct.map(question => resultItem(question, true)).join("")}</ol>` : "<p>No has acertado ninguna de las preguntas corregibles.</p>"}</section>`;
  $("mistakes").innerHTML = `<section class="result-block mistakes"><h3>Preguntas falladas (${mistakes.length})</h3>
    ${mistakes.length ? `<ol>${mistakes.map(question => resultItem(question, true)).join("")}</ol>` : "<p>No has fallado ninguna de las preguntas corregibles.</p>"}</section>`;
  $("solutions").innerHTML = `<section class="result-block"><h3>Resolución del cuestionario</h3>
    <ol>${state.test.map(question => resultItem(question, false)).join("")}</ol></section>`;
  setView("results");
}
function printCurrentResults() {
  document.body.classList.add("is-printing-results");
  window.print();
  window.setTimeout(() => document.body.classList.remove("is-printing-results"), 500);
}
function resultItem(question, showUserAnswer) {
  return `<li><p><strong>${escapeHtml(questionLabel(question))} · pregunta ${question.number}</strong></p>
    <p>${escapeHtml(question.prompt)}</p>
    ${showUserAnswer ? `<p><strong>Tu respuesta:</strong> ${escapeHtml(optionText(question, state.answers[question.id]))}</p>` : ""}
    ${question.correctAnswer
      ? `<p><strong>Respuesta correcta:</strong> ${escapeHtml(optionText(question, question.correctAnswer))}</p><p><strong>Explicación:</strong> ${explanation(question)}</p>`
      : "<p><strong>Solución pendiente de revisión.</strong></p>"}</li>`;
}
function renderSavedTests() {
  const tests = savedTests();
  $("saved-tests-list").innerHTML = tests.length ? tests.map(test => {
    const answered = Object.keys(test.answers || {}).length;
    return `<article class="saved-item"><div><h3>${escapeHtml(test.name)}</h3>
      <p>${test.questionIds.length} preguntas${test.mode === OPPOSITION.mode ? " · modo oposición" : ""}${test.mode === THEMATIC_MODE ? " · según temario" : ""} · ${answered} respondidas · ${test.completed ? "Terminado" : "En progreso"}</p></div>
      <div class="item-actions">${test.completed ? `<button class="secondary" data-review-test="${test.id}">Revisar</button><button data-print-test="${test.id}">Imprimir PDF</button>` : `<button data-resume-test="${test.id}">Continuar</button>`}
      <button class="danger" data-delete-test="${test.id}">Eliminar</button></div></article>`;
  }).join("") : '<p class="empty-state">Todavía no has guardado ningún reto.</p>';
}
function renderWrongQuestions() {
  const wrong = Object.values(readStorage(STORAGE.wrong, {})).filter(item => item.mode !== THEMATIC_MODE);
  $("retry-wrong").disabled = !wrong.length;
  $("wrong-questions-list").innerHTML = wrong.length ? `<ol class="wrong-list">${wrong.map(item => {
    const question = questionById(item.questionId);
    return question ? resultItem(question, false) : "";
  }).join("")}</ol>` : '<p class="empty-state">No hay preguntas incorrectas guardadas.</p>';
}
function retryWrong() {
  const ids = Object.values(readStorage(STORAGE.wrong, {})).filter(item => item.mode !== THEMATIC_MODE).map(item => item.questionId);
  state.test = ids.map(questionById).filter(Boolean);
  if (!state.test.length) return;
  state.testId = null; state.index = 0; state.answers = {}; state.review = {}; state.mode = "wrong";
  setView("quiz"); render();
}

$("start-test").addEventListener("click", start);
$("start-thematic-test").addEventListener("click", startThematic);
$("new-test").addEventListener("click", () => setView("welcome"));
$("restart").addEventListener("click", () => setView("welcome"));
$("previous").addEventListener("click", () => { state.index--; persistCurrentTest(); render(); });
$("next").addEventListener("click", () => state.index === state.test.length - 1 ? finish() : (state.index++, persistCurrentTest(), render()));
$("finish").addEventListener("click", () => finish());
$("review").addEventListener("change", event => {
  const id = state.test[state.index].id;
  if (event.target.checked) state.review[id] = true; else delete state.review[id];
  persistCurrentTest();
});
$("retry-wrong").addEventListener("click", retryWrong);
$("print-results").addEventListener("click", printCurrentResults);
document.addEventListener("click", event => {
  const view = event.target.dataset.view;
  if (view) setView(view);
  if (event.target.dataset.resumeTest) loadTest(event.target.dataset.resumeTest);
  if (event.target.dataset.reviewTest) loadTest(event.target.dataset.reviewTest, true);
  if (event.target.dataset.printTest) {
    loadTest(event.target.dataset.printTest, true);
    printCurrentResults();
  }
  if (event.target.dataset.deleteTest) {
    writeStorage(STORAGE.tests, savedTests().filter(test => test.id !== event.target.dataset.deleteTest));
    renderSavedTests();
  }
});
fetch("data/questions.json").then(response => response.json()).then(data => {
  state.bank = data.questions;
  const verified = state.bank.filter(question => question.correctAnswer).length;
  $("catalog").textContent = `${state.bank.length} preguntas disponibles procedentes de ${data.sources.length} exámenes. ${verified} soluciones verificadas en fuentes oficiales.`;
}).catch(() => $("catalog").textContent = "No se ha encontrado el banco de preguntas. Ejecuta el importador.");
fetch("data/thematic-questions.json").then(response => response.json()).then(data => {
  state.thematicBank = data.questions;
  $("thematic-catalog").textContent = `${state.thematicBank.length} preguntas nuevas disponibles según temario.`;
}).catch(() => $("thematic-catalog").textContent = "No se ha encontrado el banco de preguntas nuevas según temario.");
fetch("version.json", { cache: "no-store" }).then(response => response.json()).then(version => {
  $("version").textContent = `Versión ${version.commit} · ${version.deployedAt}`;
}).catch(() => {});
