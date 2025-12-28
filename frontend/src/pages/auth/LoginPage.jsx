import { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { useAuth } from '../../hooks/useAuth';
import { Input } from '../../components/ui/input';
import { Button } from '../../components/ui/button';
import { SocialAuthButtons } from '../../components/auth/SocialAuthButtons';
import { routes } from '../../config/routes';

export const LoginPage = () => {
  const { login, loading } = useAuth();
  const navigate = useNavigate();
  const [form, setForm] = useState({ email: '', password: '' });
  const [error, setError] = useState('');

  const handleChange = (event) => {
    const { name, value } = event.target;
    setForm((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    try {
      await login(form.email, form.password);
      navigate(routes.DASHBOARD);
    } catch (err) {
      setError(err.message || 'Unable to login');
    }
  };

  return (
    <div className="min-h-screen bg-background-secondary px-4 py-10">
      <div className="mx-auto max-w-md rounded-3xl bg-white p-8 shadow-lg">
        <h1 className="text-2xl font-semibold text-text-primary">Sign in</h1>
        <p className="text-sm text-text-secondary">Access your data workspace.</p>
        <form className="mt-6 space-y-4" onSubmit={handleSubmit}>
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
            {loading ? 'Signing in…' : 'Continue'}
          </Button>
        </form>
        <div className="mt-6">
          <SocialAuthButtons />
        </div>
        <div className="mt-6 flex justify-between text-sm text-text-secondary">
          <Link to={routes.FORGOT_PASSWORD}>Forgot password?</Link>
          <Link to={routes.REGISTER} className="text-primary-600">
            Create account
          </Link>
        </div>
      </div>
    </div>
  );
};

