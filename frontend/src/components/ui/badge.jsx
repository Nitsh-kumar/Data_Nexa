import { cn } from '../../utils/helpers';

const styles = {
  default: 'bg-gray-100 text-text-secondary',
  success: 'bg-success/10 text-success',
  warning: 'bg-warning/10 text-warning',
  critical: 'bg-critical/10 text-critical',
};

export const Badge = ({ children, variant = 'default', className }) => (
  <span
    className={cn(
      'inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-medium',
      styles[variant],
      className,
    )}
  >
    {children}
  </span>
);

