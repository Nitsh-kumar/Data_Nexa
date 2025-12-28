import { useMemo } from 'react';
import { analysisStore } from '../store/analysisStore';

export function useAnalysis() {
  const state = analysisStore((storeState) => storeState);

  return useMemo(
    () => ({
      currentAnalysis: state.currentAnalysis,
      status: state.status,
      results: state.results,
      insights: state.insights,
      error: state.error,
      startAnalysis: state.startAnalysis,
      pollStatus: state.pollStatus,
      getResults: state.getResults,
      reset: state.reset,
    }),
    [state],
  );
}

