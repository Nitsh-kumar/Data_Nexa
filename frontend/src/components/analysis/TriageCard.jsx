import { Card, CardContent, CardHeader, CardTitle } from '../ui/card';
import { Badge } from '../ui/badge';

export const TriageCard = ({ label, count, severity }) => {
  const colorMap = {
    critical: 'text-critical',
    warning: 'text-warning',
    info: 'text-primary-600',
  };

  return (
    <Card className="space-y-2">
      <CardHeader className="items-center justify-between">
        <CardTitle>{label}</CardTitle>
        <Badge variant={severity}>{severity.toUpperCase()}</Badge>
      </CardHeader>
      <CardContent>
        <p className={`text-3xl font-semibold ${colorMap[severity]}`}>{count}</p>
        <p className="text-sm text-text-secondary">issues to review</p>
      </CardContent>
    </Card>
  );
};

