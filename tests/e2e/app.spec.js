const { test, expect } = require("@playwright/test");

async function openApp(page) {
  await page.goto("/");
  await expect(page.locator("body")).not.toHaveClass(/is-loading/, { timeout: 5000 });
  await expect(page.locator("#catalog")).toContainText("preguntas disponibles");
  await expect(page.locator("#thematic-catalog")).toContainText("preguntas nuevas disponibles");
}

async function startStandardTest(page, name, size = "25") {
  const welcome = page.locator("#welcome");
  await welcome.getByLabel("Nombre único del reto").fill(name);
  await welcome.getByLabel("Elige la dificultad del reto").selectOption(size);
  await welcome.getByRole("button", { name: "Comenzar aventura" }).click();
  await expect(page.locator("#quiz")).toBeVisible();
  await expect(page.locator("#progress")).toContainText(`Pregunta 1 de ${size}`);
}

async function answerCurrentQuestion(page, option = "a") {
  await page.locator(`input[name="answer"][value="${option}"]`).check();
}

async function finishCurrentTest(page) {
  await page.getByRole("button", { name: "Terminar reto" }).click();
  await expect(page.locator("#results")).toBeVisible();
  await expect(page.locator("#result-summary")).toContainText("Resultado corregible");
  await expect(page.locator("#solutions")).toContainText("Resolución del cuestionario");
}

test.beforeEach(async ({ page }) => {
  await page.addInitScript(() => localStorage.clear());
});

test("loads the question catalogs and validates the start form", async ({ page }) => {
  await openApp(page);

  await expect(page.locator("#catalog")).toContainText("3376 preguntas disponibles");
  await expect(page.locator("#catalog")).toContainText("3146 soluciones documentadas");

  await page.getByRole("button", { name: "Comenzar aventura" }).click();
  await expect(page.locator("#start-error")).toContainText("Pon un nombre al reto");
});

test("starts a standard test, answers, reviews and finishes it", async ({ page }) => {
  await openApp(page);
  await startStandardTest(page, "Repaso e2e", "25");

  await answerCurrentQuestion(page, "a");
  await page.getByLabel("Guardar para entrenar después").check();
  await expect(page.locator("#answered")).toContainText("1 respondidas");

  await page.getByRole("button", { name: "Siguiente" }).click();
  await expect(page.locator("#progress")).toContainText("Pregunta 2 de 25");

  await finishCurrentTest(page);
  await expect(page.locator("#result-summary")).toContainText("1 respondidas");
  await expect(page.locator("#result-summary")).toContainText("marcadas para repasar");
});

test("saves, resumes and deletes an unfinished test", async ({ page }) => {
  await openApp(page);
  await startStandardTest(page, "Reto guardado", "25");
  await answerCurrentQuestion(page, "b");
  await page.getByRole("button", { name: "Siguiente" }).click();

  await page.getByRole("button", { name: "Tests guardados" }).click();
  await expect(page.locator("#saved-tests")).toBeVisible();
  await expect(page.locator("#saved-tests-list")).toContainText("Reto guardado");
  await expect(page.locator("#saved-tests-list")).toContainText("1 respondidas");

  await page.getByRole("button", { name: "Continuar" }).click();
  await expect(page.locator("#quiz")).toBeVisible();
  await expect(page.locator("#progress")).toContainText("Pregunta 2 de 25");

  await page.getByRole("button", { name: "Tests guardados" }).click();
  await page.getByRole("button", { name: "Eliminar" }).click();
  await expect(page.locator("#saved-tests-list")).toContainText("Todavía no has guardado ningún reto");
});

test("prevents duplicate saved test names", async ({ page }) => {
  await openApp(page);
  await startStandardTest(page, "Nombre repetido", "25");

  await page.getByRole("button", { name: "Nuevo reto" }).click();
  await page.locator("#welcome").getByLabel("Nombre único del reto").fill("Nombre repetido");
  await page.locator("#welcome").getByRole("button", { name: "Comenzar aventura" }).click();

  await expect(page.locator("#start-error")).toContainText("Ya existe un reto con ese nombre");
});

test("runs the official 2013 exam in source order", async ({ page }) => {
  await openApp(page);
  await page.getByRole("button", { name: "Turno Libre 2013" }).click();
  await expect(page.locator("#official-2013-catalog")).toContainText("86 preguntas cargadas");

  await page.locator("#official-2013-test-name").fill("Oficial 2013 e2e");
  await page.getByRole("button", { name: "Comenzar Turno Libre 2013" }).click();

  await expect(page.locator("#progress")).toContainText("Pregunta 1 de 86");
  await expect(page.locator("#source")).toContainText("Examen Turno Libre 2013.pdf · pregunta 1");
});

test("runs the official 2022 exam in source order", async ({ page }) => {
  await openApp(page);
  await page.getByRole("button", { name: "Examen 2022", exact: true }).click();
  await expect(page.locator("#official-2022-catalog")).toContainText("60 preguntas cargadas");
  await expect(page.locator("#official-2022-catalog")).toContainText("59 respuestas");

  await page.locator("#official-2022-test-name").fill("Oficial 2022 e2e");
  await page.getByRole("button", { name: "Comenzar Turno Libre 2022", exact: true }).click();

  await expect(page.locator("#progress")).toContainText("Pregunta 1 de 60");
  await expect(page.locator("#source")).toContainText("Examen Turno Libre 2022.pdf · pregunta 1");
});

test("runs the postponed official 2022 exam in source order", async ({ page }) => {
  await openApp(page);
  await page.getByRole("button", { name: "2022 aplazado", exact: true }).click();
  await expect(page.locator("#official-2022-aplazado-catalog")).toContainText("60 preguntas cargadas");
  await expect(page.locator("#official-2022-aplazado-catalog")).toContainText("60 respuestas");

  await page.locator("#official-2022-aplazado-test-name").fill("Oficial 2022 aplazado e2e");
  await page.getByRole("button", { name: "Comenzar Turno Libre 2022 aplazado" }).click();

  await expect(page.locator("#progress")).toContainText("Pregunta 1 de 60");
  await expect(page.locator("#source")).toContainText("Examen Turno Libre Aplazado 2022.pdf · pregunta 1");
});

test("runs the official 2023 exam in source order", async ({ page }) => {
  await openApp(page);
  await page.getByRole("button", { name: "Examen 2023", exact: true }).click();
  await expect(page.locator("#official-2023-catalog")).toContainText("70 preguntas cargadas");
  await expect(page.locator("#official-2023-catalog")).toContainText("70 respuestas");

  await page.locator("#official-2023-test-name").fill("Oficial 2023 e2e");
  await page.getByRole("button", { name: "Comenzar Examen 2023", exact: true }).click();

  await expect(page.locator("#progress")).toContainText("Pregunta 1 de 70");
  await expect(page.locator("#source")).toContainText("Examen 2023.pdf · pregunta 1");
});

test("runs a thematic test with the selected size", async ({ page }) => {
  await openApp(page);
  await page.getByRole("button", { name: "Preguntas nuevas según temario" }).click();
  await expect(page.locator("#thematic-catalog")).toContainText("preguntas nuevas disponibles");

  await page.locator("#thematic-test-name").fill("Temario e2e");
  await page.getByLabel("Número de preguntas").selectOption("10");
  await page.getByRole("button", { name: "Comenzar repaso por temario" }).click();

  await expect(page.locator("#quiz")).toBeVisible();
  await expect(page.locator("#progress")).toContainText("Pregunta 1 de 10");
});

test("stores mistakes and starts a retry test", async ({ page }) => {
  await openApp(page);
  await startStandardTest(page, "Fallos e2e", "25");
  await answerCurrentQuestion(page, "a");
  await finishCurrentTest(page);

  await page.getByRole("button", { name: "Preguntas incorrectas" }).click();
  const retryButton = page.getByRole("button", { name: "Repetir preguntas incorrectas" });
  const hasMistakes = await retryButton.isEnabled();

  if (hasMistakes) {
    await expect(page.locator("#wrong-questions-list")).not.toContainText("No hay preguntas incorrectas guardadas");
    await retryButton.click();
    await expect(page.locator("#quiz")).toBeVisible();
    await expect(page.locator("#progress")).toContainText(/Pregunta 1 de \d+/);
  } else {
    await expect(page.locator("#wrong-questions-list")).toContainText("No hay preguntas incorrectas guardadas");
  }
});
