export const LoadingSpinner = ({ label = 'Loading' }) => (
  <div className="flex flex-col items-center justify-center gap-3 py-10">
    <div className="h-10 w-10 animate-spin rounded-full border-4 border-primary-200 border-t-primary-600" />
    <p className="text-sm text-text-secondary">{label}…</p>
  </div>
);

