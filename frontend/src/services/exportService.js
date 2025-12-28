import api from './api';

export const exportService = {
  downloadReport: async (analysisId) => {
    const response = await api.get(`/analysis/${analysisId}/report`, {
      responseType: 'blob',
    });
    return response.data;
  },
  downloadDataset: async (datasetId) => {
    const response = await api.get(`/datasets/${datasetId}/export`, {
      responseType: 'blob',
    });
    return response.data;
  },
};

