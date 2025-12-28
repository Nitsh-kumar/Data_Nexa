import { forwardRef } from 'react';
import { cn } from '../../utils/helpers';

export const Input = forwardRef(({ className, label, error, helperText, ...props }, ref) => (
  <label className="flex flex-col gap-1 text-sm text-text-secondary">
    {label && <span className="font-medium text-text-primary">{label}</span>}
    <input
      ref={ref}
      className={cn(
        'h-11 rounded-lg border border-gray-200 px-3 text-text-primary focus:border-primary-500 focus:ring-2 focus:ring-primary-100 outline-none transition placeholder:text-text-tertiary',
        error && 'border-error focus:ring-error/20',
        className,
      )}
      {...props}
    />
    {helperText && !error && <span>{helperText}</span>}
    {error && <span className="text-error text-xs">{error}</span>}
  </label>
));

Input.displayName = 'Input';

