import api from './api';

export const datasetService = {
  upload: async (formData) => {
    const response = await api.post('/datasets/upload', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
    return response.data;
  },
  list: async () => {
    const response = await api.get('/datasets');
    return response.data;
  },
  detail: async (datasetId) => {
    const response = await api.get(`/datasets/${datasetId}`);
    return response.data;
  },
};

