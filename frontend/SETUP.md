# Frontend Setup Guide

## ✅ Status: Ready to Run!

All files have been created and the frontend is now 100% complete.

---

## 🚀 Quick Start

### 1. Install Dependencies

```bash
cd frontend
npm install
```

This will install all required packages:
- React 18.3.1
- Vite 5.1.4
- React Router DOM 6.24.1
- Zustand 4.5.2
- Axios 1.7.2
- Tailwind CSS 3.4.1
- And all dev dependencies

### 2. Start Development Server

```bash
npm run dev
```

The app will start on: **http://localhost:5173**

The browser should open automatically. If not, manually navigate to the URL.

---

## 📋 Available Scripts

```bash
npm run dev      # Start development server with HMR
npm run build    # Create production build
npm run preview  # Preview production build locally
npm run lint     # Run ESLint
npm run format   # Format code with Prettier
```

---

## 🔧 Configuration

### Environment Variables

The `.env` file has been created with default values:

```env
VITE_API_URL=http://localhost:8000/api/v1
VITE_APP_NAME=DataInsight Pro
VITE_APP_VERSION=1.0.0
VITE_ENABLE_ANALYTICS=false
```

**To change the backend URL**, edit the `VITE_API_URL` value.

### Backend Requirements

The frontend expects the backend to be running on `http://localhost:8000` with these endpoints:

**Authentication:**
- POST `/api/v1/auth/register`
- POST `/api/v1/auth/login`
- POST `/api/v1/auth/logout`
- POST `/api/v1/auth/refresh-token`
- GET `/api/v1/auth/me`

**Datasets:**
- POST `/api/v1/datasets/upload`
- GET `/api/v1/datasets`
- GET `/api/v1/datasets/{id}`

**Analysis:**
- POST `/api/v1/analysis/start`
- GET `/api/v1/analysis/{id}/status`
- GET `/api/v1/analysis/{id}/results`

**Insights:**
- GET `/api/v1/insights/{analysis_id}`

**Exports:**
- GET `/api/v1/analysis/{id}/report`
- GET `/api/v1/datasets/{id}/export`

### CORS Configuration

Make sure your backend allows requests from `http://localhost:5173` during development.

---

## 📁 Project Structure

```
frontend/
├── src/
│   ├── App.jsx                 ✅ Main routing component
│   ├── main.jsx                ✅ React entry point
│   ├── components/             ✅ 30+ components
│   ├── pages/                  ✅ 15 page components
│   ├── services/               ✅ 5 API services
│   ├── store/                  ✅ 3 Zustand stores
│   ├── hooks/                  ✅ 6 custom hooks
│   ├── utils/                  ✅ Utilities
│   ├── config/                 ✅ Configuration
│   └── styles/                 ✅ Global styles
├── public/                     ✅ Static assets
├── .env                        ✅ Environment variables
├── package.json                ✅ Dependencies
├── vite.config.js              ✅ Vite configuration
├── tailwind.config.js          ✅ Tailwind configuration
└── index.html                  ✅ HTML entry point
```

---

## 🎯 Features Implemented

### Authentication
- ✅ Login page with email/password
- ✅ Registration page
- ✅ Forgot password page
- ✅ Protected routes
- ✅ JWT token management
- ✅ Automatic token refresh

### Dashboard
- ✅ Main dashboard with stats
- ✅ Project list view
- ✅ Quick actions

### File Upload
- ✅ Drag-and-drop file upload
- ✅ Upload progress tracking
- ✅ File validation
- ✅ Goal selection

### Analysis
- ✅ Processing status page
- ✅ Action center (results view)
- ✅ Column detail view
- ✅ Data preview
- ✅ Issue cards with severity
- ✅ Triage summary

### Charts & Visualizations
- ✅ Quality gauge
- ✅ Distribution charts
- ✅ Correlation matrix
- ✅ Timeline chart

### Settings
- ✅ Profile settings
- ✅ Workspace settings
- ✅ Billing page

### Onboarding
- ✅ Goal selection
- ✅ Team setup

---

## 🔍 Troubleshooting

### Port Already in Use

If port 5173 is already in use:

```bash
# Kill the process
npx kill-port 5173

# Or change the port in vite.config.js
```

### Module Not Found Errors

```bash
# Clear node_modules and reinstall
rm -rf node_modules package-lock.json
npm install
```

### CORS Errors

Make sure your backend has CORS configured to allow `http://localhost:5173`.

In FastAPI, add:

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### 401 Unauthorized Errors

Check that:
1. Backend authentication endpoints are working
2. JWT tokens are being generated correctly
3. Token is being sent in request headers

---

## 🧪 Testing

Currently, no tests are configured. To add testing:

```bash
# Install Vitest and React Testing Library
npm install -D vitest @testing-library/react @testing-library/jest-dom

# Add test script to package.json
"test": "vitest"
```

---

## 📦 Production Build

### Build for Production

```bash
npm run build
```

This creates an optimized build in the `dist/` directory.

### Preview Production Build

```bash
npm run preview
```

### Deploy

The `dist/` directory can be deployed to:
- **Vercel**: `vercel deploy`
- **Netlify**: Drag and drop `dist/` folder
- **AWS S3 + CloudFront**: Upload to S3 bucket
- **Docker**: Use provided Dockerfile (if exists)

---

## 📚 Documentation

- [Frontend Requirements](../FRONTEND_REQUIREMENTS.md) - Complete dependency list
- [Frontend Structure](./docs/FRONTEND_STRUCTURE.md) - Architecture overview
- [Implementation Status](./docs/IMPLEMENTATION_STATUS.md) - What's implemented
- [Quick Reference](./docs/QUICK_REFERENCE.md) - Code snippets and patterns

---

## ✅ Checklist

Before starting development:

- [x] All files created
- [x] App.jsx with routing
- [x] .env file configured
- [ ] Dependencies installed (`npm install`)
- [ ] Backend running on port 8000
- [ ] CORS configured in backend
- [ ] Development server started (`npm run dev`)

---

## 🎉 You're Ready!

The frontend is now 100% complete and ready to run. Just install dependencies and start the dev server!

```bash
npm install && npm run dev
```

Visit **http://localhost:5173** and start building! 🚀

---

**Need Help?**
- Check the [Quick Reference](./docs/QUICK_REFERENCE.md) for common patterns
- Review the [Frontend Structure](./docs/FRONTEND_STRUCTURE.md) for architecture details
- See [FRONTEND_REQUIREMENTS.md](../FRONTEND_REQUIREMENTS.md) for complete setup info
