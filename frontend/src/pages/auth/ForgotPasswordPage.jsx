import { useState } from 'react';
import { Input } from '../../components/ui/input';
import { Button } from '../../components/ui/button';

export const ForgotPasswordPage = () => {
  const [email, setEmail] = useState('');
  const [submitted, setSubmitted] = useState(false);

  const handleSubmit = (event) => {
    event.preventDefault();
    setSubmitted(true);
  };

  return (
    <div className="min-h-screen bg-background-secondary px-4 py-10">
      <div className="mx-auto max-w-md rounded-3xl bg-white p-8 shadow-lg">
        <h1 className="text-2xl font-semibold text-text-primary">Reset password</h1>
        <p className="text-sm text-text-secondary">
          Enter the email linked to your account and we will send a reset link.
        </p>
        <form className="mt-6 space-y-4" onSubmit={handleSubmit}>
          <Input
            label="Email"
            type="email"
            value={email}
            onChange={(event) => setEmail(event.target.value)}
          />
          <Button type="submit" className="w-full">
            Send reset link
          </Button>
        </form>
        {submitted && (
          <p className="mt-4 text-sm text-success">
            Check your inbox (and spam folder) for the reset instructions.
          </p>
        )}
      </div>
    </div>
  );
};

