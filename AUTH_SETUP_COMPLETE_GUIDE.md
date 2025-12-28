# Complete Authentication Setup Guide

**Goal**: Set up Google OAuth authentication for DataInsight Pro

---

## 📋 Overview

We'll set up:
1. ✅ ngrok to expose your local app
2. ✅ Google OAuth credentials
3. ✅ Backend authentication endpoints
4. ✅ Frontend OAuth integration

---

## Part 1: Install and Configure ngrok

### Step 1: Download ngrok
1. Go to: https://ngrok.com/download
2. Download for Windows
3. Extract to `C:\ngrok\`

### Step 2: Sign Up and Get Token
1. Sign up: https://dashboard.ngrok.com/signup
2. Get token: https://dashboard.ngrok.com/get-started/your-authtoken
3. Copy your authtoken

### Step 3: Configure ngrok
```powershell
C:\ngrok\ngrok.exe config add-authtoken YOUR_TOKEN_HERE
```

### Step 4: Start ngrok
```powershell
C:\ngrok\ngrok.exe http 5173
```

**Copy your URL**: `https://abc123def456.ngrok-free.app`

---

## Part 2: Set Up Google OAuth

### Step 1: Create Google Cloud Project

1. **Go to**: https://console.cloud.google.com/
2. **Click**: "Select a project" → "New Project"
3. **Project name**: `DataInsight Pro`
4. **Click**: Create
5. **Wait** for project to be created
6. **Select** your new project

### Step 2: Enable Google+ API

1. **Go to**: APIs & Services → Library
2. **Search**: "Google+ API"
3. **Click**: Google+ API
4. **Click**: Enable

### Step 3: Configure OAuth Consent Screen

1. **Go to**: APIs & Services → OAuth consent screen
2. **Select**: External
3. **Click**: Create

**App information**:
- **App name**: `DataInsight Pro`
- **User support email**: Your email
- **App logo**: (optional)

**App domain**:
- **Application home page**: `https://your-ngrok-url.ngrok-free.app`
- **Application privacy policy link**: `https://your-ngrok-url.ngrok-free.app/privacy`
- **Application terms of service link**: `https://your-ngrok-url.ngrok-free.app/terms`

**Authorized domains**:
- Add: `ngrok-free.app` (without https://)

**Developer contact information**:
- Your email

**Click**: Save and Continue

**Scopes**:
- Click: Add or Remove Scopes
- Select: `email`, `profile`, `openid`
- Click: Update
- Click: Save and Continue

**Test users** (for development):
- Add your email address
- Click: Save and Continue

**Click**: Back to Dashboard

### Step 4: Create OAuth 2.0 Credentials

1. **Go to**: APIs & Services → Credentials
2. **Click**: Create Credentials → OAuth 2.0 Client ID
3. **Application type**: Web application
4. **Name**: `DataInsight Pro Web Client`

**Authorized JavaScript origins**:
```
https://your-ngrok-url.ngrok-free.app
http://localhost:5173
```

**Authorized redirect URIs**:
```
https://your-ngrok-url.ngrok-free.app/auth/callback
https://your-ngrok-url.ngrok-free.app/auth/google/callback
http://localhost:5173/auth/callback
http://localhost:5173/auth/google/callback
```

**Click**: Create

**Copy**:
- Client ID (looks like: `123456789-abc.apps.googleusercontent.com`)
- Client Secret (looks like: `GOCSPX-abc123def456`)

---

## Part 3: Configure Backend

### Step 1: Create backend/.env File

Create `backend/.env` with this content:

```env
# Database
DATABASE_URL=sqlite+aiosqlite:///./datainsight.db

# Security
SECRET_KEY=your-super-secret-key-change-this-in-production-min-32-chars
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Google OAuth
GOOGLE_CLIENT_ID=YOUR_GOOGLE_CLIENT_ID_HERE
GOOGLE_CLIENT_SECRET=YOUR_GOOGLE_CLIENT_SECRET_HERE
GOOGLE_REDIRECT_URI=https://your-ngrok-url.ngrok-free.app/auth/google/callback

# CORS - Add both localhost and ngrok URL
CORS_ORIGINS=["http://localhost:5173", "https://your-ngrok-url.ngrok-free.app"]

# App Settings
PROJECT_NAME=DataInsight Pro
VERSION=1.0.0
API_V1_STR=/api/v1
ENVIRONMENT=development
DEBUG=True

# AI Service (optional for now)
ANTHROPIC_API_KEY=your-anthropic-key-here

# Redis (optional)
REDIS_URL=redis://localhost:6379
```

**Replace**:
- `YOUR_GOOGLE_CLIENT_ID_HERE` with your actual Client ID
- `YOUR_GOOGLE_CLIENT_SECRET_HERE` with your actual Client Secret
- `your-ngrok-url.ngrok-free.app` with your actual ngrok URL
- `your-super-secret-key...` with a random 32+ character string

### Step 2: Generate a Secure SECRET_KEY

```powershell
# In PowerShell
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

Copy the output and use it as your SECRET_KEY.

---

## Part 4: Configure Frontend

### Update frontend/.env

Edit `frontend/.env`:

```env
# Use ngrok URL for backend if backend is also on ngrok
# Or use localhost if backend is local
VITE_API_URL=http://localhost:8000/api/v1

# Google OAuth
VITE_GOOGLE_CLIENT_ID=YOUR_GOOGLE_CLIENT_ID_HERE

# App Settings
VITE_APP_NAME=DataInsight Pro
VITE_APP_VERSION=1.0.0
VITE_ENABLE_ANALYTICS=false
```

**Replace**:
- `YOUR_GOOGLE_CLIENT_ID_HERE` with your actual Client ID

---

## Part 5: Install Backend Dependencies

```powershell
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
.\venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt
```

---

## Part 6: Start Everything

### Terminal 1: Frontend (Already Running)
```powershell
cd frontend
npm run dev
# Running on http://localhost:5173
```

### Terminal 2: ngrok for Frontend
```powershell
C:\ngrok\ngrok.exe http 5173
# Copy the HTTPS URL
```

### Terminal 3: Backend
```powershell
cd backend
.\venv\Scripts\Activate.ps1
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Terminal 4: ngrok for Backend (Optional)
```powershell
C:\ngrok\ngrok.exe http 8000
# Only if you want backend also public
```

---

## Part 7: Test Authentication

### Access Your App

1. **Open browser**
2. **Go to**: `https://your-ngrok-url.ngrok-free.app`
3. **Click**: "Login with Google"
4. **Sign in** with your Google account
5. **Authorize** the app
6. **You should be redirected** back to the app and logged in

---

## 🎯 Complete Checklist

### ngrok Setup
- [ ] ngrok downloaded and extracted
- [ ] ngrok authtoken configured
- [ ] ngrok running for frontend (port 5173)
- [ ] ngrok HTTPS URL copied

### Google OAuth Setup
- [ ] Google Cloud project created
- [ ] OAuth consent screen configured
- [ ] OAuth 2.0 credentials created
- [ ] Client ID and Secret copied
- [ ] Authorized origins added
- [ ] Redirect URIs added

### Backend Setup
- [ ] backend/.env file created
- [ ] Google credentials added to .env
- [ ] SECRET_KEY generated and added
- [ ] CORS origins include ngrok URL
- [ ] Virtual environment created
- [ ] Dependencies installed
- [ ] Backend server running

### Frontend Setup
- [ ] frontend/.env updated
- [ ] Google Client ID added
- [ ] Frontend server running
- [ ] Can access via ngrok URL

### Testing
- [ ] Can access app via ngrok URL
- [ ] "Login with Google" button visible
- [ ] Can click and see Google login
- [ ] Can authorize and login
- [ ] Redirected back to app
- [ ] User is logged in

---

## 🐛 Common Issues

### "redirect_uri_mismatch"
**Problem**: Google OAuth redirect URI doesn't match

**Solution**:
1. Check Google Console redirect URIs match exactly
2. Ensure using https:// for ngrok URLs
3. No trailing slashes unless your app uses them
4. Wait a few minutes for Google to update

### CORS Error
**Problem**: Backend blocking requests from ngrok URL

**Solution**:
1. Add ngrok URL to CORS_ORIGINS in backend/.env
2. Restart backend server
3. Clear browser cache

### "Invalid client"
**Problem**: Google Client ID or Secret is wrong

**Solution**:
1. Double-check Client ID in backend/.env
2. Double-check Client Secret in backend/.env
3. Ensure no extra spaces or quotes
4. Regenerate credentials if needed

### ngrok URL Changed
**Problem**: ngrok URL changes on restart (free plan)

**Solution**:
1. Update Google OAuth redirect URIs
2. Update backend/.env CORS_ORIGINS
3. Update backend/.env GOOGLE_REDIRECT_URI
4. Restart backend
5. Or upgrade to ngrok paid plan for static URLs

---

## 📝 Quick Reference

### Start Everything
```powershell
# Terminal 1: Frontend
cd frontend && npm run dev

# Terminal 2: ngrok
C:\ngrok\ngrok.exe http 5173

# Terminal 3: Backend
cd backend && .\venv\Scripts\Activate.ps1 && uvicorn app.main:app --reload
```

### Important URLs
- **Frontend Local**: http://localhost:5173
- **Frontend Public**: https://your-ngrok-url.ngrok-free.app
- **Backend Local**: http://localhost:8000
- **Backend API Docs**: http://localhost:8000/docs
- **ngrok Dashboard**: http://localhost:4040
- **Google Console**: https://console.cloud.google.com/

---

## 🎉 Success!

Once everything is set up, you should be able to:
1. ✅ Access your app via ngrok URL
2. ✅ Click "Login with Google"
3. ✅ Authenticate with Google
4. ✅ Be redirected back logged in
5. ✅ Use all app features

---

**Need help?** Check the troubleshooting section or refer to:
- NGROK_SETUP_GUIDE.md
- QUICK_NGROK_COMMANDS.md
- STARTUP_GUIDE.md

**Ready to start!** 🚀
