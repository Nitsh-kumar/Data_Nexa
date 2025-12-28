export const CorrelationMatrix = ({ matrix = [] }) => (
  <div className="rounded-2xl border border-gray-100 bg-white p-5">
    <p className="text-sm font-medium text-text-primary">Correlation matrix</p>
    <div className="mt-4 grid grid-cols-5 gap-2">
      {matrix.map((value, index) => (
        <div
          key={`${value}-${index}`}
          className="flex h-12 items-center justify-center rounded-lg text-sm font-medium text-white"
          style={{ backgroundColor: `rgba(37, 99, 235, ${value})` }}
        >
          {Math.round(value * 100)}%
        </div>
      ))}
    </div>
  </div>
);

