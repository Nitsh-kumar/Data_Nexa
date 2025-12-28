export const TimelineChart = ({ items = [] }) => (
  <div className="rounded-2xl border border-gray-100 bg-white p-5">
    <p className="text-sm font-medium text-text-primary">Timeline</p>
    <div className="mt-4 space-y-4">
      {items.map((item) => (
        <div key={item.id} className="flex items-start gap-3">
          <div className="mt-1 h-2 w-2 rounded-full bg-primary-500" />
          <div>
            <p className="text-sm font-semibold text-text-primary">{item.label}</p>
            <p className="text-xs text-text-secondary">{item.timestamp}</p>
          </div>
        </div>
      ))}
    </div>
  </div>
);

