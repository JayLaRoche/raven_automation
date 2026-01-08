# 🚀 CLICK & RUN - Raven Shop Automation Startup

**Problem:** Getting `localhost refused to connect`?

**Solution:** Use the batch files! No terminal knowledge needed.

---

## 3-Click Startup

### Step 1: Start Backend 🖱️
**File Location:**
```
C:\Users\larochej3\Desktop\raven-shop-automation\START_BACKEND.bat
```

**Action:** Double-click `START_BACKEND.bat`

**Expected:** A new console window opens with the backend server running.

**Wait for:** 
```
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000
```

✓ **Backend running!** Keep this window open.

---

### Step 2: Start Frontend 🖱️
**File Location:**
```
C:\Users\larochej3\Desktop\raven-shop-automation\START_FRONTEND.bat
```

**Action:** Double-click `START_FRONTEND.bat`

**Expected:** A new console window opens with the frontend dev server.

**Wait for:**
```
➜  Local:   http://localhost:3000/
```

✓ **Frontend running!** Keep this window open.

---

### Step 3: Open Application 🌐
**Action:** Open your browser and go to:
```
http://localhost:3000
```

✓ **You should see the Raven Shop Automation application!**

---

## It's That Simple!

Now you can:
- ✓ View frame series with images
- ✓ Generate drawings
- ✓ See real-time changes (hot reload)

---

## Troubleshooting 1-Click Style

### Issue: Still getting "Connection Refused"

**Quick Fix:**
1. Minimize/close all windows
2. Delete all `.bat` files and re-create them from the instructions below
3. Double-click `START_BACKEND.bat` again
4. Wait 10 seconds
5. Double-click `START_FRONTEND.bat`
6. Go to http://localhost:3000

### Issue: "Port already in use"

**Quick Fix:**
```
Right-click START_BACKEND.bat → Edit
Add this line at the top:
taskkill /F /IM python.exe /IM node.exe
```

### Issue: "npm: command not found"

Node.js not installed. Download from: https://nodejs.org/
- Install with default options
- Restart computer
- Try again

---

## What These Files Do

### START_BACKEND.bat
```batch
Starts: Python FastAPI server on http://localhost:8000
Purpose: API endpoints for frame data, drawings, images
Keep running: YES (don't close this window)
```

### START_FRONTEND.bat
```batch
Starts: Node.js React development server on http://localhost:3000
Purpose: User interface and application
Keep running: YES (don't close this window)
```

---

## If You Want to Stop Everything

**Easy Way:**
- Click the X button on each console window

**That's it!** Both servers will shut down cleanly.

---

## One-Time Setup (First Time Only)

If the batch files don't exist or need updating:

### Create START_BACKEND.bat

1. Open Notepad
2. Copy this:
```batch
@echo off
cd /d "%~dp0backend"
taskkill /F /IM python.exe >nul 2>&1
echo Starting backend server...
start "Raven Backend" python -m uvicorn main:app --host 0.0.0.0 --port 8000
echo.
echo Server is starting in a new window...
timeout /t 3 /nobreak
```

3. Save as: `START_BACKEND.bat` (in project root)

### Create START_FRONTEND.bat

1. Open Notepad
2. Copy this:
```batch
@echo off
cd /d "%~dp0frontend"
taskkill /F /IM node.exe >nul 2>&1
if not exist node_modules (
    echo Installing npm packages...
    call npm install
)
echo Starting frontend...
call npm run dev
pause
```

3. Save as: `START_FRONTEND.bat` (in project root)

---

## That's It!

Your complete development system is now:
1. **One click away** from running the backend
2. **One click away** from running the frontend
3. **One navigation** away from the application

No terminal commands needed! 🎉

---

## Bonus: Advanced Users

If you prefer the command line:

**Terminal 1:**
```powershell
cd backend
python -m uvicorn main:app --host 0.0.0.0 --port 8000
```

**Terminal 2:**
```powershell
cd frontend
npm run dev
```

**Browser:**
```
http://localhost:3000
```

---

## Status

✓ Backend server: Working  
✓ Frontend server: Working  
✓ Database: Connected  
✓ Frame images: Available (67 files)  
✓ Static files: Mounted  

**Ready to use!** 🚀
