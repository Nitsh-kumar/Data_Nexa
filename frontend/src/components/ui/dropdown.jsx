import { useState } from 'react';
import { cn } from '../../utils/helpers';

/**
 * Lightweight dropdown used for filters and simple menus.
 */
export const Dropdown = ({ label, items = [], onSelect }) => {
  const [open, setOpen] = useState(false);

  return (
    <div className="relative inline-block text-left">
      <button
        type="button"
        onClick={() => setOpen((prev) => !prev)}
        className="inline-flex items-center gap-2 rounded-lg border border-gray-200 bg-white px-4 py-2 text-sm font-medium text-text-primary shadow-sm hover:bg-gray-50"
      >
        {label}
        <span className="text-text-tertiary">{open ? '▴' : '▾'}</span>
      </button>

      {open && (
        <div className="absolute right-0 z-10 mt-2 w-48 rounded-lg border border-gray-200 bg-white p-2 shadow-lg">
          {items.map((item) => (
            <button
              key={item.value}
              type="button"
              className={cn(
                'w-full rounded-md px-3 py-2 text-left text-sm text-text-secondary hover:bg-background-tertiary',
                item.active && 'bg-primary-50 text-primary-600',
              )}
              onClick={() => {
                onSelect?.(item.value);
                setOpen(false);
              }}
            >
              {item.label}
            </button>
          ))}
        </div>
      )}
    </div>
  );
};

