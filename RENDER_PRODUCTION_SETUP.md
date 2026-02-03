# Render.com Production Deployment Guide

## ✅ Pre-Deployment Checklist

### 1. Files Verified
- [x] `render.yaml` configured with database and services
- [x] Static files (95 PNG images) tracked in git
- [x] Frontend .env.production configured
- [x] Backend requirements.txt includes all dependencies
- [x] Database migrations configured with Alembic

### 2. Environment Variables Required

#### Backend Service (Auto-configured by Render)
```env
DATABASE_URL=<auto-populated from PostgreSQL database>
CORS_ORIGINS=https://raven-frontend.onrender.com
APP_ENV=production
ENVIRONMENT=production
DEBUG=false
LOG_LEVEL=INFO
```

#### Frontend Service
```env
VITE_API_URL=https://raven-backend.onrender.com
NODE_VERSION=20.11.0
```

## 🚀 Deployment Steps

### Step 1: Connect GitHub Repository
1. Go to https://render.com/dashboard
2. Click "New" → "Blueprint"
3. Connect your GitHub repository: `JayLaRoche/raven_automation`
4. Render will detect `render.yaml` and create all services

### Step 2: Verify Services Created
Render will automatically create:
- ✅ **raven-db** - PostgreSQL database (Free tier)
- ✅ **raven-backend** - Python web service (Free tier)
- ✅ **raven-frontend** - Static site (Free tier)

### Step 3: Monitor Deployment
Watch the build logs for each service:

**Backend Build Sequence:**
```bash
pip install -r requirements.txt
alembic upgrade head         # Creates database tables
python init_db.py           # Seeds frame series data
uvicorn main:app --host 0.0.0.0 --port $PORT
```

**Frontend Build Sequence:**
```bash
npm ci
npm run build               # Creates production build in dist/
```

### Step 4: Verify Static Files Deployed
After backend deployment completes, check:
```bash
curl https://raven-backend.onrender.com/static/frames/series-86-head.png
# Should return image (not 404)
```

### Step 5: Verify Database Connection
```bash
curl https://raven-backend.onrender.com/health
# Expected response:
{
  "status": "healthy",
  "timestamp": "2026-02-03T12:00:00",
  "database": "connected"
}
```

### Step 6: Test Frame Series Endpoint
```bash
curl https://raven-backend.onrender.com/api/frames/series-with-images
# Should return:
{
  "series": [
    {"name": "86", "thumbnail": "/static/frames/series-86-thumbnail.png"},
    {"name": "135", "thumbnail": "/static/frames/series-135-thumbnail.png"},
    ...
  ]
}
```

### Step 7: Test Frontend
Visit: https://raven-frontend.onrender.com

**Verify:**
- [x] Frame series dropdown shows images
- [x] Generate PDF button works
- [x] Export button creates PDF download
- [x] Projects can be created and saved

## 🔧 Troubleshooting

### Issue: Static Images Not Loading
**Symptoms:** Frame series dropdown shows no images

**Fix:**
1. Check backend logs for static mount errors
2. Verify in Render shell:
   ```bash
   ls -la /opt/render/project/src/static/frames/
   ```
3. If missing, check `.dockerignore` doesn't exclude `static/`

### Issue: PDF Generation Fails
**Symptoms:** "Generate PDF" button shows error

**Fix:**
1. Check backend logs: `FileNotFoundError` for images
2. Verify ReportLab/Pillow installed:
   ```bash
   pip list | grep -i "reportlab\|pillow"
   ```
3. Check `/app/outputs` directory exists and is writable

### Issue: Projects Not Saving
**Symptoms:** "Create Project" fails with 500 error

**Fix:**
1. Check database connection in health endpoint
2. Verify migrations ran:
   ```bash
   alembic current
   # Should show: abc123 (head)
   ```
3. Manually run migrations if needed:
   ```bash
   alembic upgrade head
   python init_db.py
   ```

### Issue: CORS Errors in Browser
**Symptoms:** Network errors when frontend calls backend

**Fix:**
1. Update backend environment variable:
   ```env
   CORS_ORIGINS=https://raven-frontend.onrender.com
   ```
2. Redeploy backend service

## 📊 Service URLs

After deployment:
- **Frontend:** https://raven-frontend.onrender.com
- **Backend API:** https://raven-backend.onrender.com
- **Database:** Internal Render network (not public)

## 🔄 Continuous Deployment

Render auto-deploys on git push to `main` branch:
```bash
git add .
git commit -m "Update feature"
git push origin main
# Render automatically builds and deploys
```

## 💾 Database Backups

**Manual Backup:**
1. Go to Render Dashboard → raven-db
2. Click "Backups" tab
3. Click "Create Backup"

**Restore from Backup:**
1. Render Dashboard → raven-db → Backups
2. Select backup → Click "Restore"

## 🎯 Post-Deployment Verification

Run this checklist after deployment:

```bash
# 1. Health check
curl https://raven-backend.onrender.com/health

# 2. Frame series API
curl https://raven-backend.onrender.com/api/frames/series

# 3. Static file
curl -I https://raven-backend.onrender.com/static/frames/series-86-head.png

# 4. Frontend loads
curl -I https://raven-frontend.onrender.com

# 5. Create test project
curl -X POST https://raven-backend.onrender.com/api/projects/ \
  -H "Content-Type: application/json" \
  -d '{"project_name": "Test Project", "customer_name": "Test Customer"}'
```

All should return 200 OK status.

## 🚨 Known Limitations (Free Tier)

- Services spin down after 15 minutes of inactivity
- First request after spin-down takes ~30 seconds
- Database limited to 1GB storage
- No custom domains (upgrade to paid tier)

## 📝 Maintenance

### Update Dependencies
```bash
# Update requirements.txt
pip install --upgrade package-name
pip freeze > requirements.txt

# Commit and push
git add requirements.txt
git commit -m "Update dependencies"
git push origin main
```

### Add New Environment Variable
1. Render Dashboard → Service → Environment
2. Add variable
3. Click "Save Changes"
4. Service auto-redeploys

### View Logs
Render Dashboard → Service → Logs (real-time)

---

**Last Updated:** 2026-02-03  
**Deployed By:** Raven Shop Automation Team
