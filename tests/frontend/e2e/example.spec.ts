import { test, expect } from "@playwright/test";

test("sample", async ({ page }) => {
  await page.goto("http://localhost:5173");
  expect(page).toBeDefined();
});
