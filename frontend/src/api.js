import axios from "axios";

export const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";

export function getAuthHeaders() {
  const demoSelected = localStorage.getItem("careermail_demo") === "true";
  if (demoSelected) return {};
  const token = localStorage.getItem("gmail_token");
  return token ? { Authorization: `Bearer ${token}` } : {};
}

export const api = axios.create({
  baseURL: API_BASE_URL,
  withCredentials: true,
});

api.interceptors.request.use((config) => {
  config.headers = {
    ...config.headers,
    ...getAuthHeaders(),
  };
  return config;
});
