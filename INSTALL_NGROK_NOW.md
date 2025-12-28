# Install ngrok - Quick Manual Method

Since npm install is slow, let's use the direct download method (faster and more reliable).

---

## 🚀 Quick Installation (5 minutes)

### Step 1: Download ngrok

1. **Open your browser**
2. **Go to**: https://ngrok.com/download
3. **Click**: Download for Windows
4. **Save** the zip file to your Downloads folder

### Step 2: Extract ngrok

1. **Find** the downloaded file: `ngrok-v3-stable-windows-amd64.zip`
2. **Right-click** → Extract All
3. **Extract to**: `C:\ngrok\` (or any folder you prefer)
4. You should now have: `C:\ngrok\ngrok.exe`

### Step 3: Add to PATH (Optional but Recommended)

**Option A - Add to PATH**:
1. Press `Windows + R`
2. Type: `sysdm.cpl` and press Enter
3. Go to "Advanced" tab
4. Click "Environment Variables"
5. Under "System variables", find "Path"
6. Click "Edit"
7. Click "New"
8. Add: `C:\ngrok`
9. Click OK on all windows
10. **Restart your terminal**

**Option B - Use Full Path** (Easier):
Just use the full path when running ngrok:
```powershell
C:\ngrok\ngrok.exe http 5173
```

---

## 🔑 Step 4: Get Your Auth Token

1. **Sign up** (if you haven't): https://dashboard.ngrok.com/signup
2. **Login** to ngrok dashboard
3. **Go to**: https://dashboard.ngrok.com/get-started/your-authtoken
4. **Copy** your authtoken (looks like: `2abc123def456ghi789jkl`)

---

## ⚙️ Step 5: Configure ngrok

Open PowerShell and run:

```powershell
# If you added to PATH:
ngrok config add-authtoken YOUR_TOKEN_HERE

# If using full path:
C:\ngrok\ngrok.exe config add-authtoken YOUR_TOKEN_HERE
```

Replace `YOUR_TOKEN_HERE` with your actual token.

---

## 🎯 Step 6: Start ngrok

```powershell
# If you added to PATH:
ngrok http 5173

# If using full path:
C:\ngrok\ngrok.exe http 5173
```

You should see:
```
ngrok

Session Status                online
Account                       your-email@example.com
Forwarding                    https://abc123def456.ngrok-free.app -> http://localhost:5173

Connections                   ttl     opn     rt1     rt5     p50     p90
                              0       0       0.00    0.00    0.00    0.00
```

**Copy your URL**: `https://abc123def456.ngrok-free.app`

---

## ✅ Verify Installation

Test if ngrok is working:

```powershell
# If added to PATH:
ngrok version

# If using full path:
C:\ngrok\ngrok.exe version
```

You should see something like: `ngrok version 3.x.x`

---

## 🎉 You're Done!

ngrok is now installed and ready to use!

**Next steps**:
1. ✅ ngrok installed
2. ✅ Auth token configured
3. ⏳ Start ngrok tunnel
4. ⏳ Configure Google OAuth
5. ⏳ Update backend CORS

---

## 🚀 Quick Commands

### Start tunnel for frontend
```powershell
ngrok http 5173
```

### Start tunnel for backend
```powershell
ngrok http 8000
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

## 📝 What to Do After Starting ngrok

1. **Copy the HTTPS URL** from ngrok output
2. **Update backend CORS** in `backend/.env`:
   ```env
   CORS_ORIGINS=["http://localhost:5173", "https://your-ngrok-url.ngrok-free.app"]
   ```
3. **Configure Google OAuth** with the ngrok URL
4. **Restart backend** if it's running

---

## 🐛 Troubleshooting

### "ngrok is not recognized"
- Use full path: `C:\ngrok\ngrok.exe`
- Or add to PATH and restart terminal

### "Please sign up"
- You need to add your authtoken first
- Get it from: https://dashboard.ngrok.com/get-started/your-authtoken

### "Tunnel not established"
- Check if your app is running on the port
- Verify port number is correct (5173 for frontend, 8000 for backend)

---

**Ready to expose your app!** 🚀

**Download now**: https://ngrok.com/download
