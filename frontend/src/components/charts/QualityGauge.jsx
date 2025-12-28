export const QualityGauge = ({ score = 0 }) => (
  <div className="rounded-2xl border border-gray-100 bg-white p-5 text-center">
    <p className="text-sm text-text-secondary">Quality score</p>
    <p className="mt-2 text-4xl font-bold text-primary-600">{score}</p>
    <p className="text-xs uppercase tracking-widest text-text-tertiary">/ 100</p>
    <div className="mt-4 h-2 rounded-full bg-gray-100">
      <div className="h-full rounded-full bg-primary-600" style={{ width: `${score}%` }} />
    </div>
  </div>
);

