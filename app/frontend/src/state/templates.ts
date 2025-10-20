import { create } from "zustand";

import { Template } from "../types";

interface TemplateState {
  templates: Template[];
  addTemplate: (template: Template) => void;
}

export const useTemplateStore = create<TemplateState>((set) => ({
  templates: [],
  addTemplate: (template) =>
    set((state) => ({ templates: [...state.templates, template] })),
}));
