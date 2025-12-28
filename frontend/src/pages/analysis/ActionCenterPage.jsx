import { AppLayout } from '../../components/layout/AppLayout';
import { TriageCard } from '../../components/analysis/TriageCard';
import { IssueCard } from '../../components/analysis/IssueCard';
import { DataPreview } from '../../components/analysis/DataPreview';
import { QualityGauge } from '../../components/charts/QualityGauge';
import { InsightsList } from '../../features/insights/InsightsList';
import { CodeGenerationModal } from '../../features/codeGeneration/CodeGenerationModal';
import { Badge } from '../../components/ui/badge';
import { Button } from '../../components/ui/button';

const datasetInfo = {
  name: 'customers_prod_v2.csv',
  rows: 128000,
  columns: 48,
  size: '56 MB',
};

const triageStats = [
  { label: 'Critical', count: 3, severity: 'critical' },
  { label: 'Warnings', count: 8, severity: 'warning' },
  { label: 'Insights', count: 14, severity: 'info' },
];

const issues = [
  {
    id: 1,
    severity: 'critical',
    category: 'PII leakage',
    title: 'Email column contains invalid domains',
    description: '1.2% of rows contain disposable or malformed email domains.',
    impact: 'High',
    recommendation: 'Normalize the column and reject rows that do not match RFC 822.',
  },
  {
    id: 2,
    severity: 'warning',
    category: 'Null density',
    title: 'Missing country codes',
    description: '14% of addresses do not have a country_code assigned.',
    impact: 'Medium',
    recommendation: 'Backfill country_code using postal_code or user locale.',
  },
];

const previewData = {
  columns: ['customer_id', 'email', 'country_code', 'lifetime_value'],
  rows: [
    { customer_id: 'C-1022', email: 'gina@example.com', country_code: 'US', lifetime_value: '$12k' },
    { customer_id: 'C-1023', email: 'sunil@example.in', country_code: 'IN', lifetime_value: '$8k' },
  ],
};

const quickStats = [
  { label: 'PII detected', value: '6 columns' },
  { label: 'Null columns', value: '12%' },
  { label: 'Schema drift', value: '2 fields' },
];

export const ActionCenterPage = () => (
  <AppLayout>
    <div className="space-y-6">
      <header className="flex flex-wrap items-center justify-between gap-4">
        <div>
          <p className="text-sm text-text-tertiary">Dataset</p>
          <h1 className="text-3xl font-semibold text-text-primary">{datasetInfo.name}</h1>
          <div className="mt-2 flex flex-wrap gap-4 text-sm text-text-secondary">
            <span>{datasetInfo.rows.toLocaleString()} rows</span>
            <span>{datasetInfo.columns} columns</span>
            <span>{datasetInfo.size}</span>
          </div>
        </div>
        <div className="flex items-center gap-3">
          <Button variant="secondary">Export CSV</Button>
          <Button>Export report</Button>
        </div>
      </header>

      <section className="grid gap-4 md:grid-cols-3">
        {triageStats.map((stat) => (
          <TriageCard key={stat.label} {...stat} />
        ))}
      </section>

      <section className="grid gap-6 lg:grid-cols-[3fr_2fr]">
        <div className="space-y-4">
          <div className="flex items-center justify-between">
            <h2 className="text-xl font-semibold text-text-primary">Issues</h2>
            <Badge variant="info">{issues.length} open</Badge>
          </div>
          <div className="space-y-4">
            {issues.map((issue) => (
              <IssueCard key={issue.id} issue={issue}>
                <IssueCard.Header severity={issue.severity} />
                <IssueCard.Body>
                  <IssueCard.Description />
                  <IssueCard.Impact />
                  <IssueCard.Recommendation />
                </IssueCard.Body>
                <IssueCard.Actions>
                  <CodeGenerationModal analysisId={issue.id} />
                </IssueCard.Actions>
              </IssueCard>
            ))}
          </div>
        </div>
        <div className="space-y-4">
          <h3 className="text-xl font-semibold text-text-primary">Data preview</h3>
          <DataPreview data={previewData} />
          <div className="rounded-2xl border border-gray-100 bg-white p-4">
            <p className="text-sm font-medium text-text-primary">Affected rows indicator</p>
            <p className="text-sm text-text-secondary">~1,280 rows need review</p>
          </div>
        </div>
      </section>

      <aside className="grid gap-6 lg:grid-cols-3">
        <QualityGauge score={87} />
        <div className="rounded-2xl border border-gray-100 bg-white p-5">
          <p className="text-sm font-semibold text-text-primary">Quick stats</p>
          <div className="mt-4 space-y-3">
            {quickStats.map((stat) => (
              <div key={stat.label} className="flex items-center justify-between">
                <span className="text-sm text-text-secondary">{stat.label}</span>
                <span className="text-sm font-medium text-text-primary">{stat.value}</span>
              </div>
            ))}
          </div>
        </div>
        <div className="rounded-2xl border border-gray-100 bg-white p-5">
          <p className="text-sm font-semibold text-text-primary">Top recommendations</p>
          <InsightsList
            insights={[
              { id: '1', title: 'Normalize email casing', summary: 'Reduces duplicate accounts.' },
              { id: '2', title: 'Fill missing country codes', summary: 'Improves geo segmentation.' },
            ]}
          />
        </div>
      </aside>
    </div>
  </AppLayout>
);

