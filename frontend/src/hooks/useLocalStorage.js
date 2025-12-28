import { useEffect, useState } from 'react';

/**
 * Syncs a state value with localStorage. Great for UI preferences or cached filters.
 */
export function useLocalStorage(key, initialValue) {
  const [storedValue, setStoredValue] = useState(() => {
    try {
      const item = window.localStorage.getItem(key);
      return item ? JSON.parse(item) : initialValue;
    } catch (error) {
      console.warn('Unable to read localStorage', error);
      return initialValue;
    }
  });

  useEffect(() => {
    try {
      window.localStorage.setItem(key, JSON.stringify(storedValue));
    } catch (error) {
      console.warn('Unable to write to localStorage', error);
    }
  }, [key, storedValue]);

  return [storedValue, setStoredValue];
}

