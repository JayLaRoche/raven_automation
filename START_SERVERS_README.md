# 🚀 How to Start Your Raven Shop Drawing App

## Quick Start (EASIEST)

**Option 1: Click the Batch File (Windows)**

Double-click this file to start both servers:
```
C:\Users\larochej3\Desktop\raven-shop-automation\START_SERVERS.bat
```

This will:
1. ✅ Open Backend server window (port 8000)
2. ✅ Open Frontend server window (port 3000)
3. ✅ Both servers will start automatically
4. You can close the first window that appears

Then visit: **http://localhost:3000**

---

## Manual Start (If Batch File Doesn't Work)

### Terminal 1 - Start Backend
```bash
cd C:\Users\larochej3\Desktop\raven-shop-automation\backend
uvicorn main:app --reload
```
✅ Backend will run on http://localhost:8000

### Terminal 2 - Start Frontend
```bash
cd C:\Users\larochej3\Desktop\raven-shop-automation\frontend
npm run dev
```
✅ Frontend will run on http://localhost:3000

### Browser
Visit: **http://localhost:3000**

---

## Stop the Servers

**If using batch file:**
- Close the Backend window (click X)
- Close the Frontend window (click X)

**If using manual terminals:**
- Press `CTRL+C` in each terminal window

---

## Troubleshooting

### Getting "Connection Refused"?
1. Make sure both server windows are open
2. Check that npm run dev is showing "Vite ready"
3. Try refreshing the browser (F5)

### Port Already in Use?
If ports 3000 or 8000 are already in use:

**For Frontend (3000):**
```bash
cd frontend
npm run dev -- --port 3001
```

**For Backend (8000):**
```bash
cd backend
uvicorn main:app --reload --port 8001
```

Then visit: http://localhost:3001

---

## What You Should See

When you open http://localhost:3000, you'll see:

```
┌─────────────────────────────────────────────────┐
│  Raven Custom Glass                             │
│  Shop Drawing Generator                         │
│                                                 │
│  [Generator] [Projects]                         │
├─────────────────────────────────────────────────┤
│                                                 │
│  LEFT PANEL:          │  RIGHT PANEL:           │
│  ├─ Frame Series      │  ├─ Drawing Canvas      │
│  ├─ Product Type      │  │  (preview area)      │
│  ├─ Width             │  │                      │
│  ├─ Height            │  │                      │
│  ├─ Glass Type        │  │                      │
│  ├─ Color             │  │                      │
│  ├─ Grids             │  └─ Export PNG button   │
│  └─ Generate Button   │                         │
└─────────────────────────────────────────────────┘
```

---

**Your app is ready! 🎉**

Just run the batch file or follow the manual steps above.
