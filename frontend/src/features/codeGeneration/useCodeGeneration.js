import { useState } from 'react';
import { sleep } from '../../utils/helpers';

export const useCodeGeneration = () => {
  const [code, setCode] = useState('');
  const [isGenerating, setIsGenerating] = useState(false);

  const generateCode = async (analysisId) => {
    if (!analysisId) return;
    setIsGenerating(true);
    // Placeholder: swap with backend call later.
    await sleep(1000);
    setCode(
      `# Remediation script for analysis ${analysisId}\n` +
        "df['email'] = df['email'].str.lower()\n" +
        "df = df.drop_duplicates(subset='customer_id')\n" +
        'print("Dataset cleaned successfully!")\n',
    );
    setIsGenerating(false);
  };

  return { code, isGenerating, generateCode };
};

