# 🚀 DO THIS NOW - Quick Action List

**Goal**: Get ngrok running and configure OAuth in the next 15 minutes

---

## ✅ Step-by-Step Actions

### 1. Download ngrok (2 minutes)
```
1. Open browser
2. Go to: https://ngrok.com/download
3. Click "Download for Windows"
4. Save the zip file
5. Extract to C:\ngrok\
```

### 2. Sign Up for ngrok (2 minutes)
```
1. Go to: https://dashboard.ngrok.com/signup
2. Sign up with email or Google
3. Verify your email
4. Login to dashboard
```

### 3. Get Your Auth Token (1 minute)
```
1. Go to: https://dashboard.ngrok.com/get-started/your-authtoken
2. Copy the token (looks like: 2abc123def456...)
3. Keep it handy
```

### 4. Configure ngrok (1 minute)
```powershell
# Open PowerShell and run:
C:\ngrok\ngrok.exe config add-authtoken YOUR_TOKEN_HERE
```

### 5. Start ngrok (1 minute)
```powershell
# In PowerShell:
C:\ngrok\ngrok.exe http 5173
```

**COPY THE URL** that appears (like: `https://abc123.ngrok-free.app`)

---

## 🎯 Now Configure Google OAuth

### 6. Create Google Cloud Project (3 minutes)
```
1. Go to: https://console.cloud.google.com/
2. Click "New Project"
3. Name: "DataInsight Pro"
4. Click "Create"
5. Select your project
```

### 7. Configure OAuth Consent Screen (3 minutes)
```
1. Go to: APIs & Services → OAuth consent screen
2. Select: External
3. App name: DataInsight Pro
4. User support email: your-email@example.com
5. App domain: https://your-ngrok-url.ngrok-free.app
6. Authorized domains: ngrok-free.app
7. Developer contact: your-email@example.com
8. Click: Save and Continue (through all steps)
```

### 8. Create OAuth Credentials (2 minutes)
```
1. Go to: APIs & Services → Credentials
2. Click: Create Credentials → OAuth 2.0 Client ID
3. Type: Web application
4. Name: DataInsight Pro Web Client

Authorized JavaScript origins:
  https://your-ngrok-url.ngrok-free.app
  http://localhost:5173

Authorized redirect URIs:
  https://your-ngrok-url.ngrok-free.app/auth/callback
  http://localhost:5173/auth/callback

5. Click: Create
6. COPY Client ID and Client Secret
```

---

## 📝 What You Should Have Now

After completing the above:

✅ ngrok installed at `C:\ngrok\`
✅ ngrok authtoken configured
✅ ngrok running with URL like: `https://abc123.ngrok-free.app`
✅ Google Cloud project created
✅ OAuth consent screen configured
✅ OAuth credentials created
✅ Client ID copied
✅ Client Secret copied

---

## 🎯 Next: Configure Your App

### Create backend/.env

Create file: `backend/.env`

```env
DATABASE_URL=sqlite+aiosqlite:///./datainsight.db
SECRET_KEY=change-this-to-a-random-32-character-string
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

GOOGLE_CLIENT_ID=paste-your-client-id-here
GOOGLE_CLIENT_SECRET=paste-your-client-secret-here
GOOGLE_REDIRECT_URI=https://your-ngrok-url.ngrok-free.app/auth/callback

CORS_ORIGINS=["http://localhost:5173", "https://your-ngrok-url.ngrok-free.app"]

PROJECT_NAME=DataInsight Pro
VERSION=1.0.0
API_V1_STR=/api/v1
ENVIRONMENT=development
DEBUG=True
```

**Replace**:
- `paste-your-client-id-here` → Your actual Google Client ID
- `paste-your-client-secret-here` → Your actual Google Client Secret
- `your-ngrok-url.ngrok-free.app` → Your actual ngrok URL
- `change-this-to-a-random-32-character-string` → Generate with:
  ```powershell
  python -c "import secrets; print(secrets.token_urlsafe(32))"
  ```

---

## 🚀 Then Start Backend

```powershell
cd backend
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

---

## ✅ Final Check

You should now have:

**Terminal 1**: Frontend running (already done ✅)
**Terminal 2**: ngrok running (new)
**Terminal 3**: Backend running (new)

**Access**:
- Local: http://localhost:5173
- Public: https://your-ngrok-url.ngrok-free.app
- Backend: http://localhost:8000
- API Docs: http://localhost:8000/docs

---

## 🎉 Test It!

1. Open: `https://your-ngrok-url.ngrok-free.app`
2. Click: "Login with Google"
3. Sign in with Google
4. Authorize the app
5. You should be logged in!

---

## 📞 Quick Links

- **ngrok Download**: https://ngrok.com/download
- **ngrok Dashboard**: https://dashboard.ngrok.com/
- **Google Console**: https://console.cloud.google.com/
- **Get Auth Token**: https://dashboard.ngrok.com/get-started/your-authtoken

---

## 🆘 If You Get Stuck

1. Check **AUTH_SETUP_COMPLETE_GUIDE.md** for detailed steps
2. Check **NGROK_SETUP_GUIDE.md** for ngrok help
3. Check **QUICK_NGROK_COMMANDS.md** for quick commands

---

**START NOW!** ⏰

**Estimated Time**: 15 minutes total
**Current Step**: Download ngrok from https://ngrok.com/download
