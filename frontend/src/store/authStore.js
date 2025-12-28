import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import { authService } from '../services/authService';

/**
 * Authentication store powered by Zustand + persist middleware.
 * The persist helper keeps the token/user in localStorage so reloads stay signed in.
 */
export const authStore = create(
  persist(
    (set, get) => ({
      user: null,
      token: null,
      isAuthenticated: false,
      loading: false,
      error: null,
      login: async (email, password) => {
        set({ loading: true, error: null });
        try {
          const data = await authService.login({ email, password });
          set({
            user: data.user,
            token: data.access_token,
            isAuthenticated: true,
            loading: false,
          });
        } catch (error) {
          set({ loading: false, error: error.message || 'Login failed' });
          throw error;
        }
      },
      register: async (userData) => {
        set({ loading: true, error: null });
        try {
          const data = await authService.register(userData);
          set({
            user: data.user,
            token: data.access_token,
            isAuthenticated: true,
            loading: false,
          });
        } catch (error) {
          set({ loading: false, error: error.message || 'Registration failed' });
          throw error;
        }
      },
      logout: async () => {
        try {
          await authService.logout();
        } catch (error) {
          console.warn('Logout request failed, clearing local state anyway.', error);
        } finally {
          set({ user: null, token: null, isAuthenticated: false });
        }
      },
      refreshToken: async () => {
        const { token } = get();
        if (!token) return null;
        try {
          const data = await authService.refresh();
          set({ token: data.access_token, isAuthenticated: true });
          if (data.user) {
            set({ user: data.user });
          }
          return data.access_token;
        } catch (error) {
          console.error('Unable to refresh token', error);
          set({ user: null, token: null, isAuthenticated: false });
          return null;
        }
      },
      hydrateUser: async () => {
        const { user, token } = get();
        if (!token || user) return;
        try {
          const data = await authService.me();
          set({ user: data });
        } catch (error) {
          console.error('Failed to hydrate user profile', error);
        }
      },
    }),
    {
      name: 'auth-store',
      partialize: (state) => ({
        user: state.user,
        token: state.token,
        isAuthenticated: state.isAuthenticated,
      }),
    },
  ),
);

