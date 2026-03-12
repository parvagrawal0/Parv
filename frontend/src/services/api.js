import axios from "axios";

// Defaults to the backend dev server (uvicorn) port.
// You can override by setting `API_BASE_URL` at build-time (webpack DefinePlugin or env injection).
const API_BASE_URL = (typeof process !== "undefined" &&
  process.env &&
  process.env.API_BASE_URL) ||
  "http://localhost:8000/api";

const apiClient = axios.create({
  baseURL: API_BASE_URL
});

apiClient.interceptors.request.use((config) => {
  const token = localStorage.getItem("token");
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    const status = error?.response?.status;
    if (status === 401) {
      localStorage.removeItem("token");
      // If the user is in the app, force re-login on auth failures.
      if (typeof window !== "undefined") {
        window.location.href = "/login";
      }
    }
    return Promise.reject(error);
  }
);

export const registerUser = async (data) => {
  const response = await apiClient.post("/auth/register", data);
  return response.data;
};

export const loginUser = async (data) => {
  const response = await apiClient.post("/auth/login", data);
  return response.data;
};

export const fetchNotes = async () => {
  const response = await apiClient.get("/notes");
  return response.data;
};

export const fetchNoteById = async (id) => {
  const response = await apiClient.get(`/notes/${id}`);
  return response.data;
};

export const createNote = async (data) => {
  const response = await apiClient.post("/notes", data);
  return response.data;
};

export const updateNote = async (id, data) => {
  const response = await apiClient.put(`/notes/${id}`, data);
  return response.data;
};

export const deleteNote = async (id) => {
  const response = await apiClient.delete(`/notes/${id}`);
  return response.data;
};

