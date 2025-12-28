import { Link } from 'react-router-dom';
import { useAuth } from '../../hooks/useAuth';
import { routes } from '../../config/routes';
import { Button } from '../ui/button';

export const Header = () => {
  const { user, logout } = useAuth();

  return (
    <header className="sticky top-0 z-20 flex items-center justify-between border-b border-gray-100 bg-white px-4 py-4 shadow-sm md:px-8 lg:px-10">
      <div>
        <p className="text-sm text-text-tertiary">Welcome back</p>
        <h1 className="text-2xl font-semibold text-text-primary">
          {user?.name || 'Analyst'}
        </h1>
      </div>
      <div className="flex items-center gap-3">
        <Link to={routes.SETTINGS_PROFILE} className="text-sm text-primary-600">
          Settings
        </Link>
        <Button variant="secondary" onClick={logout}>
          Logout
        </Button>
      </div>
    </header>
  );
};

