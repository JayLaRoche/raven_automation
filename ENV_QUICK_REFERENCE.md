# Environment Configuration Quick Reference

## One-Line Setup

```bash
# Copy environment template
cp .env.example .env

# Edit with your values
# nano .env  (or use your editor)

# Start development
./start_dev.sh
```

## Environment Variables by Priority

### CRITICAL (Must Set in Production)

```bash
APP_ENV=production
DATABASE_URL=postgresql://user:password@host:5432/db
JWT_SECRET_KEY=generate_with_openssl_rand_-base64_32
VITE_API_URL=https://api.yourdomain.com
CORS_ORIGINS=https://yourdomain.com,https://www.yourdomain.com
```

### IMPORTANT (Recommended for All Environments)

```bash
DEBUG=false                    # true only in development
BACKEND_HOST=0.0.0.0
BACKEND_PORT=8000
VITE_PORT=3000
GOOGLE_SHEETS_CREDENTIALS_PATH=./credentials/google-sheets.json
GOOGLE_SHEET_ID=your_sheet_id
```

### OPTIONAL (Has Good Defaults)

```bash
LOG_LEVEL=INFO               # DEBUG in dev, INFO in prod
MAX_UPLOAD_SIZE_MB=50
FRAME_SYNC_INTERVAL=60
DB_PROVIDER=postgresql       # or sqlite for dev
FEATURE_PDF_EXPORT=true
FEATURE_GOOGLE_SHEETS_SYNC=true
FEATURE_FRAME_LIBRARY=true
```

## Quick Start Commands

```bash
# Development
export APP_ENV=development
./start_dev.sh

# Production Build
export APP_ENV=production
cd frontend && npm run build

# Production Backend
export APP_ENV=production
cd backend && gunicorn -w 4 main:app

# Check Configuration
curl http://localhost:8000/

# Test API
curl http://localhost:8000/api/frames/series
```

## Database Setup

### PostgreSQL (Production)
```bash
# Connection string format
postgresql://username:password@host:port/database

# Example
DATABASE_URL=postgresql://raven_user:MyPassword123@prod-db.example.com:5432/raven_drawings
```

### SQLite (Development Only)
```bash
DB_PROVIDER=sqlite
SQLITE_DB_PATH=./data/raven_drawings.db
```

## Environment Checklist

### Development
- [ ] `APP_ENV=development`
- [ ] `DEBUG=true`
- [ ] `DATABASE_URL` set (PostgreSQL or SQLite)
- [ ] `VITE_API_URL=http://localhost:8000`
- [ ] CORS allows localhost

### Staging
- [ ] `APP_ENV=staging`
- [ ] `DEBUG=false`
- [ ] `DATABASE_URL` points to staging database
- [ ] `JWT_SECRET_KEY` is strong and set
- [ ] `VITE_API_URL` points to staging backend
- [ ] Certificates are valid

### Production
- [ ] `APP_ENV=production`
- [ ] `DEBUG=false`
- [ ] `DATABASE_URL` points to production database
- [ ] `JWT_SECRET_KEY` is strong, generated, and stored in secrets manager
- [ ] `VITE_API_URL` points to production backend (HTTPS only)
- [ ] `CORS_ORIGINS` lists only HTTPS domains
- [ ] SSL/TLS certificates are installed
- [ ] Backups are configured
- [ ] Monitoring is enabled

## Common Issues & Fixes

| Issue | Cause | Fix |
|-------|-------|-----|
| Database connection refused | PostgreSQL not running or wrong URL | Check `psql -h localhost` or use SQLite |
| Frontend can't reach backend | VITE_API_URL is wrong | Check `echo $VITE_API_URL` or update .env |
| CORS errors | Frontend URL not in CORS_ORIGINS | Add frontend URL to CORS_ORIGINS in .env |
| Production error: "JWT secret not set" | JWT_SECRET_KEY is default | Generate and set: `openssl rand -base64 32` |
| Ports already in use | Another app using 3000 or 8000 | Change in .env or kill the other process |

## Security Notes

🔒 **NEVER:**
- Hardcode secrets in code
- Commit .env to git
- Use default passwords
- Run production with DEBUG=true
- Use HTTP in production

✅ **ALWAYS:**
- Use environment variables for secrets
- Keep .env in .gitignore
- Use HTTPS in production
- Set strong passwords
- Generate JWT_SECRET_KEY: `openssl rand -base64 32`
- Use managed database services
- Rotate secrets regularly
