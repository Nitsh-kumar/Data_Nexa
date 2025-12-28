import { useState } from 'react';
import { Button } from '../../components/ui/button';
import { useUpload } from '../../hooks/useUpload';
import { useNavigate } from 'react-router-dom';
import { routes } from '../../config/routes';

const goals = [
  { id: 'data_quality', label: 'Improve Data Quality', description: 'Detect anomalies & nulls' },
  { id: 'governance', label: 'Compliance & Governance', description: 'Track PII exposure' },
  { id: 'ai', label: 'AI Readiness', description: 'Validate training datasets' },
];

export const GoalSelectionPage = () => {
  const { setGoal } = useUpload();
  const [selectedGoal, setSelectedGoal] = useState('');
  const navigate = useNavigate();

  const handleContinue = () => {
    if (selectedGoal) {
      setGoal(selectedGoal);
      navigate(routes.ONBOARDING_TEAM);
    }
  };

  return (
    <div className="min-h-screen bg-background-secondary px-4 py-10">
      <div className="mx-auto max-w-3xl space-y-6">
        <div>
          <h1 className="text-3xl font-semibold text-text-primary">What brings you here?</h1>
          <p className="text-text-secondary">Pick a goal so we can tailor your workspace.</p>
        </div>
        <div className="grid gap-4 md:grid-cols-3">
          {goals.map((goal) => (
            <button
              key={goal.id}
              type="button"
              onClick={() => setSelectedGoal(goal.id)}
              className={`rounded-2xl border p-4 text-left ${
                selectedGoal === goal.id
                  ? 'border-primary-500 bg-primary-50'
                  : 'border-gray-200 bg-white'
              }`}
            >
              <p className="text-lg font-semibold text-text-primary">{goal.label}</p>
              <p className="text-sm text-text-secondary">{goal.description}</p>
            </button>
          ))}
        </div>
        <Button disabled={!selectedGoal} onClick={handleContinue}>
          Continue
        </Button>
      </div>
    </div>
  );
};

