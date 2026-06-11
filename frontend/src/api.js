import axios from "axios";

export const API_BASE_URL = "https://careermail-ai-backend.onrender.com";

export function getAuthHeaders() {
  const token = localStorage.getItem("gmail_token");

  if (!token) {
    return {};
  }

  return {
    Authorization: `Bearer ${token}`,
  };
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