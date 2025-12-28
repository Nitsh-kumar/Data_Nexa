import { useEffect, useState } from 'react';

/**
 * Returns a debounced version of the input value. Useful for search boxes and
 * expensive computations you want to delay until the user stops typing.
 */
export function useDebounce(value, delay = 300) {
  const [debouncedValue, setDebouncedValue] = useState(value);

  useEffect(() => {
    const timeout = setTimeout(() => setDebouncedValue(value), delay);
    return () => clearTimeout(timeout);
  }, [value, delay]);

  return debouncedValue;
}

