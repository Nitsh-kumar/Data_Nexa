export const InsightsList = ({ insights = [] }) => (
  <div className="space-y-3">
    {insights.map((insight) => (
      <div key={insight.id} className="rounded-2xl border border-gray-100 bg-white p-4">
        <p className="text-sm font-semibold text-text-primary">{insight.title}</p>
        <p className="text-xs text-text-secondary">{insight.summary}</p>
      </div>
    ))}
    {!insights.length && <p className="text-sm text-text-tertiary">No insights available yet.</p>}
  </div>
);

