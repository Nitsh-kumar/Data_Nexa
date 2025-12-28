import { useEffect, useState } from 'react';
import { analysisService } from '../../services/analysisService';

export const useInsights = (analysisId) => {
  const [insights, setInsights] = useState([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (!analysisId) return;
    let active = true;
    setLoading(true);

    analysisService
      .getInsights(analysisId)
      .then((data) => {
        if (active) setInsights(data);
      })
      .finally(() => active && setLoading(false));

    return () => {
      active = false;
    };
  }, [analysisId]);

  return { insights, loading };
};

