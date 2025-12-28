import { createContext, useContext } from 'react';
import { Button } from '../ui/button';
import { Badge } from '../ui/badge';
import { cn } from '../../utils/helpers';

const IssueContext = createContext({});

export const IssueCard = ({ issue, children }) => (
  <IssueContext.Provider value={issue}>
    <div className="rounded-2xl border border-gray-100 bg-white p-4 shadow-sm">{children}</div>
  </IssueContext.Provider>
);

const useIssue = () => useContext(IssueContext);

const severityColors = {
  critical: 'text-critical',
  warning: 'text-warning',
  info: 'text-primary-600',
};

const Header = ({ severity }) => {
  const issue = useIssue();
  return (
    <div className="flex flex-wrap items-start justify-between gap-2">
      <div>
        <p className="text-xs uppercase text-text-tertiary">{issue.category}</p>
        <h4 className="text-lg font-semibold text-text-primary">{issue.title}</h4>
      </div>
      <Badge variant={severity}>{severity}</Badge>
    </div>
  );
};

const Body = ({ children }) => (
  <div className="mt-3 space-y-3 text-sm text-text-secondary">{children}</div>
);

const Description = () => {
  const issue = useIssue();
  return <p>{issue.description}</p>;
};

const ImpactBadge = () => {
  const issue = useIssue();
  return (
    <div className={cn('inline-flex items-center gap-2 text-xs font-medium', severityColors[issue.severity])}>
      Impact: {issue.impact}
    </div>
  );
};

const Recommendation = () => {
  const issue = useIssue();
  return (
    <div className="rounded-lg bg-background-tertiary p-3 text-sm text-text-primary">
      <p className="font-medium">Recommendation</p>
      <p className="text-text-secondary">{issue.recommendation}</p>
    </div>
  );
};

const Actions = () => (
  <div className="mt-4 flex flex-wrap gap-3">
    <Button variant="secondary">View details</Button>
    <Button>Generate code</Button>
  </div>
);

IssueCard.Header = Header;
IssueCard.Body = Body;
IssueCard.Description = Description;
IssueCard.Impact = ImpactBadge;
IssueCard.Recommendation = Recommendation;
IssueCard.Actions = Actions;

