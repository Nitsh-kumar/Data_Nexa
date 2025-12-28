import { useEffect, useState } from 'react';
import { analysisService } from '../services/analysisService';

/**
 * Polls the backend every 3 seconds for updated analysis status and results.
 * Returns the status/results tuple so components can render accordingly.
 */
export function useAnalysisPolling(analysisId, options = {}) {
  const [status, setStatus] = useState('processing');
  const [results, setResults] = useState(null);
  const pollingInterval = options.interval || 3000;

  useEffect(() => {
    if (!analysisId) return undefined;

    let isCancelled = false;
    const intervalId = setInterval(async () => {
      try {
        const statusResponse = await analysisService.getStatus(analysisId);
        if (isCancelled) return;
        setStatus(statusResponse.status);

        if (statusResponse.status === 'completed') {
          const fetchedResults = await analysisService.getResults(analysisId);
          if (!isCancelled) {
            setResults(fetchedResults);
            clearInterval(intervalId);
          }
        }
      } catch (error) {
        console.error('Polling error', error);
      }
    }, pollingInterval);

    return () => {
      isCancelled = true;
      clearInterval(intervalId);
    };
  }, [analysisId, pollingInterval]);

  return { status, results };
}

