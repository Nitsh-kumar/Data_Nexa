import { useState } from 'react';

export const Tooltip = ({ children, label }) => {
  const [open, setOpen] = useState(false);
  return (
    <span
      className="relative inline-flex"
      onMouseEnter={() => setOpen(true)}
      onMouseLeave={() => setOpen(false)}
    >
      {children}
      {open && (
        <span className="absolute bottom-full left-1/2 -translate-x-1/2 -translate-y-2 rounded-md bg-text-primary px-2 py-1 text-xs text-white">
          {label}
        </span>
      )}
    </span>
  );
};

