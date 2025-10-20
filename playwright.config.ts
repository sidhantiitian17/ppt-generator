import { defineConfig } from "@playwright/test";

export default defineConfig({
  testDir: "tests/frontend/e2e",
  use: {
    baseURL: "http://localhost:5173",
  },
});
