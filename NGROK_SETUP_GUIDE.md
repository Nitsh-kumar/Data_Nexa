# ngrok Setup Guide for DataInsight Pro

**Purpose**: Expose your local application to the internet with a public HTTPS URL

---

## 🌐 What is ngrok?

ngrok creates a secure tunnel from a public URL to your local server. This is useful for:
- Testing OAuth (Google, GitHub login)
- Sharing your app with others
- Testing webhooks
- Mobile device testing
- Demo purposes

---

## 📋 Step-by-Step Setup

### Step 1: Install ngrok

#### Option A: Download from Website (Recommended)
1. Go to https://ngrok.com/
2. Click "Sign up" (free account)
3. Download ngrok for Windows
4. Extract the zip file to a folder (e.g., `C:\ngrok\`)

#### Option B: Using Chocolatey (Windows Package Manager)
```powershell
choco install ngrok
```

#### Option C: Using npm
```powershell
npm install -g ngrok
```

### Step 2: Sign Up and Get Auth Token

1. **Create Account**: https://dashboard.ngrok.com/signup
2. **Get Auth Token**: https://dashboard.ngrok.com/get-started/your-authtoken
3. **Copy your authtoken** (looks like: `2abc123def456ghi789jkl`)

### Step 3: Configure ngrok

```powershell
# Add your authtoken (replace with your actual token)
ngrok config add-authtoken YOUR_AUTH_TOKEN_HERE
```

Example:
```powershell
ngrok config add-authtoken 2abc123def456ghi789jkl
```

---

## 🚀 Running ngrok

### For Frontend (Port 5173)

```powershell
ngrok http 5173
```

You'll see output like:
```
ngrok

Session Status                online
Account                       your-email@example.com
Version                       3.x.x
Region                        United States (us)
Latency                       -
Web Interface                 http://127.0.0.1:4040
Forwarding                    https://abc123def456.ngrok-free.app -> http://localhost:5173

Connections                   ttl     opn     rt1     rt5     p50     p90
                              0       0       0.00    0.00    0.00    0.00
```

**Your public URL**: `https://abc123def456.ngrok-free.app`

### For Backend (Port 8000)

If you also need to expose the backend:

```powershell
# In a separate terminal
ngrok http 8000
```

---

## 🔧 Configuration for Your App

### Update Frontend Environment

Once you have your ngrok URL, update your frontend configuration:

**frontend/.env**:
```env
# If backend is also on ngrok
VITE_API_URL=https://your-backend-url.ngrok-free.app/api/v1

# If backend is still local
VITE_API_URL=http://localhost:8000/api/v1
```

### Update Backend CORS

**backend/.env**:
```env
# Add your ngrok URL to allowed origins
CORS_ORIGINS=["http://localhost:5173", "https://your-frontend-url.ngrok-free.app"]
```

---

## 🔐 For Google OAuth Setup

### Step 1: Get Your ngrok URL

After running `ngrok http 5173`, copy the HTTPS URL:
```
https://abc123def456.ngrok-free.app
```

### Step 2: Configure Google Cloud Console

1. **Go to**: https://console.cloud.google.com/
2. **Select your project** (or create one)
3. **Navigate to**: APIs & Services → Credentials
4. **Click**: OAuth consent screen

#### OAuth Consent Screen Configuration

**App Domain Section**:
- **Application home page**: `https://abc123def456.ngrok-free.app`
- **Application privacy policy link**: `https://abc123def456.ngrok-free.app/privacy`
- **Application terms of service link**: `https://abc123def456.ngrok-free.app/terms`

**Authorized domains**:
- Add: `ngrok-free.app` (without https://)

### Step 3: Configure OAuth 2.0 Client

**Create OAuth 2.0 Client ID**:
1. Go to: APIs & Services → Credentials
2. Click: Create Credentials → OAuth 2.0 Client ID
3. Application type: Web application

**Authorized JavaScript origins**:
```
https://abc123def456.ngrok-free.app
```

**Authorized redirect URIs**:
```
https://abc123def456.ngrok-free.app/auth/callback
https://abc123def456.ngrok-free.app/auth/google/callback
```

### Step 4: Important Rules

✅ **DO**:
- Use the exact URL ngrok gives you
- Include `https://` in redirect URIs
- Use the base domain in authorized origins
- Match URLs exactly (no trailing slashes unless needed)

❌ **DON'T**:
- Add paths to authorized origins (e.g., `/login`)
- Mix http and https
- Add trailing slashes inconsistently
- Use different subdomains

---

## 🎯 Complete Setup Example

### Scenario: Frontend on ngrok, Backend local

**1. Start Frontend**:
```powershell
# Terminal 1
cd frontend
npm run dev
```

**2. Start ngrok for Frontend**:
```powershell
# Terminal 2
ngrok http 5173
```

**3. Start Backend**:
```powershell
# Terminal 3
cd backend
.\venv\Scripts\Activate.ps1
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**4. Update Backend CORS**:
```env
CORS_ORIGINS=["http://localhost:5173", "https://your-ngrok-url.ngrok-free.app"]
```

**5. Access Your App**:
- Local: http://localhost:5173
- Public: https://your-ngrok-url.ngrok-free.app

---

## 🌟 Advanced: Both Frontend and Backend on ngrok

### Setup

**Terminal 1 - Frontend**:
```powershell
cd frontend
npm run dev
```

**Terminal 2 - Frontend ngrok**:
```powershell
ngrok http 5173
# Copy the URL: https://frontend-abc123.ngrok-free.app
```

**Terminal 3 - Backend**:
```powershell
cd backend
.\venv\Scripts\Activate.ps1
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Terminal 4 - Backend ngrok**:
```powershell
ngrok http 8000
# Copy the URL: https://backend-def456.ngrok-free.app
```

### Configuration

**frontend/.env**:
```env
VITE_API_URL=https://backend-def456.ngrok-free.app/api/v1
```

**backend/.env**:
```env
CORS_ORIGINS=["https://frontend-abc123.ngrok-free.app"]
```

---

## 🔍 Monitoring ngrok

### Web Interface

ngrok provides a web interface at: **http://localhost:4040**

Features:
- See all requests
- Inspect request/response details
- Replay requests
- View connection stats

### Command Line Status

Press `Ctrl+C` to stop ngrok

---

## 💡 Tips and Best Practices

### 1. Free vs Paid Plans

**Free Plan**:
- ✅ Random URLs (changes each restart)
- ✅ HTTPS support
- ✅ Basic features
- ❌ No custom domains
- ❌ URL changes on restart

**Paid Plans** ($8-10/month):
- ✅ Custom domains
- ✅ Reserved URLs (don't change)
- ✅ More concurrent tunnels
- ✅ Better performance

### 2. URL Changes

**Problem**: Free ngrok URLs change every time you restart

**Solutions**:
- Use ngrok's reserved domains (paid)
- Update Google OAuth settings each time
- Use environment variables for easy updates

### 3. Performance

- ngrok adds ~50-200ms latency
- Good for testing, not for production
- Use for development/demo only

### 4. Security

- ✅ ngrok provides HTTPS automatically
- ✅ Secure tunnel
- ⚠️ Anyone with the URL can access your app
- ⚠️ Don't share sensitive data on free ngrok URLs

---

## 🐛 Troubleshooting

### ngrok command not found

**Solution**:
```powershell
# Add ngrok to PATH or use full path
C:\ngrok\ngrok.exe http 5173
```

### Tunnel not established

**Solution**:
1. Check if authtoken is configured: `ngrok config check`
2. Verify port is correct and app is running
3. Check firewall settings

### CORS errors with ngrok

**Solution**:
Update backend CORS to include ngrok URL:
```env
CORS_ORIGINS=["http://localhost:5173", "https://your-ngrok-url.ngrok-free.app"]
```

Restart backend after changing CORS settings.

### Google OAuth "redirect_uri_mismatch"

**Solution**:
1. Verify redirect URI in Google Console matches exactly
2. Check for trailing slashes
3. Ensure using HTTPS (not HTTP)
4. Wait a few minutes for Google to update

### ngrok URL changes

**Solution**:
- Upgrade to paid plan for reserved domains
- Or update Google OAuth settings each time
- Use ngrok config file for consistent settings

---

## 📝 Quick Reference

### Start ngrok
```powershell
ngrok http 5173
```

### With custom subdomain (paid)
```powershell
ngrok http 5173 --subdomain=myapp
```

### With custom domain (paid)
```powershell
ngrok http 5173 --hostname=myapp.example.com
```

### View web interface
```
http://localhost:4040
```

### Stop ngrok
```
Ctrl + C
```

---

## 🎯 Complete Workflow

### For Google OAuth Testing

1. **Start your app locally**:
   ```powershell
   # Terminal 1: Frontend
   cd frontend
   npm run dev
   
   # Terminal 2: Backend
   cd backend
   .\venv\Scripts\Activate.ps1
   uvicorn app.main:app --reload
   ```

2. **Start ngrok**:
   ```powershell
   # Terminal 3
   ngrok http 5173
   ```

3. **Copy ngrok URL**: `https://abc123.ngrok-free.app`

4. **Update Google OAuth**:
   - Authorized JavaScript origins: `https://abc123.ngrok-free.app`
   - Authorized redirect URIs: `https://abc123.ngrok-free.app/auth/callback`

5. **Update backend CORS**:
   ```env
   CORS_ORIGINS=["https://abc123.ngrok-free.app"]
   ```

6. **Restart backend**

7. **Test**: Visit `https://abc123.ngrok-free.app`

---

## ✅ Checklist

Before testing with ngrok:

- [ ] ngrok installed and configured
- [ ] Authtoken added
- [ ] Frontend running on port 5173
- [ ] Backend running on port 8000
- [ ] ngrok tunnel started
- [ ] ngrok URL copied
- [ ] Google OAuth configured with ngrok URL
- [ ] Backend CORS updated with ngrok URL
- [ ] Backend restarted
- [ ] Tested access via ngrok URL

---

## 🆘 Need Help?

### ngrok Documentation
- https://ngrok.com/docs

### ngrok Dashboard
- https://dashboard.ngrok.com/

### Common Issues
- Check ngrok status: http://localhost:4040
- Verify app is running: http://localhost:5173
- Check CORS settings in backend
- Verify Google OAuth redirect URIs match exactly

---

**Ready to expose your app to the internet!** 🚀

**Next Step**: Run `ngrok http 5173` and copy the HTTPS URL!
