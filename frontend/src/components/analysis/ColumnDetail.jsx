import { Card, CardContent, CardHeader, CardTitle } from '../ui/card';

export const ColumnDetail = ({ column }) => {
  if (!column) return null;

  return (
    <Card>
      <CardHeader>
        <div>
          <p className="text-xs uppercase text-text-tertiary">Column detail</p>
          <CardTitle>{column.name}</CardTitle>
        </div>
        <p className="text-sm text-text-secondary">{column.type}</p>
      </CardHeader>
      <CardContent className="grid gap-4 md:grid-cols-2">
        {Object.entries(column.stats || {}).map(([label, value]) => (
          <div key={label}>
            <p className="text-xs uppercase text-text-tertiary">{label}</p>
            <p className="text-lg font-semibold text-text-primary">{value}</p>
          </div>
        ))}
      </CardContent>
    </Card>
  );
};

