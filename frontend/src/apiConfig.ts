// Auto-generated API configuration
export const API_BASE_URL: string = import.meta.env.DEV
  ? import.meta.env.VITE_USE_GO_BACKEND === "true"
    ? "http://127.0.0.1:8080" // Go backend on port 8080
    : "http://127.0.0.1:5001" // Python Flask backend on port 5001 (default)
  : window.location.origin; // Uses the current domain in production
