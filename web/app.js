const state = { bank: [], test: [], index: 0, answers: {}, review: {} };
const $ = (id) => document.getElementById(id);

function shuffle(items) {
  return [...items].sort(() => Math.random() - 0.5);
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
  $("next").textContent = state.index === state.test.length - 1 ? "Finalizar" : "Siguiente";
}
function finish() {
  const answered = Object.keys(state.answers).length;
  const pending = state.test.length - answered;
  const reviews = Object.keys(state.review).length;
  $("result-summary").innerHTML = `<p><strong>${answered}</strong> respondidas · <strong>${pending}</strong> sin responder · <strong>${reviews}</strong> marcadas para repasar.</p>
    <p>Estos PDF no contienen plantilla de soluciones, así que el modo actual sirve para practicar y revisar cobertura. El importador ya admite añadir respuestas correctas al JSON más adelante.</p>`;
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
  $("catalog").textContent = `${state.bank.length} preguntas disponibles procedentes de ${data.sources.length} exámenes.`;
}).catch(() => $("catalog").textContent = "No se ha encontrado el banco de preguntas. Ejecuta el importador.");
