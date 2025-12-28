import { AppLayout } from '../../components/layout/AppLayout';
import { Button } from '../../components/ui/button';

export const BillingPage = () => (
  <AppLayout>
    <div className="max-w-3xl space-y-6 rounded-3xl bg-white p-8">
      <div>
        <h1 className="text-3xl font-semibold text-text-primary">Billing</h1>
        <p className="text-sm text-text-secondary">Plan usage and payment method.</p>
      </div>
      <div className="rounded-2xl border border-gray-100 p-5">
        <p className="text-sm font-semibold text-text-primary">Current plan</p>
        <p className="text-3xl font-bold text-text-primary">
          Scale <span className="text-base font-medium text-text-secondary">· $249/mo</span>
        </p>
        <Button className="mt-4">Change plan</Button>
      </div>
      <div className="rounded-2xl border border-gray-100 p-5">
        <p className="text-sm font-semibold text-text-primary">Payment method</p>
        <p className="text-text-secondary">Visa ending in 4242 · Expires 12/28</p>
        <Button variant="secondary" className="mt-3">
          Update card
        </Button>
      </div>
    </div>
  </AppLayout>
);

