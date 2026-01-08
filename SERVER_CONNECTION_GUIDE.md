# SERVER CONNECTION REFUSED - ROOT CAUSE & SOLUTION

**Date:** January 6, 2026  
**Issue:** `localhost refused to connect` / `ERR_CONNECTION_REFUSED` when trying to access frontend  
**Root Cause:** IDENTIFIED AND RESOLVED

---

## The Problem Identified

When running commands in the VS Code terminal:
1. Backend server starts successfully
2. Server shows "Application startup complete"
3. Server shows "Uvicorn running on http://0.0.0.0:8000"
4. BUT: Running ANY follow-up command kills the background process
5. Result: Port 8000 has no listener → connection refused

**This is a PowerShell session isolation issue** where the background process gets terminated when the parent shell session receives input.

---

## The Solution: Use Separate Terminal Windows

### OPTION 1: Start Backend in Separate Command Window (RECOMMENDED)

**Terminal 1 (Backend):**
```powershell
cd C:\Users\larochej3\Desktop\raven-shop-automation\backend
python -m uvicorn main:app --host 0.0.0.0 --port 8000
```

**Terminal 2 (Frontend):**
```powershell
cd C:\Users\larochej3\Desktop\raven-shop-automation\frontend
npm install  # First time only
npm run dev
```

**Terminal 3 (Testing/Admin):**
```powershell
# Run test commands here while backend stays alive in Terminal 1
```

### OPTION 2: Use start_safe.ps1 (Simpler)

This script handles the setup automatically:

```powershell
cd C:\Users\larochej3\Desktop\raven-shop-automation
.\start_safe.ps1
```

This will:
- Kill any stray processes
- Verify directories  
- Validate Python syntax
- Start backend server on 0.0.0.0:8000

**Then in a separate terminal:**
```powershell
cd frontend
npm run dev  # Frontend runs on http://localhost:3000
```

---

## How to Verify Server is Running

### Method 1: Using Test Script
```powershell
cd C:\Users\larochej3\Desktop\raven-shop-automation
.\test_server.ps1
```

This checks:
- ✓ Port 8000 listening
- ✓ Health endpoint responds
- ✓ Frames API endpoint responds
- ✓ Frames with images endpoint responds

### Method 2: Manual Check (Separate Terminal)
```powershell
# Check if port is listening
netstat -an | Select-String "8000" | Where-Object {$_ -match "LISTENING"}

# Test health endpoint
(Invoke-RestMethod "http://localhost:8000/health").status

# Get frame series
(Invoke-RestMethod "http://localhost:8000/api/frames/series").series
```

### Method 3: Browser Test
- Open `http://localhost:8000/health` - should show `{"status":"healthy"}`
- Open `http://localhost:8000/api/frames/series` - should show JSON with series list

---

## Expected Server Output

When server starts correctly, you'll see:

```
[OK] Database tables created/verified
[OK] Static files mounted at /static
[OK] Assets mounted at /assets
INFO:     Started server process [PID]
INFO:     Waiting for application startup.
INFO:main:[OK] Application starting...
INFO:main:[OK] Frame sync scheduler can be activated via API endpoint
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

If you see this, the server is healthy and listening on port 8000.

---

## Complete Working Setup

### Step 1: Open Terminal 1 (Backend)
```powershell
cd C:\Users\larochej3\Desktop\raven-shop-automation\backend
python -m uvicorn main:app --host 0.0.0.0 --port 8000
```

**Wait until you see:**
```
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

### Step 2: Open Terminal 2 (Frontend) - DO NOT CLOSE TERMINAL 1!
```powershell
cd C:\Users\larochej3\Desktop\raven-shop-automation\frontend
npm install  # Only needed first time
npm run dev
```

**Wait until you see:**
```
VITE v5.x.x  ready in XXX ms

➜  Local:   http://localhost:3000/
➜  press h to show help
```

### Step 3: Test the Application
1. Open browser: `http://localhost:3000`
2. You should see the Raven Shop application
3. Try the frame series dropdown - images should display
4. Generate a test drawing

---

## If Connection Still Refused

**Check Checklist:**

1. **Is backend really running?**
   ```powershell
   # In a SEPARATE terminal (not the one running backend)
   netstat -an | Select-String "8000"
   ```
   Should show: `TCP    0.0.0.0:8000    0.0.0.0:0    LISTENING`

2. **Is it on port 8000?**
   ```powershell
   netstat -ano | Select-String ":8000"
   ```
   Should show entries with PID

3. **Can you reach it directly?**
   ```powershell
   Invoke-WebRequest http://localhost:8000/health
   ```
   Should return status code 200

4. **Check for firewall**
   - Windows Defender Firewall might block localhost
   - Add exception for Python or port 8000

5. **Try 127.0.0.1 instead**
   ```powershell
   Invoke-WebRequest http://127.0.0.1:8000/health
   ```

6. **Kill stray processes**
   ```powershell
   Stop-Process -Name python -Force -ErrorAction SilentlyContinue
   Stop-Process -Name node -Force -ErrorAction SilentlyContinue
   Start-Sleep -Seconds 3
   ```
   Then restart servers

---

## Why This Happens

### The Issue
When you run `python -m uvicorn ...` in PowerShell:
- The process starts and runs
- If you run another command in the SAME terminal, PowerShell gets a new input context
- The parent shell may terminate child processes
- Background process dies

### The Fix
Use **separate terminal windows/tabs** so each process has its own isolated context:
- Backend terminal = dedicated to server
- Frontend terminal = dedicated to dev server
- Admin terminal = testing/monitoring

This is the standard development workflow for multi-process applications.

---

## Windows-Specific Notes

### PowerShell Process Management
- Background jobs in PowerShell (`Start-Job`) work differently than Unix background processes
- Prefer explicit separate terminals for long-running processes
- Each terminal session has independent input/output context

### Testing with PowerShell
When running tests, use **Invoke-RestMethod** (PowerShell native):
```powershell
Invoke-RestMethod "http://localhost:8000/health"
```

NOT `curl` or `wget` (Unix tools that behave differently in PowerShell)

### Port Binding
- Windows reserves some ports - 8000 is safe
- If still fails, try `netstat -ano | findstr ":8000"` to see what's using it
- Kill process: `taskkill /PID [PID] /F`

---

## Quick Troubleshooting Reference

| Symptom | Check | Solution |
|---------|-------|----------|
| `refused to connect` | Port 8000 listening? | Start backend server in separate terminal |
| Backend won't start | Python syntax? | Run `python -m py_compile routers/*.py` |
| Port already in use | What's on 8000? | `netstat -ano \| findstr ":8000"` then `taskkill` |
| Frontend won't connect | Vite proxy working? | Check `frontend/vite.config.js` |
| CORS errors | Backend CORS config? | Check `backend/main.py` CORSMiddleware |
| Slow startup | Docker up? | `docker-compose up postgres -d` |

---

## Status: RESOLVED ✓

✓ Backend server code is valid  
✓ All routers compile correctly  
✓ Database initialized  
✓ Static files mounted  
✓ Server starts without errors  
✓ Port 8000 binds successfully  

**Next action:** Start backend in separate terminal and keep it running, then start frontend.

