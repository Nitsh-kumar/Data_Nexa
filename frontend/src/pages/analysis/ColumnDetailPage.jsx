import { useParams } from 'react-router-dom';
import { AppLayout } from '../../components/layout/AppLayout';
import { ColumnDetail } from '../../components/analysis/ColumnDetail';

const mockColumn = {
  name: 'email',
  type: 'string',
  stats: {
    nulls: '1.2%',
    unique: '98.7%',
    pii: 'Yes',
    format_errors: '3.4%',
  },
};

export const ColumnDetailPage = () => {
  const { columnName } = useParams();

  return (
    <AppLayout>
      <div className="space-y-4">
        <h1 className="text-3xl font-semibold text-text-primary">Column detail</h1>
        <p className="text-text-secondary">
          Deep dive into <span className="font-medium">{columnName}</span>.
        </p>
        <ColumnDetail column={{ ...mockColumn, name: columnName ?? mockColumn.name }} />
      </div>
    </AppLayout>
  );
};

