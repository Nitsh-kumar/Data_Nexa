import { AppLayout } from '../../components/layout/AppLayout';
import { LoadingSpinner } from '../../components/common/LoadingSpinner';

export const ProcessingPage = () => (
  <AppLayout>
    <div className="rounded-3xl bg-white p-10">
      <LoadingSpinner label="Crunching dataset insights" />
      <p className="text-center text-sm text-text-secondary">
        You can leave this page — we will email you once the analysis is ready.
      </p>
    </div>
  </AppLayout>
);

