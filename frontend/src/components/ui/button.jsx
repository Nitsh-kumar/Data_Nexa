import { forwardRef } from 'react';
import { cn } from '../../utils/helpers';

const baseStyles =
  'inline-flex items-center justify-center rounded-lg font-medium transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-offset-2 disabled:opacity-50 disabled:pointer-events-none';

const variants = {
  primary: 'bg-primary-600 text-white hover:bg-primary-700 focus-visible:ring-primary-500',
  secondary:
    'bg-background-tertiary text-text-primary hover:bg-background-tertiary/80 focus-visible:ring-primary-100',
  ghost: 'bg-transparent text-text-secondary hover:text-text-primary hover:bg-gray-100',
};

/**
 * Shared button component modeled after shadcn/ui's API.
 */
export const Button = forwardRef(
  ({ asChild, className, variant = 'primary', children, ...props }, ref) => {
    const Component = asChild ? 'span' : 'button';
    return (
      <Component ref={ref} className={cn(baseStyles, variants[variant], className)} {...props}>
        {children}
      </Component>
    );
  },
);

Button.displayName = 'Button';

