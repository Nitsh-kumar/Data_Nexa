import { create } from 'zustand';
import { analysisService } from '../services/analysisService';

const defaultState = {
  currentAnalysis: null,
  status: 'idle', // idle, processing, completed, error
  results: null,
  insights: [],
  error: null,
};

export const analysisStore = create((set, get) => ({
  ...defaultState,
  startAnalysis: async (datasetId, goal) => {
    set({ status: 'processing', error: null });
    try {
      const analysis = await analysisService.startAnalysis(datasetId, goal);
      set({ currentAnalysis: analysis, status: analysis.status || 'processing' });
      return analysis;
    } catch (error) {
      set({ status: 'error', error: error.message || 'Unable to start analysis' });
      throw error;
    }
  },
  pollStatus: async (analysisId) => {
    if (!analysisId) throw new Error('analysisId is required');
    try {
      const statusPayload = await analysisService.getStatus(analysisId);
      set({ status: statusPayload.status });
      if (statusPayload.status === 'completed') {
        await get().getResults(analysisId);
      }
      return statusPayload;
    } catch (error) {
      set({ status: 'error', error: error.message || 'Polling failed' });
      throw error;
    }
  },
  getResults: async (analysisId) => {
    try {
      const [results, insights] = await Promise.all([
        analysisService.getResults(analysisId),
        analysisService.getInsights(analysisId),
      ]);
      set({ results, insights });
      return { results, insights };
    } catch (error) {
      set({ status: 'error', error: error.message || 'Fetching results failed' });
      throw error;
    }
  },
  reset: () => set({ ...defaultState }),
}));

