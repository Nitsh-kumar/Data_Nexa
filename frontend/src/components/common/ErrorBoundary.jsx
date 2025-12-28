import { Component } from 'react';
import { Button } from '../ui/button';

export class ErrorBoundary extends Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false };
  }

  static getDerivedStateFromError() {
    return { hasError: true };
  }

  componentDidCatch(error, errorInfo) {
    console.error('React error boundary', error, errorInfo);
  }

  handleRetry = () => {
    this.setState({ hasError: false });
    this.props.onRetry?.();
  };

  render() {
    if (this.state.hasError) {
      return (
        <div className="rounded-2xl border border-error/30 bg-error/5 p-6 text-center">
          <p className="text-lg font-semibold text-error">Something went wrong.</p>
          <p className="mt-2 text-sm text-text-secondary">
            Please try again or contact support if the issue persists.
          </p>
          <Button className="mt-4" variant="primary" onClick={this.handleRetry}>
            Try again
          </Button>
        </div>
      );
    }

    return this.props.children;
  }
}

