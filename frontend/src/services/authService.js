import api from './api';

/**
 * Auth service centralizes every call related to authentication so the stores
 * can stay lean and testable.
 */
export const authService = {
  login: async (payload) => {
    const response = await api.post('/auth/login', payload);
    return response.data;
  },
  register: async (payload) => {
    const response = await api.post('/auth/register', payload);
    return response.data;
  },
  logout: async () => {
    const response = await api.post('/auth/logout');
    return response.data;
  },
  refresh: async () => {
    const response = await api.post('/auth/refresh-token');
    return response.data;
  },
  me: async () => {
    const response = await api.get('/auth/me');
    return response.data;
  },
};

