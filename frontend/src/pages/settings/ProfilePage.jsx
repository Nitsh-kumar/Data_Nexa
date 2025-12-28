import { AppLayout } from '../../components/layout/AppLayout';
import { Input } from '../../components/ui/input';
import { Button } from '../../components/ui/button';

export const ProfilePage = () => (
  <AppLayout>
    <div className="max-w-2xl space-y-6 rounded-3xl bg-white p-8">
      <div>
        <h1 className="text-3xl font-semibold text-text-primary">Profile</h1>
        <p className="text-sm text-text-secondary">Update your personal details.</p>
      </div>
      <div className="space-y-4">
        <Input label="Name" defaultValue="Alex Analyst" />
        <Input label="Email" type="email" defaultValue="alex@datainsight.pro" />
        <Button>Save changes</Button>
      </div>
    </div>
  </AppLayout>
);

