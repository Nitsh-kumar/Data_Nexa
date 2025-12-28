import { useState } from 'react';
import { Button } from '../../components/ui/button';
import { Input } from '../../components/ui/input';
import { useNavigate } from 'react-router-dom';
import { routes } from '../../config/routes';

export const TeamSetupPage = () => {
  const [emails, setEmails] = useState(['']);
  const navigate = useNavigate();

  const handleChange = (index, value) => {
    setEmails((prev) => prev.map((email, idx) => (idx === index ? value : email)));
  };

  const addEmail = () => setEmails((prev) => [...prev, '']);

  const handleContinue = () => {
    navigate(routes.DASHBOARD);
  };

  return (
    <div className="min-h-screen bg-background-secondary px-4 py-10">
      <div className="mx-auto max-w-2xl space-y-6">
        <div>
          <h1 className="text-3xl font-semibold text-text-primary">Invite your teammates</h1>
          <p className="text-text-secondary">They will receive an email with onboarding steps.</p>
        </div>
        <div className="space-y-3">
          {emails.map((email, index) => (
            <Input
              key={index}
              label={`Teammate ${index + 1}`}
              type="email"
              value={email}
              onChange={(event) => handleChange(index, event.target.value)}
            />
          ))}
          <Button variant="secondary" onClick={addEmail}>
            + Add another teammate
          </Button>
        </div>
        <Button onClick={handleContinue}>Go to dashboard</Button>
      </div>
    </div>
  );
};

