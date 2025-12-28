import { Button } from '../ui/button';

const providers = [
  { label: 'Continue with Google', icon: '🟢', provider: 'google' },
  { label: 'Continue with GitHub', icon: '⚫', provider: 'github' },
  { label: 'Continue with Azure AD', icon: '🔷', provider: 'azure' },
];

export const SocialAuthButtons = ({ onSelect }) => (
  <div className="space-y-3">
    {providers.map((provider) => (
      <Button
        key={provider.provider}
        variant="secondary"
        className="w-full justify-start gap-3"
        onClick={() => onSelect?.(provider.provider)}
      >
        <span>{provider.icon}</span>
        {provider.label}
      </Button>
    ))}
  </div>
);

