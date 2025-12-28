# Quick ngrok Commands for DataInsight Pro

---

## 🚀 Quick Start (3 Steps)

### 1. Install ngrok
```powershell
# Download from: https://ngrok.com/download
# Or install via npm:
npm install -g ngrok
```

### 2. Add Auth Token
```powershell
# Get token from: https://dashboard.ngrok.com/get-started/your-authtoken
ngrok config add-authtoken YOUR_TOKEN_HERE
```

### 3. Start Tunnel
```powershell
ngrok http 5173
```

---

## 📋 Essential Commands

### Expose Frontend (Port 5173)
```powershell
ngrok http 5173
```

### Expose Backend (Port 8000)
```powershell
ngrok http 8000
```

### View Web Interface
```
http://localhost:4040
```

### Stop ngrok
```
Ctrl + C
```

---

## 🔧 What to Do After Starting ngrok

### 1. Copy Your URL
After running `ngrok http 5173`, you'll see:
```
Forwarding    https://abc123def456.ngrok-free.app -> http://localhost:5173
```

Copy: `https://abc123def456.ngrok-free.app`

### 2. Update Backend CORS

Edit `backend/.env`:
```env
CORS_ORIGINS=["http://localhost:5173", "https://abc123def456.ngrok-free.app"]
```

### 3. Restart Backend
```powershell
# Stop backend (Ctrl+C)
# Start again:
uvicorn app.main:app --reload
```

### 4. Access Your App
- Local: http://localhost:5173
- Public: https://abc123def456.ngrok-free.app

---

## 🎯 For Google OAuth

### Add to Google Cloud Console

**Authorized JavaScript origins**:
```
https://abc123def456.ngrok-free.app
```

**Authorized redirect URIs**:
```
https://abc123def456.ngrok-free.app/auth/callback
https://abc123def456.ngrok-free.app/auth/google/callback
```

**App Domain** (OAuth consent screen):
```
https://abc123def456.ngrok-free.app
```

---

## ⚠️ Important Notes

1. **URL Changes**: Free ngrok URLs change every restart
2. **Update Google OAuth**: Each time you restart ngrok
3. **Update CORS**: Add new ngrok URL to backend
4. **HTTPS Only**: Always use https:// for OAuth
5. **Exact Match**: URLs must match exactly in Google Console

---

## 🐛 Quick Fixes

### "command not found"
```powershell
# Use full path
C:\path\to\ngrok.exe http 5173
```

### CORS Error
```env
# backend/.env - Add ngrok URL
CORS_ORIGINS=["https://your-ngrok-url.ngrok-free.app"]
```

### OAuth redirect_uri_mismatch
- Check URL matches exactly in Google Console
- No trailing slashes
- Use https:// not http://

---

## 📞 Quick Links

- **Download**: https://ngrok.com/download
- **Dashboard**: https://dashboard.ngrok.com/
- **Docs**: https://ngrok.com/docs
- **Get Token**: https://dashboard.ngrok.com/get-started/your-authtoken

---

**That's it! Run `ngrok http 5173` and you're live!** 🎉
