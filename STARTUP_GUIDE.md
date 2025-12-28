# DataInsight Pro - Complete Startup Guide

**Date**: November 29, 2025  
**Status**: Ready to Run

---

## 🔍 Current System Status

### ✅ Installed
- **Python**: 3.13.6 (Detected)
- **Backend**: Complete with all files
- **Frontend**: Complete with all files

### ❌ Not Installed
- **Node.js**: Required for frontend (npm not found)
- **Backend Dependencies**: Need to be installed
- **Frontend Dependencies**: Need to be installed (requires Node.js)

---

## 📋 Prerequisites

### 1. Node.js Installation (Required for Frontend)

**Download Node.js 18+ LTS:**
- Visit: https://nodejs.org/
- Download the LTS version (Long Term Support)
- Run the installer
- Verify installation: `node --version` and `npm --version`

**Alternative - Using Chocolatey (Windows Package Manager):**
```powershell
# Install Chocolatey first (if not installed)
# Then install Node.js
choco install nodejs-lts
```

### 2. Python (Already Installed ✅)
- Python 3.13.6 is already installed

---

## 🚀 Step-by-Step Startup

### Phase 1: Install Node.js (Frontend Requirement)

1. **Download and Install Node.js**
   - Go to https://nodejs.org/
   - Download Node.js 18.x LTS or higher
   - Run the installer (accept all defaults)
   - Restart your terminal/PowerShell

2. **Verify Installation**
   ```powershell
   node --version
   npm --version
   ```

### Phase 2: Backend Setup

1. **Navigate to Backend Directory**
   ```powershell
   cd backend
   ```

2. **Create Virtual Environment**
   ```powershell
   python -m venv venv
   ```

3. **Activate Virtual Environment**
   ```powershell
   # Windows PowerShell
   .\venv\Scripts\Activate.ps1
   
   # Windows CMD
   venv\Scripts\activate.bat
   ```

4. **Install Backend Dependencies**
   ```powershell
   pip install -r requirements.txt
   ```

5. **Set Up Environment Variables**
   ```powershell
   # Copy example env file
   copy .env.example .env
   
   # Edit .env file with your settings
   # Minimum required:
   # - DATABASE_URL
   # - SECRET_KEY
   # - ANTHROPIC_API_KEY (for AI features)
   ```

6. **Initialize Database** (if using PostgreSQL)
   ```powershell
   # Create database migrations
   alembic upgrade head
   ```

7. **Start Backend Server**
   ```powershell
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

   Backend will be available at: **http://localhost:8000**
   API docs at: **http://localhost:8000/docs**

### Phase 3: Frontend Setup (After Node.js is Installed)

1. **Open New Terminal** (keep backend running)

2. **Navigate to Frontend Directory**
   ```powershell
   cd frontend
   ```

3. **Install Frontend Dependencies**
   ```powershell
   npm install
   ```

4. **Verify Environment Variables**
   ```powershell
   # .env file already created with:
   # VITE_API_URL=http://localhost:8000/api/v1
   ```

5. **Start Frontend Development Server**
   ```powershell
   npm run dev
   ```

   Frontend will be available at: **http://localhost:5173**

---

## 🎯 Quick Start (After Prerequisites)

### Terminal 1 - Backend
```powershell
cd backend
.\venv\Scripts\Activate.ps1
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Terminal 2 - Frontend
```powershell
cd frontend
npm run dev
```

### Access the Application
- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

---

## 🔧 Configuration

### Backend Configuration (.env)

Create `backend/.env` file:

```env
# Database
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/datainsight

# Security
SECRET_KEY=your-secret-key-here-change-this-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# AI Service
ANTHROPIC_API_KEY=your-anthropic-api-key-here

# Redis (optional)
REDIS_URL=redis://localhost:6379

# CORS
CORS_ORIGINS=["http://localhost:5173"]

# Environment
ENVIRONMENT=development
DEBUG=True
```

### Frontend Configuration (.env)

Already created at `frontend/.env`:

```env
VITE_API_URL=http://localhost:8000/api/v1
VITE_APP_NAME=DataInsight Pro
VITE_APP_VERSION=1.0.0
VITE_ENABLE_ANALYTICS=false
```

---

## 🗄️ Database Setup

### Option 1: PostgreSQL (Recommended)

1. **Install PostgreSQL**
   - Download from: https://www.postgresql.org/download/
   - Or use Docker: `docker run -d -p 5432:5432 -e POSTGRES_PASSWORD=password postgres`

2. **Create Database**
   ```sql
   CREATE DATABASE datainsight;
   ```

3. **Update DATABASE_URL in backend/.env**
   ```env
   DATABASE_URL=postgresql+asyncpg://postgres:password@localhost:5432/datainsight
   ```

4. **Run Migrations**
   ```powershell
   cd backend
   alembic upgrade head
   ```

### Option 2: SQLite (Development Only)

Update `backend/.env`:
```env
DATABASE_URL=sqlite+aiosqlite:///./datainsight.db
```

---

## 🐛 Troubleshooting

### Node.js Not Found
**Error**: `npm : The term 'npm' is not recognized`

**Solution**:
1. Install Node.js from https://nodejs.org/
2. Restart terminal
3. Verify: `node --version`

### Python Virtual Environment Issues
**Error**: Cannot activate virtual environment

**Solution**:
```powershell
# Enable script execution (run as Administrator)
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Then activate
.\venv\Scripts\Activate.ps1
```

### Port Already in Use
**Error**: Port 8000 or 5173 already in use

**Solution**:
```powershell
# Kill process on port 8000
npx kill-port 8000

# Kill process on port 5173
npx kill-port 5173
```

### CORS Errors
**Error**: CORS policy blocking requests

**Solution**:
- Ensure backend `.env` has: `CORS_ORIGINS=["http://localhost:5173"]`
- Restart backend server

### Database Connection Error
**Error**: Cannot connect to database

**Solution**:
1. Verify PostgreSQL is running
2. Check DATABASE_URL in `.env`
3. Ensure database exists: `CREATE DATABASE datainsight;`

### Module Not Found (Backend)
**Error**: `ModuleNotFoundError`

**Solution**:
```powershell
# Ensure virtual environment is activated
.\venv\Scripts\Activate.ps1

# Reinstall dependencies
pip install -r requirements.txt
```

### Module Not Found (Frontend)
**Error**: Cannot find module

**Solution**:
```powershell
# Clear and reinstall
Remove-Item -Recurse -Force node_modules
Remove-Item package-lock.json
npm install
```

---

## ✅ Verification Checklist

### Before Starting

- [ ] Node.js installed (v18+)
- [ ] Python installed (v3.11+) ✅
- [ ] PostgreSQL installed (or using SQLite)
- [ ] Backend `.env` file configured
- [ ] Frontend `.env` file exists ✅

### Backend Running

- [ ] Virtual environment activated
- [ ] Dependencies installed
- [ ] Database migrations run
- [ ] Server running on port 8000
- [ ] API docs accessible at http://localhost:8000/docs

### Frontend Running

- [ ] Node modules installed
- [ ] Development server running on port 5173
- [ ] Can access http://localhost:5173
- [ ] No console errors

### Integration Working

- [ ] Frontend can reach backend API
- [ ] No CORS errors
- [ ] Login page loads
- [ ] Can register new user
- [ ] Can login with credentials

---

## 📊 System Requirements

### Minimum Requirements
- **OS**: Windows 10/11, macOS 10.15+, Linux
- **RAM**: 4GB
- **Storage**: 2GB free space
- **Node.js**: 18.x or higher
- **Python**: 3.11 or higher
- **PostgreSQL**: 14+ (or SQLite for development)

### Recommended Requirements
- **RAM**: 8GB+
- **Storage**: 5GB+ free space
- **Node.js**: 20.x LTS
- **Python**: 3.11+
- **PostgreSQL**: 15+

---

## 🎯 Next Steps After Installation

1. **Install Node.js** (if not already installed)
2. **Set up backend** (virtual environment, dependencies, database)
3. **Set up frontend** (npm install)
4. **Start both servers**
5. **Access the application** at http://localhost:5173
6. **Create a test account** and explore features

---

## 📚 Additional Resources

### Documentation
- [Backend README](backend/README.md)
- [Frontend Setup](frontend/SETUP.md)
- [Frontend Requirements](FRONTEND_REQUIREMENTS.md)
- [API Documentation](http://localhost:8000/docs) (when running)

### External Resources
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [React Documentation](https://react.dev/)
- [Vite Documentation](https://vitejs.dev/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)

---

## 🆘 Getting Help

### Common Issues
1. Check this troubleshooting section
2. Review error messages carefully
3. Verify all prerequisites are installed
4. Check configuration files

### Error Logs
- **Backend**: Check terminal output where uvicorn is running
- **Frontend**: Check browser console (F12)
- **Database**: Check PostgreSQL logs

---

## 🎉 Success Indicators

When everything is working correctly, you should see:

### Backend Terminal
```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

### Frontend Terminal
```
VITE v5.1.4  ready in 500 ms

➜  Local:   http://localhost:5173/
➜  Network: use --host to expose
➜  press h to show help
```

### Browser
- Login page loads without errors
- No CORS errors in console
- Can interact with UI elements

---

**Ready to start? Follow the steps above!** 🚀

**Current Status**: Waiting for Node.js installation to proceed with frontend setup.
