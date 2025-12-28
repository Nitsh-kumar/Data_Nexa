import { cn } from '../../utils/helpers';

export const Progress = ({ value = 0, className }) => (
  <div className={cn('h-2 w-full rounded-full bg-gray-100', className)}>
    <div
      className="h-full rounded-full bg-primary-500 transition-all"
      style={{ width: `${value}%` }}
    />
  </div>
);

