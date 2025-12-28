# DataInsight Pro - Frontend Structure Documentation

## Overview

The frontend is a **React 18 + Vite** application using modern tooling and a feature-first architecture. It's designed to provide a clean, responsive UI for the DataInsight Pro data profiling tool.

## Technology Stack

### Core Framework
- **React 18.3.1**: UI library with hooks and modern patterns
- **Vite 5.1.4**: Fast build tool and dev server
- **React Router DOM 6.24.1**: Client-side routing

### State Management
- **Zustand 4.5.2**: Lightweight state management (stores for auth, upload, analysis)

### HTTP Client
- **Axios 1.7.2**: Promise-based HTTP client with interceptors

### Styling
- **Tailwind CSS 3.4.1**: Utility-first CSS framework
- **PostCSS**: CSS processing
- **Autoprefixer**: Automatic vendor prefixing

### Code Quality
- **ESLint 8.57.0**: JavaScript linting
  - `eslint-plugin-react`: React-specific rules
  - `eslint-plugin-react-hooks`: Hooks rules
  - `eslint-plugin-jsx-a11y`: Accessibility rules
  - `eslint-config-prettier`: Prettier compatibility
- **Prettier 3.2.5**: Code formatting

### Utilities
- **clsx 2.1.1**: Conditional className utility

## Project Structure

```
frontend/
├── public/                     # Static assets
│   ├── favicon.svg
│   └── logo.svg
│
├── src/
│   ├── assets/                 # Images, icons, media
│   │   ├── icons/
│   │   └── images/
│   │
│   ├── components/             # Reusable UI components
│   │   ├── analysis/          # Analysis-related components
│   │   ├── auth/              # Authentication UI
│   │   ├── charts/            # Data visualization components
│   │   ├── common/            # Shared components
│   │   ├── layout/            # Layout components (Header, Sidebar, etc.)
│   │   ├── ui/                # Base UI primitives (Button, Input, etc.)
│   │   └── upload/            # File upload components
│   │
│   ├── config/                 # Configuration files
│   │   ├── apiConfig.js       # API configuration
│   │   └── routes.js          # Route definitions
│   │
│   ├── features/               # Feature-specific modules
│   │   ├── codeGeneration/    # Code generation feature
│   │   └── insights/          # AI insights feature
│   │
│   ├── hooks/                  # Custom React hooks
│   │   ├── useAnalysis.js     # Analysis operations
│   │   ├── useAnalysisPolling.js  # Poll analysis status
│   │   ├── useAuth.js         # Authentication
│   │   ├── useDebounce.js     # Debounce utility
│   │   ├── useLocalStorage.js # Local storage wrapper
│   │   └── useUpload.js       # File upload
│   │
│   ├── pages/                  # Route-level page components
│   │   ├── analysis/          # Analysis results pages
│   │   ├── auth/              # Login, Register pages
│   │   ├── dashboard/         # Main dashboard
│   │   ├── onboarding/        # User onboarding flow
│   │   └── settings/          # User settings
│   │
│   ├── services/               # API service layer
│   │   ├── api.js             # Axios instance with interceptors
│   │   ├── analysisService.js # Analysis API calls
│   │   ├── authService.js     # Auth API calls
│   │   ├── datasetService.js  # Dataset API calls
│   │   └── exportService.js   # Export API calls
│   │
│   ├── store/                  # Zustand state stores
│   │   ├── analysisStore.js   # Analysis state
│   │   ├── authStore.js       # Auth state & token management
│   │   └── uploadStore.js     # Upload state
│   │
│   ├── styles/                 # Global styles
│   │   ├── index.css          # Main stylesheet (Tailwind imports)
│   │   └── themes.js          # Theme configuration
│   │
│   ├── utils/                  # Utility functions
│   │   ├── constants.js       # App constants
│   │   ├── formatters.js      # Data formatting utilities
│   │   ├── helpers.js         # General helpers
│   │   └── validators.js      # Input validation
│   │
│   └── main.jsx                # React entry point
│
├── .env.example                # Environment variables template
├── .eslintrc.js                # ESLint configuration
├── .prettierrc                 # Prettier configuration
├── index.html                  # HTML entry point
├── package.json                # Dependencies and scripts
├── postcss.config.js           # PostCSS configuration
├── tailwind.config.js          # Tailwind CSS configuration
├── vite.config.js              # Vite configuration
└── README.md                   # Frontend documentation
```

## Architecture Patterns

### Feature-First Organization
Components and logic are organized by feature (auth, upload, analysis) rather than by type, making it easier to locate related code.

### Service Layer Pattern
All API calls are centralized in service files (`services/`), keeping components clean and testable.

### Custom Hooks
Business logic is extracted into custom hooks (`hooks/`), promoting reusability and separation of concerns.

### Zustand Stores
State management uses Zustand for simplicity:
- `authStore`: User authentication, token management
- `uploadStore`: File upload state and progress
- `analysisStore`: Analysis results and status

## Key Features Implemented

### 1. Authentication System
- **Location**: `src/components/auth/`, `src/services/authService.js`, `src/store/authStore.js`
- **Features**:
  - Login/Register flows
  - JWT token management
  - Automatic token refresh on 401 responses
  - Protected routes

### 2. File Upload
- **Location**: `src/components/upload/`, `src/hooks/useUpload.js`, `src/store/uploadStore.js`
- **Features**:
  - Drag-and-drop file upload
  - File validation (CSV/Excel)
  - Upload progress tracking
  - Multi-file support

### 3. Data Analysis
- **Location**: `src/pages/analysis/`, `src/hooks/useAnalysis.js`, `src/hooks/useAnalysisPolling.js`
- **Features**:
  - Analysis status polling
  - Results visualization
  - Column-level statistics display

### 4. AI Insights
- **Location**: `src/features/insights/`
- **Features**:
  - Display AI-generated insights
  - Severity-based categorization
  - Actionable recommendations

### 5. Code Generation
- **Location**: `src/features/codeGeneration/`
- **Features**:
  - Generate Python/SQL/R code
  - Copy-to-clipboard functionality
  - Syntax highlighting

## API Integration

### Base Configuration
```javascript
// Default API URL: http://localhost:8000/api/v1
// Override with VITE_API_URL environment variable
```

### Axios Interceptors
- **Request Interceptor**: Automatically adds JWT token to all requests
- **Response Interceptor**: Handles 401 errors with automatic token refresh

### Service Files
Each service file exports methods for specific API endpoints:
- `authService`: `/auth/*` endpoints
- `datasetService`: `/datasets/*` endpoints
- `analysisService`: `/analysis/*` endpoints
- `exportService`: `/exports/*` endpoints

## Development Workflow

### Available Scripts
```bash
npm run dev      # Start dev server on http://localhost:5173
npm run build    # Create production build
npm run preview  # Preview production build locally
npm run lint     # Run ESLint
npm run format   # Format code with Prettier
```

### Environment Variables
Create a `.env` file based on `.env.example`:
```env
VITE_API_URL=http://localhost:8000/api/v1
```

### Code Style
- **Line Length**: 100 characters (enforced by Prettier)
- **Quotes**: Single quotes for JavaScript
- **Semicolons**: Required
- **Trailing Commas**: ES5 style

## Current Status

### ✅ Implemented
- Project structure and configuration
- Build tooling (Vite, ESLint, Prettier, Tailwind)
- Service layer with API integration
- Authentication service and store
- Custom hooks for common operations
- Zustand stores for state management

### ⚠️ Missing/Incomplete
- **App.jsx**: Main App component is referenced but not created
- **Component implementations**: Most component directories exist but may be empty
- **Page implementations**: Page components need to be built
- **Routing configuration**: Routes need to be defined in App.jsx
- **UI components**: Base UI primitives need implementation
- **Charts**: Data visualization components need implementation

## Next Steps

1. **Create App.jsx** with routing configuration
2. **Implement base UI components** (Button, Input, Card, etc.)
3. **Build page components** (Dashboard, Login, Analysis Results)
4. **Implement chart components** for data visualization
5. **Connect stores to components** for state management
6. **Add error boundaries** for better error handling
7. **Implement loading states** and skeletons
8. **Add unit tests** with Vitest or Jest
9. **Optimize bundle size** and performance

## Integration with Backend

The frontend is designed to work with the FastAPI backend:

### Expected Backend Endpoints
- `POST /api/v1/auth/register`
- `POST /api/v1/auth/login`
- `POST /api/v1/auth/refresh-token`
- `GET /api/v1/auth/me`
- `POST /api/v1/datasets/upload`
- `GET /api/v1/datasets/{id}`
- `POST /api/v1/analysis/start`
- `GET /api/v1/analysis/{id}/status`
- `GET /api/v1/analysis/{id}/results`
- `GET /api/v1/insights/{analysis_id}`
- `POST /api/v1/exports/code`

### CORS Configuration
Backend must allow requests from `http://localhost:5173` during development.

## Accessibility

The project includes `eslint-plugin-jsx-a11y` to enforce accessibility best practices:
- Semantic HTML elements
- ARIA attributes where needed
- Keyboard navigation support
- Screen reader compatibility

## Performance Considerations

- **Code Splitting**: Use React.lazy() for route-based code splitting
- **Memoization**: Use React.memo() and useMemo() for expensive computations
- **Virtualization**: Consider react-window for large lists
- **Image Optimization**: Use appropriate formats and lazy loading
- **Bundle Analysis**: Run `vite build --analyze` to check bundle size

## Deployment

### Production Build
```bash
npm run build
# Output: dist/ directory
```

### Environment Variables
Set `VITE_API_URL` to production API endpoint before building.

### Hosting Options
- **Vercel**: Zero-config deployment
- **Netlify**: Simple static hosting
- **AWS S3 + CloudFront**: Scalable CDN solution
- **Docker**: Use provided Dockerfile (if exists)

## Resources

- [React Documentation](https://react.dev)
- [Vite Documentation](https://vitejs.dev)
- [Tailwind CSS Documentation](https://tailwindcss.com)
- [Zustand Documentation](https://github.com/pmndrs/zustand)
- [React Router Documentation](https://reactrouter.com)
