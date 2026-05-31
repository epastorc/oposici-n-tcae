const state = { bank: [], test: [], index: 0, answers: {}, review: {} };
const $ = (id) => document.getElementById(id);

window.setTimeout(() => {
  document.body.classList.remove("is-loading");
  $("loader").setAttribute("aria-hidden", "true");
}, 3000);

function shuffle(items) {
  return [...items].sort(() => Math.random() - 0.5);
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
function show(section) {
  ["welcome", "quiz", "results"].forEach(id => $(id).hidden = id !== section);
}
function start() {
  const size = Math.min(Number($("test-size").value), state.bank.length);
  state.test = shuffle(state.bank).slice(0, size);
  state.index = 0; state.answers = {}; state.review = {};
  show("quiz"); render();
}
function render() {
  const question = state.test[state.index];
  $("progress").textContent = `Pregunta ${state.index + 1} de ${state.test.length}`;
  $("answered").textContent = `${Object.keys(state.answers).length} respondidas`;
  $("progress-fill").style.width = `${((state.index + 1) / state.test.length) * 100}%`;
  $("source").textContent = `${question.source} · pregunta ${question.number}`;
  $("prompt").textContent = question.prompt;
  $("options").innerHTML = question.options.map(option => `
    <label class="option"><input type="radio" name="answer" value="${option.key}"
      ${state.answers[question.id] === option.key ? "checked" : ""}>
      <strong class="option-key">${option.key.toUpperCase()})</strong><span>${option.text}</span></label>`).join("");
  document.querySelectorAll('[name="answer"]').forEach(input => input.addEventListener("change", event => {
    state.answers[question.id] = event.target.value; render();
  }));
  $("review").checked = Boolean(state.review[question.id]);
  $("previous").disabled = state.index === 0;
  $("next").textContent = state.index === state.test.length - 1 ? "Terminar reto" : "Siguiente";
}
function finish() {
  const answered = Object.keys(state.answers).length;
  const pending = state.test.length - answered;
  const reviews = Object.keys(state.review).length;
  const verified = state.test.filter(question => question.correctAnswer);
  const graded = verified.filter(question => state.answers[question.id]);
  const correct = graded.filter(question => state.answers[question.id] === question.correctAnswer);
  const mistakes = graded.filter(question => state.answers[question.id] !== question.correctAnswer);
  const unverified = state.test.length - verified.length;
  const grade = graded.length ? ((correct.length / graded.length) * 10).toFixed(2).replace(".", ",") : null;
  const score = graded.length ? `${correct.length} de ${graded.length}` : "Todavía no hay respuestas verificadas contestadas en este test";
  $("result-summary").innerHTML = `<p><strong>${answered}</strong> respondidas · <strong>${pending}</strong> sin responder · <strong>${reviews}</strong> marcadas para repasar.</p>
    <p><strong>Resultado verificable:</strong> ${score}.</p>
    <p><strong>Nota:</strong> ${grade === null ? "no disponible" : `${grade} / 10`}.</p>
    <p>La nota se calcula sobre las <strong>${graded.length}</strong> preguntas verificadas que has contestado. Este test contiene <strong>${verified.length}</strong> preguntas con solución investigada en fuentes oficiales y <strong>${unverified}</strong> pendientes de revisión.</p>`;
  $("mistakes").innerHTML = `<section class="result-block mistakes">
    <h3>Preguntas falladas (${mistakes.length})</h3>
    ${mistakes.length ? `<ol>${mistakes.map(question => `<li>
      <p><strong>${escapeHtml(question.source)} · pregunta ${question.number}</strong></p>
      <p>${escapeHtml(question.prompt)}</p>
      <p><strong>Tu respuesta:</strong> ${escapeHtml(optionText(question, state.answers[question.id]))}</p>
      <p><strong>Respuesta correcta:</strong> ${escapeHtml(optionText(question, question.correctAnswer))}</p>
      <p><strong>Explicación:</strong> ${explanation(question)}</p>
    </li>`).join("")}</ol>` : "<p>No has fallado ninguna de las preguntas corregibles.</p>"}
  </section>`;
  $("solutions").innerHTML = `<section class="result-block">
    <h3>Resolución del cuestionario</h3>
    <ol>${state.test.map(question => `<li>
      <p><strong>${escapeHtml(question.source)} · pregunta ${question.number}</strong></p>
      <p>${escapeHtml(question.prompt)}</p>
      ${question.correctAnswer
        ? `<p><strong>Respuesta correcta:</strong> ${escapeHtml(optionText(question, question.correctAnswer))}</p>
          <p><strong>Explicación:</strong> ${explanation(question)}</p>`
        : "<p><strong>Solución pendiente de revisión.</strong></p>"}
    </li>`).join("")}</ol>
  </section>`;
  show("results");
}
$("start-test").addEventListener("click", start);
$("new-test").addEventListener("click", () => show("welcome"));
$("restart").addEventListener("click", () => show("welcome"));
$("previous").addEventListener("click", () => { state.index--; render(); });
$("next").addEventListener("click", () => state.index === state.test.length - 1 ? finish() : (state.index++, render()));
$("finish").addEventListener("click", finish);
$("review").addEventListener("change", event => {
  const id = state.test[state.index].id;
  if (event.target.checked) state.review[id] = true; else delete state.review[id];
});
fetch("data/questions.json").then(response => response.json()).then(data => {
  state.bank = data.questions;
  const verified = state.bank.filter(question => question.correctAnswer).length;
  $("catalog").textContent = `${state.bank.length} preguntas disponibles procedentes de ${data.sources.length} exámenes. ${verified} soluciones verificadas en fuentes oficiales.`;
}).catch(() => $("catalog").textContent = "No se ha encontrado el banco de preguntas. Ejecuta el importador.");
fetch("version.json", { cache: "no-store" }).then(response => response.json()).then(version => {
  $("version").textContent = `Versión ${version.commit} · ${version.deployedAt}`;
}).catch(() => {});
