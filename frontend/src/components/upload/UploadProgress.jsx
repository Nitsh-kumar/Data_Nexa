import { Progress } from '../ui/progress';

export const UploadProgress = ({ value = 0, status = 'idle' }) => (
  <div className="rounded-xl border border-gray-100 bg-white p-4">
    <div className="flex items-center justify-between text-sm">
      <span className="font-medium text-text-primary">Upload progress</span>
      <span className="text-text-secondary">{status}</span>
    </div>
    <Progress value={value} className="mt-3" />
  </div>
);

