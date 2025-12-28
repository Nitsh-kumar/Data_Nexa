import { AppLayout } from '../../components/layout/AppLayout';
import { EmptyState } from '../../components/common/EmptyState';
import { DistributionChart } from '../../components/charts/DistributionChart';
import { TimelineChart } from '../../components/charts/TimelineChart';

export const DashboardPage = () => (
  <AppLayout>
    <div className="grid gap-6 lg:grid-cols-3">
      <div className="lg:col-span-2 space-y-6">
        <DistributionChart title="Row quality distribution" description="Last 7 ingests" />
        <EmptyState
          title="No active projects yet"
          description="Upload your first dataset to kick off an analysis."
          actionLabel="Start upload"
        />
      </div>
      <TimelineChart
        items={[
          { id: 1, label: 'Workspace created', timestamp: 'Just now' },
          { id: 2, label: 'Invite pending', timestamp: 'Soon' },
        ]}
      />
    </div>
  </AppLayout>
);

