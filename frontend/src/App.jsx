import { Routes, Route, Navigate } from 'react-router-dom';
import { ProtectedRoute } from './components/auth/ProtectedRoute';
import { routes } from './config/routes';

// Auth pages
import { LoginPage } from './pages/auth/LoginPage';
import { RegisterPage } from './pages/auth/RegisterPage';
import { ForgotPasswordPage } from './pages/auth/ForgotPasswordPage';

// Dashboard pages
import { DashboardPage } from './pages/dashboard/DashboardPage';
import { ProjectListPage } from './pages/dashboard/ProjectListPage';

// Analysis pages
import { UploadPage } from './pages/analysis/UploadPage';
import { ProcessingPage } from './pages/analysis/ProcessingPage';
import { ActionCenterPage } from './pages/analysis/ActionCenterPage';
import { ColumnDetailPage } from './pages/analysis/ColumnDetailPage';
import { ReportPage } from './pages/analysis/ReportPage';

// Onboarding pages
import { GoalSelectionPage } from './pages/onboarding/GoalSelectionPage';
import { TeamSetupPage } from './pages/onboarding/TeamSetupPage';

// Settings pages
import { ProfilePage } from './pages/settings/ProfilePage';
import { WorkspacePage } from './pages/settings/WorkspacePage';
import { BillingPage } from './pages/settings/BillingPage';

/**
 * Main App component with routing configuration.
 * Uses React Router v6 with nested routes and protected route wrapper.
 */
function App() {
  return (
    <Routes>
      {/* Public routes - accessible without authentication */}
      <Route path={routes.LOGIN} element={<LoginPage />} />
      <Route path={routes.REGISTER} element={<RegisterPage />} />
      <Route path={routes.FORGOT_PASSWORD} element={<ForgotPasswordPage />} />

      {/* Protected routes - require authentication */}
      <Route element={<ProtectedRoute />}>
        {/* Dashboard */}
        <Route path={routes.DASHBOARD} element={<DashboardPage />} />
        <Route path="/projects" element={<ProjectListPage />} />

        {/* Analysis workflow */}
        <Route path={routes.UPLOAD} element={<UploadPage />} />
        <Route path={routes.PROCESSING} element={<ProcessingPage />} />
        <Route path={routes.ACTION_CENTER} element={<ActionCenterPage />} />
        <Route path={routes.COLUMN_DETAIL} element={<ColumnDetailPage />} />
        <Route path={routes.REPORT} element={<ReportPage />} />

        {/* Onboarding */}
        <Route path={routes.ONBOARDING_GOAL} element={<GoalSelectionPage />} />
        <Route path={routes.ONBOARDING_TEAM} element={<TeamSetupPage />} />

        {/* Settings */}
        <Route path={routes.SETTINGS_PROFILE} element={<ProfilePage />} />
        <Route path={routes.SETTINGS_WORKSPACE} element={<WorkspacePage />} />
        <Route path={routes.SETTINGS_BILLING} element={<BillingPage />} />
      </Route>

      {/* Default redirects */}
      <Route path="/" element={<Navigate to={routes.DASHBOARD} replace />} />
      <Route path="*" element={<Navigate to={routes.DASHBOARD} replace />} />
    </Routes>
  );
}

export default App;
