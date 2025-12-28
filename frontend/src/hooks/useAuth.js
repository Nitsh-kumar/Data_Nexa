import { useEffect } from 'react';
import { authStore } from '../store/authStore';

/**
 * Convenience hook that exposes auth state/actions with one import.
 * It also attempts to hydrate the user profile on mount when a token exists.
 */
export function useAuth() {
  const { user, token, isAuthenticated, loading, error, login, register, logout, hydrateUser } =
    authStore((state) => ({
      user: state.user,
      token: state.token,
      isAuthenticated: state.isAuthenticated,
      loading: state.loading,
      error: state.error,
      login: state.login,
      register: state.register,
      logout: state.logout,
      hydrateUser: state.hydrateUser,
    }));

  useEffect(() => {
    hydrateUser();
  }, [hydrateUser]);

  return { user, token, isAuthenticated, loading, error, login, register, logout };
}

