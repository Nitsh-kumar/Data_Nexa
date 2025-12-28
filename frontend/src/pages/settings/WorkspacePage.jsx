import { AppLayout } from '../../components/layout/AppLayout';
import { Input } from '../../components/ui/input';
import { Button } from '../../components/ui/button';

export const WorkspacePage = () => (
  <AppLayout>
    <div className="max-w-2xl space-y-6 rounded-3xl bg-white p-8">
      <div>
        <h1 className="text-3xl font-semibold text-text-primary">Workspace</h1>
        <p className="text-sm text-text-secondary">Control workspace defaults and branding.</p>
      </div>
      <div className="space-y-4">
        <Input label="Workspace name" defaultValue="Data Team HQ" />
        <Input label="Default timezone" defaultValue="UTC" />
        <Button>Save workspace settings</Button>
      </div>
    </div>
  </AppLayout>
);

