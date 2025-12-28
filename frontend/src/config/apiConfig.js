export const API_CONFIG = {
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1',
  timeouts: {
    default: 30000,
  },
};

