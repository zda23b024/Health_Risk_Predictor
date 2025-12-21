import axios from "axios";

const API_URL = process.env.REACT_APP_API_URL || "http://localhost:5000";

// Single axios instance so we can attach auth token automatically
const api = axios.create({ baseURL: API_URL });

api.interceptors.request.use((config) => {
  const token = localStorage.getItem("token");
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export const getHealthEntries = (days = 7) => {
  return api.get(`/health`, {
    params: { days },
  });
};

export const addHealthEntry = (entry) => {
  // entry = { weight, steps, water_intake, sleep_hours, entry_date? }
  return api.post(`/health`, entry);
};

// =========================
// Module 2 – Stats API
// =========================
export const getHealthStats = (days = 7) => {
  return api.get(`/health/stats`, {
    params: { days },
  });
};

// =========================
// Module 3 – Prediction API
// =========================
export const predictHealthRisk = (payload) => {
  // payload = { weight, height, steps, water_intake, sleep_hours }
  return api.post(`/health/predict`, payload);
};

// =========================
// Auth API
// =========================
export const registerUser = (payload) => {
  return api.post(`/auth/register`, payload);
};

export const loginUser = (payload) => {
  return api.post(`/auth/login`, payload);
};

export const resendVerification = (payload) => {
  return api.post(`/auth/resend-verification`, payload);
};

export const getMe = () => {
  return api.get(`/auth/me`);
};
