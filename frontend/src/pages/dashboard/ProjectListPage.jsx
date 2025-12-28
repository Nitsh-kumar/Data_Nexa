import { AppLayout } from '../../components/layout/AppLayout';
import { Card, CardContent, CardHeader, CardTitle } from '../../components/ui/card';

const projects = [
  { id: 'demo-1', name: 'Marketing Data Health', status: 'Processing', datasets: 3 },
  { id: 'demo-2', name: 'Finance Controls', status: 'Completed', datasets: 5 },
];

export const ProjectListPage = () => (
  <AppLayout>
    <div className="space-y-4">
      {projects.map((project) => (
        <Card key={project.id}>
          <CardHeader className="items-center justify-between">
            <CardTitle>{project.name}</CardTitle>
            <span className="text-sm text-text-tertiary">{project.status}</span>
          </CardHeader>
          <CardContent>
            <p className="text-sm text-text-secondary">{project.datasets} datasets attached</p>
          </CardContent>
        </Card>
      ))}
    </div>
  </AppLayout>
);

