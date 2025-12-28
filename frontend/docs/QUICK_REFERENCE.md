# Frontend Quick Reference

## 🚀 Getting Started

```bash
cd frontend
npm install
npm run dev
```

Visit: http://localhost:5173

---

## 📁 Where to Find Things

| What | Where |
|------|-------|
| UI Components | `src/components/ui/` |
| Page Components | `src/pages/` |
| API Calls | `src/services/` |
| State Management | `src/store/` |
| Custom Hooks | `src/hooks/` |
| Utilities | `src/utils/` |
| Styles | `src/styles/` |
| Config | `src/config/` |

---

## 🔧 Common Commands

```bash
# Development
npm run dev          # Start dev server
npm run build        # Production build
npm run preview      # Preview production build

# Code Quality
npm run lint         # Run ESLint
npm run format       # Format with Prettier
```

---

## 🌐 API Integration

### Base URL
```javascript
// Default: http://localhost:8000/api/v1
// Override with VITE_API_URL in .env
```

### Making API Calls
```javascript
import api from '@/services/api';

// GET request
const data = await api.get('/datasets');

// POST request
const result = await api.post('/datasets/upload', formData);
```

### Using Services
```javascript
import { authService } from '@/services/authService';

// Login
const { token, user } = await authService.login({ email, password });

// Register
const { token, user } = await authService.register({ email, password, name });
```

---

## 🗄️ State Management (Zustand)

### Auth Store
```javascript
import { authStore } from '@/store/authStore';

// Get state
const { user, token, isAuthenticated } = authStore();

// Actions
authStore.getState().login(token, user);
authStore.getState().logout();
```

### Upload Store
```javascript
import { uploadStore } from '@/store/uploadStore';

const { files, progress, isUploading } = uploadStore();
```

### Analysis Store
```javascript
import { analysisStore } from '@/store/analysisStore';

const { currentAnalysis, results, status } = analysisStore();
```

---

## 🎣 Custom Hooks

### useAuth
```javascript
import { useAuth } from '@/hooks/useAuth';

const { user, login, logout, isAuthenticated } = useAuth();
```

### useUpload
```javascript
import { useUpload } from '@/hooks/useUpload';

const { upload, progress, isUploading } = useUpload();
```

### useAnalysis
```javascript
import { useAnalysis } from '@/hooks/useAnalysis';

const { startAnalysis, getResults } = useAnalysis();
```

### useAnalysisPolling
```javascript
import { useAnalysisPolling } from '@/hooks/useAnalysisPolling';

const { status, results, error } = useAnalysisPolling(analysisId);
```

---

## 🎨 Styling with Tailwind

### Common Patterns
```jsx
// Button
<button className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700">
  Click Me
</button>

// Card
<div className="bg-white rounded-lg shadow-md p-6">
  Content
</div>

// Input
<input 
  className="w-full px-3 py-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-blue-500"
  type="text"
/>
```

### Using clsx for Conditional Classes
```javascript
import clsx from 'clsx';

const buttonClass = clsx(
  'px-4 py-2 rounded',
  isPrimary && 'bg-blue-600 text-white',
  isDisabled && 'opacity-50 cursor-not-allowed'
);
```

---

## 🛣️ Routing

### Basic Route Setup (in App.jsx)
```jsx
import { Routes, Route } from 'react-router-dom';

<Routes>
  <Route path="/" element={<HomePage />} />
  <Route path="/login" element={<LoginPage />} />
  <Route path="/dashboard" element={<DashboardPage />} />
  <Route path="/analysis/:id" element={<AnalysisPage />} />
</Routes>
```

### Navigation
```javascript
import { useNavigate } from 'react-router-dom';

const navigate = useNavigate();
navigate('/dashboard');
```

### Protected Routes
```jsx
<Route 
  path="/dashboard" 
  element={
    <ProtectedRoute>
      <DashboardPage />
    </ProtectedRoute>
  } 
/>
```

---

## 📦 Component Structure Template

```jsx
import { useState } from 'react';
import clsx from 'clsx';

/**
 * ComponentName - Brief description
 * 
 * @param {Object} props
 * @param {string} props.title - Title text
 * @param {Function} props.onAction - Action handler
 */
export function ComponentName({ title, onAction }) {
  const [state, setState] = useState(null);

  const handleClick = () => {
    // Logic here
    onAction?.();
  };

  return (
    <div className="component-wrapper">
      <h2>{title}</h2>
      <button onClick={handleClick}>Action</button>
    </div>
  );
}
```

---

## 🔐 Authentication Flow

### Login Flow
```javascript
import { authService } from '@/services/authService';
import { authStore } from '@/store/authStore';

async function handleLogin(email, password) {
  try {
    const { token, user } = await authService.login({ email, password });
    authStore.getState().login(token, user);
    navigate('/dashboard');
  } catch (error) {
    console.error('Login failed:', error);
  }
}
```

### Protected Component
```javascript
import { useAuth } from '@/hooks/useAuth';
import { Navigate } from 'react-router-dom';

function ProtectedRoute({ children }) {
  const { isAuthenticated } = useAuth();
  
  if (!isAuthenticated) {
    return <Navigate to="/login" />;
  }
  
  return children;
}
```

---

## 📤 File Upload Pattern

```javascript
import { useUpload } from '@/hooks/useUpload';

function UploadComponent() {
  const { upload, progress, isUploading } = useUpload();

  const handleFileChange = async (event) => {
    const file = event.target.files[0];
    if (file) {
      await upload(file);
    }
  };

  return (
    <div>
      <input type="file" onChange={handleFileChange} />
      {isUploading && <progress value={progress} max="100" />}
    </div>
  );
}
```

---

## 📊 Data Fetching Pattern

```javascript
import { useState, useEffect } from 'react';
import api from '@/services/api';

function DataComponent() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    async function fetchData() {
      try {
        const response = await api.get('/datasets');
        setData(response.data);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    }
    fetchData();
  }, []);

  if (loading) return <div>Loading...</div>;
  if (error) return <div>Error: {error}</div>;
  return <div>{/* Render data */}</div>;
}
```

---

## 🎯 Environment Variables

Create `.env` file:
```env
VITE_API_URL=http://localhost:8000/api/v1
```

Access in code:
```javascript
const apiUrl = import.meta.env.VITE_API_URL;
```

---

## 🐛 Debugging Tips

### React DevTools
Install React DevTools browser extension for component inspection.

### Network Requests
Check browser DevTools → Network tab for API calls.

### Console Logging
```javascript
console.log('Debug:', { variable });
console.error('Error:', error);
console.table(arrayData);
```

### Vite Dev Server
Hot Module Replacement (HMR) automatically updates on file changes.

---

## 📚 Key Dependencies

| Package | Purpose | Docs |
|---------|---------|------|
| React | UI Library | [react.dev](https://react.dev) |
| React Router | Routing | [reactrouter.com](https://reactrouter.com) |
| Zustand | State Management | [github.com/pmndrs/zustand](https://github.com/pmndrs/zustand) |
| Axios | HTTP Client | [axios-http.com](https://axios-http.com) |
| Tailwind CSS | Styling | [tailwindcss.com](https://tailwindcss.com) |
| Vite | Build Tool | [vitejs.dev](https://vitejs.dev) |

---

## 🚨 Common Issues

### Port Already in Use
```bash
# Kill process on port 5173
npx kill-port 5173
# Or change port in vite.config.js
```

### CORS Errors
Ensure backend allows `http://localhost:5173` in CORS settings.

### 401 Unauthorized
Check if token is being sent in request headers.

### Module Not Found
```bash
npm install
# Clear cache if needed
rm -rf node_modules package-lock.json
npm install
```

---

## ✅ Best Practices

1. **Keep components small** - Single responsibility
2. **Extract logic to hooks** - Reusable and testable
3. **Use TypeScript** - Better type safety (future improvement)
4. **Write tests** - Test as you build
5. **Document complex logic** - Help future you
6. **Use semantic HTML** - Better accessibility
7. **Handle errors gracefully** - User-friendly messages
8. **Optimize images** - Faster load times
9. **Code split routes** - Smaller bundles
10. **Follow ESLint rules** - Consistent code style

---

**Quick Links**:
- [Full Structure Documentation](./FRONTEND_STRUCTURE.md)
- [Implementation Status](./IMPLEMENTATION_STATUS.md)
- [Backend API Docs](../../backend/docs/)
