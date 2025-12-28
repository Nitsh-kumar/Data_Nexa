export const required = (value) => (value ? null : 'This field is required');

export const isEmail = (value) => {
  if (!value) return 'Email is required';
  return /\S+@\S+\.\S+/.test(value) ? null : 'Enter a valid email';
};

export const isStrongPassword = (value) => {
  if (!value) return 'Password is required';
  const strong = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{8,}$/;
  return strong.test(value)
    ? null
    : 'Use 8+ chars with uppercase, lowercase, and a number';
};

