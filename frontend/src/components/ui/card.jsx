import { cn } from '../../utils/helpers';

export const Card = ({ className, children, ...props }) => (
  <div className={cn('card p-4 md:p-6', className)} {...props}>
    {children}
  </div>
);

export const CardHeader = ({ className, children }) => (
  <div className={cn('mb-4 flex items-start justify-between gap-2', className)}>{children}</div>
);

export const CardTitle = ({ className, children }) => (
  <h3 className={cn('text-lg font-semibold text-text-primary', className)}>{children}</h3>
);

export const CardContent = ({ className, children }) => (
  <div className={cn('text-sm text-text-secondary space-y-3', className)}>{children}</div>
);

export const CardFooter = ({ className, children }) => (
  <div className={cn('mt-4 flex items-center justify-end gap-3', className)}>{children}</div>
);

