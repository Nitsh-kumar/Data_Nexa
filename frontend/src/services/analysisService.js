import api from './api';

export const analysisService = {
  startAnalysis: async (datasetId, goalType) => {
    const response = await api.post('/analysis/start', {
      dataset_id: datasetId,
      goal_type: goalType,
    });
    return response.data;
  },
  getStatus: async (analysisId) => {
    const response = await api.get(`/analysis/${analysisId}/status`);
    return response.data;
  },
  getResults: async (analysisId) => {
    const response = await api.get(`/analysis/${analysisId}/results`);
    return response.data;
  },
  getInsights: async (analysisId) => {
    const response = await api.get(`/insights/${analysisId}`);
    return response.data;
  },
};

