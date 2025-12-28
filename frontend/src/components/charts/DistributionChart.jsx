/**
 * Simplified placeholder chart using CSS gradients. Replace with Recharts, nivo,
 * or Chart.js when you are ready for production visualizations.
 */
export const DistributionChart = ({ title, description }) => (
  <div className="rounded-2xl border border-gray-100 bg-white p-5">
    <p className="text-sm font-medium text-text-primary">{title}</p>
    <p className="text-xs text-text-secondary">{description}</p>
    <div className="mt-4 h-32 rounded-xl bg-gradient-to-r from-primary-100 via-primary-500/40 to-primary-100" />
  </div>
);

