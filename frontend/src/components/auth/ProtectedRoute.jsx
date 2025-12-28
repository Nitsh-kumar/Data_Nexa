import { Navigate, Outlet } from 'react-router-dom';
import { useAuth } from '../../hooks/useAuth';
import { routes } from '../../config/routes';

/**
 * Wraps authenticated routes. If the user is not logged in, redirect to /login.
 */
export const ProtectedRoute = () => {
  const { isAuthenticated, loading } = useAuth();

  if (loading) {
    return <div className="p-6 text-center text-sm text-text-secondary">Checking access…</div>;
  }

  return isAuthenticated ? <Outlet /> : <Navigate to={routes.LOGIN} replace />;
};

