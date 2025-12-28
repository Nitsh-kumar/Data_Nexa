import axios from 'axios';
import { authStore } from '../store/authStore';

// Axios singleton used across services. It automatically sends the auth token
// and attempts a silent refresh whenever a 401 response is detected.
const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1',
  timeout: 30000,
});

api.interceptors.request.use((config) => {
  const token = authStore.getState().token;
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

api.interceptors.response.use(
  (response) => response,
  async (error) => {
    if (error.response?.status === 401) {
      // Token might be expired; attempt a refresh then retry once.
      try {
        await authStore.getState().refreshToken();
      } catch (refreshError) {
        console.error('Token refresh failed', refreshError);
      }
    }
    return Promise.reject(error);
  },
);

export default api;

