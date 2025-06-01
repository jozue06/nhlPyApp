/// <reference types="vite/client" />

interface ImportMetaEnv {
  readonly VITE_USE_GO_BACKEND?: string;
  // Add other env variables here as needed
}

interface ImportMeta {
  readonly env: ImportMetaEnv;
}
