import { Button } from '../ui/button';

export const EmptyState = ({ title, description, actionLabel, onAction }) => (
  <div className="rounded-2xl border border-dashed border-gray-200 bg-white p-10 text-center">
    <p className="text-lg font-semibold text-text-primary">{title}</p>
    <p className="mt-2 text-sm text-text-secondary">{description}</p>
    {actionLabel && (
      <Button className="mt-4" onClick={onAction}>
        {actionLabel}
      </Button>
    )}
  </div>
);

