import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const reviewCode = async (code, language) => {
  const response = await api.post('/api/review', { code, language });
  return response.data;
};

export const explainCode = async (code, language) => {
  const response = await api.post('/api/explain', { code, language });
  return response.data;
};

export const optimizeCode = async (code, language) => {
  const response = await api.post('/api/optimize', { code, language });
  return response.data;
};

export default api;