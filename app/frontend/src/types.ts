export type PlaceholderType =
  | "text"
  | "image"
  | "chart"
  | "table"
  | "bullet_list"
  | "quote";

export interface Placeholder {
  id: string;
  type: PlaceholderType;
  x: number;
  y: number;
  width: number;
  height: number;
  rotation: number;
  content?: string;
}

export interface Slide {
  id: string;
  title?: string;
  layout: string;
  placeholders: Placeholder[];
  notes?: string;
}

export interface Deck {
  id: string;
  name: string;
  slides: Slide[];
}

export interface Template {
  id: string;
  name: string;
  slides: Slide[];
}
