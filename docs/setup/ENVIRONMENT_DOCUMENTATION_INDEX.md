# 📖 Environment Configuration - Complete Documentation Index

## 🎯 Start Here

**New to this setup?** Start with one of these:

1. **Want to develop locally?**
   → Read: [Quick Start Guide](#quick-start)
   → Then: `./start_dev.sh`

2. **Deploying to production?**
   → Read: [ENVIRONMENT_SETUP.md - Production Deployment](ENVIRONMENT_SETUP.md#-production-deployment)
   → Then: Use [PRE_DEPLOYMENT_CHECKLIST.md](PRE_DEPLOYMENT_CHECKLIST.md)

3. **Just need quick reference?**
   → See: [ENV_QUICK_REFERENCE.md](ENV_QUICK_REFERENCE.md)

---

## 📚 Documentation Files

### Core Documentation

| File | Purpose | Read Time |
|------|---------|-----------|
| **[ENVIRONMENT_SETUP.md](ENVIRONMENT_SETUP.md)** | Complete guide for all environments | 20 min |
| **[ENV_QUICK_REFERENCE.md](ENV_QUICK_REFERENCE.md)** | Quick lookup for developers | 5 min |
| **[PRE_DEPLOYMENT_CHECKLIST.md](PRE_DEPLOYMENT_CHECKLIST.md)** | Verification before deployment | 10 min |
| **[ENVIRONMENT_CONFIGURATION_SUMMARY.md](ENVIRONMENT_CONFIGURATION_SUMMARY.md)** | What was audited and changed | 10 min |
| **[ENVIRONMENT_AUDIT_COMPLETE.md](ENVIRONMENT_AUDIT_COMPLETE.md)** | Technical audit results | 5 min |

### Configuration Files

| File | Purpose |
|------|---------|
| **[.env.example](.env.example)** | Environment variable template |
| **[backend/app/config.py](backend/app/config.py)** | Central configuration management |
| **[backend/main.py](backend/main.py)** | FastAPI application (updated) |
| **[backend/app/database.py](backend/app/database.py)** | Database configuration (updated) |
| **[frontend/vite.config.js](frontend/vite.config.js)** | Vite configuration (updated) |

### Helper Scripts

| File | Purpose |
|------|---------|
| **[start_dev.sh](start_dev.sh)** | Single command to start development |

---

## 🚀 Quick Start

### Development (5 minutes)

```bash
# 1. Create environment
cp .env.example .env

# 2. Start everything
./start_dev.sh

# 3. Open browser
# Frontend: http://localhost:3000
# Backend:  http://localhost:8000
# API Docs: http://localhost:8000/docs
```

### Production (30 minutes)

```bash
# 1. Create environment
cp .env.example .env

# 2. Configure (edit .env with production values)
nano .env
# Set: APP_ENV=production, DATABASE_URL, JWT_SECRET_KEY, etc.

# 3. Run deployment checklist
# See: PRE_DEPLOYMENT_CHECKLIST.md

# 4. Deploy
# Follow: ENVIRONMENT_SETUP.md → Production Deployment
```

---

## 🎯 Common Tasks

### "I need to run this locally"
1. Read: [Quick Start](#quick-start) above
2. Run: `./start_dev.sh`
3. Done! Open http://localhost:3000

### "I need to deploy to production"
1. Read: [ENVIRONMENT_SETUP.md](ENVIRONMENT_SETUP.md)
2. Prepare: Use [PRE_DEPLOYMENT_CHECKLIST.md](PRE_DEPLOYMENT_CHECKLIST.md)
3. Deploy: Follow production deployment guide

### "Where do I set environment variables?"
1. Development: Edit `.env` file
2. Production: Use secrets manager (AWS Secrets Manager, Azure Key Vault, etc.)
3. Reference: [ENV_QUICK_REFERENCE.md](ENV_QUICK_REFERENCE.md#critical-must-set-in-production)

### "How do I switch between dev and production?"
1. Set: `APP_ENV=development` (or `production`)
2. Reload: Restart the application
3. Verify: Check startup logs for configuration summary

### "I'm getting a database error"
1. Check: [ENVIRONMENT_SETUP.md - Troubleshooting](ENVIRONMENT_SETUP.md#-troubleshooting)
2. Verify: Database URL in `.env`
3. Test: Try SQLite for development

### "Frontend can't reach backend"
1. Check: `VITE_API_URL` in `.env`
2. Verify: Backend is running
3. Test: `curl http://localhost:8000/api/frames/series`
4. See: [ENVIRONMENT_SETUP.md - CORS error](ENVIRONMENT_SETUP.md#cors-error-on-frontend)

---

## 🔐 Security

### Before Committing to Git
- [ ] `.env` is NOT committed
- [ ] No secrets in code
- [ ] `.gitignore` protects secrets
- [ ] See: [.gitignore](.gitignore)

### Before Deploying to Production
- [ ] All checklist items complete
- [ ] See: [PRE_DEPLOYMENT_CHECKLIST.md](PRE_DEPLOYMENT_CHECKLIST.md)
- [ ] JWT secret is set
- [ ] Database URL is production
- [ ] CORS allows HTTPS only
- [ ] Debug mode is OFF

### Security Best Practices
1. Never hardcode secrets
2. Use environment variables
3. Never commit `.env`
4. Use HTTPS in production
5. Restrict CORS to known domains
6. Keep secrets in a secrets manager
7. See: [ENVIRONMENT_SETUP.md - Security](ENVIRONMENT_SETUP.md#-security-configuration-for-production)

---

## 📊 Configuration Overview

### What Controls What

```
APP_ENV (environment variable)
├─ development  → Uses debug mode, SQLite ok, localhost CORS
├─ staging      → Uses production config, PostgreSQL required
└─ production   → Enforces security, no debug, HTTPS only

DATABASE_URL
├─ PostgreSQL   → Production ready
└─ SQLite       → Development only

CORS_ORIGINS
├─ localhost    → Development
└─ https://...  → Production (HTTPS only)

JWT_SECRET_KEY
├─ Set          → Used for authentication
└─ Not set      → Production error

DEBUG
├─ true         → Development (detailed logging)
└─ false        → Production (safe logging)
```

---

## 🔄 Environment Variables by Type

### Critical (Production)
```
APP_ENV=production
DATABASE_URL=postgresql://...
JWT_SECRET_KEY=strong_secret
VITE_API_URL=https://...
CORS_ORIGINS=https://...
```

### Important
```
DEBUG=false
BACKEND_PORT=8000
VITE_PORT=3000
LOG_LEVEL=INFO
```

### Optional (Has Defaults)
```
MAX_UPLOAD_SIZE_MB=50
FRAME_SYNC_INTERVAL=60
GOOGLE_SHEETS_CREDENTIALS_PATH=...
```

See: [ENV_QUICK_REFERENCE.md](ENV_QUICK_REFERENCE.md) for complete list

---

## 📁 Project Structure

```
raven-shop-automation/
├── .env.example              ← Copy this to .env
├── .gitignore                ← Protects .env
├── .env                       ← NEVER commit this
├── ENVIRONMENT_SETUP.md      ← Complete guide
├── ENV_QUICK_REFERENCE.md    ← Quick lookup
├── PRE_DEPLOYMENT_CHECKLIST.md ← Deployment verification
├── start_dev.sh              ← One-command startup
├── backend/
│   ├── app/
│   │   ├── config.py         ← Configuration management
│   │   └── database.py       ← Database setup (updated)
│   ├── main.py               ← FastAPI app (updated)
│   └── routers/
├── frontend/
│   ├── .env.example          ← Frontend env template
│   ├── vite.config.js        ← Vite config (updated)
│   └── src/
└── docker-compose.yml        ← For database setup
```

---

## 🧪 Testing Your Configuration

### Backend
```bash
# Test database connection
curl http://localhost:8000/api/frames/series

# View API documentation
open http://localhost:8000/docs

# Check configuration (in logs on startup)
# Look for: RAVEN SHOP AUTOMATION - CONFIGURATION SUMMARY
```

### Frontend
```bash
# Test API connection (in browser console)
console.log(import.meta.env.VITE_API_URL)

# Should see current API endpoint
# Development: http://localhost:8000
# Production: https://api.yourdomain.com
```

### Full Stack
```bash
# 1. Start everything
./start_dev.sh

# 2. Open browser to http://localhost:3000
# 3. Try to generate a drawing
# 4. Check for errors in browser console (F12)
```

---

## 🆘 Troubleshooting Flow

1. **Error in backend logs?**
   → Check: [ENVIRONMENT_SETUP.md - Troubleshooting](ENVIRONMENT_SETUP.md#-troubleshooting)

2. **Frontend not connecting?**
   → Check: VITE_API_URL in `.env`
   → See: [ENV_QUICK_REFERENCE.md](ENV_QUICK_REFERENCE.md#common-issues--fixes)

3. **Database not working?**
   → Check: DATABASE_URL syntax
   → Try: SQLite for development
   → See: [ENVIRONMENT_SETUP.md - Database](ENVIRONMENT_SETUP.md#-database-configuration)

4. **Deployment failing?**
   → Use: [PRE_DEPLOYMENT_CHECKLIST.md](PRE_DEPLOYMENT_CHECKLIST.md)
   → Read: [ENVIRONMENT_SETUP.md - Production](ENVIRONMENT_SETUP.md#-backend-deployment)

5. **Still stuck?**
   → Check: Backend startup logs
   → Review: Configuration summary
   → See: All documentation files

---

## 📞 Key Contacts/Resources

### Configuration
- **Template**: [.env.example](.env.example)
- **Code**: [backend/app/config.py](backend/app/config.py)
- **Reference**: [ENV_QUICK_REFERENCE.md](ENV_QUICK_REFERENCE.md)

### Setup & Development
- **Guide**: [ENVIRONMENT_SETUP.md](ENVIRONMENT_SETUP.md)
- **Quick Start**: [Quick Start](#quick-start) above
- **Scripts**: [start_dev.sh](start_dev.sh)

### Deployment
- **Checklist**: [PRE_DEPLOYMENT_CHECKLIST.md](PRE_DEPLOYMENT_CHECKLIST.md)
- **Guide**: [ENVIRONMENT_SETUP.md - Production](ENVIRONMENT_SETUP.md#-backend-deployment)

### Information
- **Summary**: [ENVIRONMENT_CONFIGURATION_SUMMARY.md](ENVIRONMENT_CONFIGURATION_SUMMARY.md)
- **Audit**: [ENVIRONMENT_AUDIT_COMPLETE.md](ENVIRONMENT_AUDIT_COMPLETE.md)

---

## ✅ Next Steps

1. **First time here?**
   - [ ] Read this file (you're done!)
   - [ ] Follow [Quick Start](#quick-start)
   - [ ] Run `./start_dev.sh`

2. **Ready to deploy?**
   - [ ] Read [ENVIRONMENT_SETUP.md](ENVIRONMENT_SETUP.md)
   - [ ] Use [PRE_DEPLOYMENT_CHECKLIST.md](PRE_DEPLOYMENT_CHECKLIST.md)
   - [ ] Deploy following production guide

3. **Need help?**
   - [ ] Check [ENV_QUICK_REFERENCE.md](ENV_QUICK_REFERENCE.md)
   - [ ] See troubleshooting section
   - [ ] Review relevant documentation file

---

## 🎓 Learning Path

```
START HERE
    ↓
[ENVIRONMENT_CONFIGURATION_SUMMARY.md] ← What changed
    ↓
[Choose your path]
    ├─ Local Development
    │   └─ [ENVIRONMENT_SETUP.md] → Development section
    │
    └─ Production Deployment
        ├─ [ENVIRONMENT_SETUP.md] → Security & Production sections
        └─ [PRE_DEPLOYMENT_CHECKLIST.md] → Verify before deploying
    
    ↓
[ENV_QUICK_REFERENCE.md] ← Keep handy while working
```

---

## 📋 Document Legend

| Icon | Meaning |
|------|---------|
| ✅ | Completed/Verified |
| ⚠️ | Warning/Important |
| 🚀 | Production/Deployment |
| 🐛 | Debugging/Troubleshooting |
| 🔐 | Security |
| 📊 | Configuration |

---

**Last Updated**: January 7, 2026
**Version**: 1.0 - Initial Environment Audit Complete

