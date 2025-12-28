import { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { Input } from '../../components/ui/input';
import { Button } from '../../components/ui/button';
import { useAuth } from '../../hooks/useAuth';
import { routes } from '../../config/routes';

export const RegisterPage = () => {
  const navigate = useNavigate();
  const { register, loading } = useAuth();
  const [form, setForm] = useState({ name: '', email: '', password: '' });
  const [error, setError] = useState('');

  const handleChange = (event) => {
    const { name, value } = event.target;
    setForm((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    try {
      await register(form);
      navigate(routes.ONBOARDING_GOAL);
    } catch (err) {
      setError(err.message || 'Unable to register');
    }
  };

  return (
    <div className="min-h-screen bg-background-secondary px-4 py-10">
      <div className="mx-auto max-w-md rounded-3xl bg-white p-8 shadow-lg">
        <h1 className="text-2xl font-semibold text-text-primary">Create your workspace</h1>
        <form className="mt-6 space-y-4" onSubmit={handleSubmit}>
          <Input label="Name" name="name" value={form.name} onChange={handleChange} />
          <Input label="Email" name="email" value={form.email} onChange={handleChange} type="email" />
          <Input
            label="Password"
            name="password"
            value={form.password}
            onChange={handleChange}
            type="password"
          />
          {error && <p className="text-sm text-error">{error}</p>}
          <Button type="submit" className="w-full" disabled={loading}>
            {loading ? 'Creating...' : 'Continue'}
          </Button>
        </form>
        <p className="mt-4 text-center text-sm text-text-secondary">
          Already have an account?{' '}
          <Link to={routes.LOGIN} className="text-primary-600">
            Sign in
          </Link>
        </p>
      </div>
    </div>
  );
};

