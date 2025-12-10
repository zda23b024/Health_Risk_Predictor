import axios from "axios";

const API_URL = process.env.REACT_APP_API_URL || "http://localhost:5000";

export const getHealthEntries = (days = 7) => {
  return axios.get(`${API_URL}/health`, {
    params: { days },
  });
};

export const addHealthEntry = (entry) => {
  // entry = { weight, steps, water_intake, sleep_hours, entry_date? }
  return axios.post(`${API_URL}/health`, entry);
};
