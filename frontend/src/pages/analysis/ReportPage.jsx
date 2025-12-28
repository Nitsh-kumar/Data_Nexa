import { AppLayout } from '../../components/layout/AppLayout';
import { Button } from '../../components/ui/button';
import { exportService } from '../../services/exportService';

export const ReportPage = () => {
  const handleDownload = async () => {
    try {
      await exportService.downloadReport('demo-analysis');
      alert('Report download triggered (mock).');
    } catch (error) {
      console.error('Download failed', error);
    }
  };

  return (
    <AppLayout>
      <div className="rounded-3xl bg-white p-10 shadow-sm">
        <h1 className="text-3xl font-semibold text-text-primary">Final report</h1>
        <p className="text-text-secondary">Summary of findings and recommended remediations.</p>
        <div className="mt-6 space-y-4 text-sm text-text-secondary">
          <p>• 3 critical issues resolved</p>
          <p>• 8 warnings pending validation</p>
          <p>• Export contains reproducible steps + SQL snippets</p>
        </div>
        <Button className="mt-6" onClick={handleDownload}>
          Download PDF
        </Button>
      </div>
    </AppLayout>
  );
};

