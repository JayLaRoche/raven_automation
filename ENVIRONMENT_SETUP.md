# 🚀 Development & Deployment Guide

## Quick Start

### Development Mode

Start both frontend and backend servers with hot reload:

```bash
# Linux/macOS
./start_dev.sh

# Windows (PowerShell)
.\START_SERVERS.bat
```

This starts:
- **Frontend**: http://localhost:3000 (React with Vite)
- **Backend**: http://localhost:8000 (FastAPI)
- **API Docs**: http://localhost:8000/docs (Swagger UI)

### Production Mode

See [Production Deployment](#production-deployment) section below.

---

## 📋 Environment Configuration

### Setting Up Environment Variables

1. **Copy the template file:**
   ```bash
   cp .env.example .env
   ```

2. **Edit `.env` with your configuration:**
   ```bash
   nano .env  # Linux/macOS
   # or edit in VS Code
   ```

### Environment File Structure

The `.env` file controls application behavior across all environments:

```dotenv
# Determines which database and configuration to use
APP_ENV=development  # Options: development, staging, production

# Database connection (auto-selected based on APP_ENV)
DATABASE_URL=postgresql://user:pass@localhost:5432/raven_drawings

# Frontend API endpoint
VITE_API_URL=http://localhost:8000

# Google Sheets integration
GOOGLE_SHEETS_CREDENTIALS_PATH=./credentials/google-sheets.json

# See .env.example for all available options
```

---

## 🔄 Development vs Production

### Development Environment (`APP_ENV=development`)

**Configuration:**
- Hot reload enabled for both frontend and backend
- Debug logging enabled
- CORS allows localhost origins
- SQLite fallback available (no PostgreSQL required)
- Detailed error messages
- Source maps included

**Start:**
```bash
export APP_ENV=development
./start_dev.sh
```

**Features:**
- ✅ Hot module reloading
- ✅ Detailed error pages
- ✅ Full debug logging
- ✅ API documentation at /docs
- ✅ CORS disabled for localhost development

### Production Environment (`APP_ENV=production`)

**Configuration:**
- Hot reload disabled
- Debug mode disabled
- CORS restricted to HTTPS origins only
- PostgreSQL required (no SQLite fallback)
- Optimized logging (INFO level only)
- Source maps disabled for security
- Secret management enforced

**Requirements:**
```bash
# CRITICAL: Must set these in production
APP_ENV=production
DATABASE_URL=postgresql://user:password@prod-db-host:5432/raven_drawings
VITE_API_URL=https://api.yourdomain.com
JWT_SECRET_KEY=generate_strong_secret_key_here
CORS_ORIGINS=https://yourdomain.com,https://www.yourdomain.com
```

**Start:**
```bash
export APP_ENV=production
cd backend && uvicorn main:app --host 0.0.0.0 --port 8000
cd ../frontend && npm run build && npm run preview
```

---

## 🗄️ Database Configuration

### Development: Local PostgreSQL

```bash
# 1. Install PostgreSQL (if not already installed)
# macOS: brew install postgresql@15
# Ubuntu: sudo apt-get install postgresql postgresql-contrib

# 2. Start PostgreSQL service
# macOS: brew services start postgresql@15
# Ubuntu: sudo systemctl start postgresql

# 3. Create database and user
createuser -P raven_user
createdb -O raven_user raven_drawings

# 4. Update .env
DATABASE_URL=postgresql://raven_user:your_password@localhost:5432/raven_drawings

# 5. Run migrations
cd backend
alembic upgrade head
```

### Development: SQLite (No PostgreSQL)

For quick local development without PostgreSQL:

```bash
# Set in .env
DB_PROVIDER=sqlite
SQLITE_DB_PATH=./data/raven_drawings.db

# Database will auto-create on first run
# No migration needed - just start the app
```

### Production: PostgreSQL

```bash
# Use a managed service (recommended):
# - Azure Database for PostgreSQL
# - AWS RDS
# - Google Cloud SQL
# - DigitalOcean Managed Databases

# Set DATABASE_URL to your managed service connection string
DATABASE_URL=postgresql://user:password@prod-db.database.windows.net:5432/raven_drawings
```

---

## 🔐 Security Configuration for Production

### 1. Database

```bash
# ✓ Use strong passwords
# ✓ Use managed PostgreSQL (not self-hosted)
# ✓ Enable SSL connections
# ✓ Restrict network access to application servers only
DATABASE_URL=postgresql://user:STRONG_PASSWORD@managed-db-host:5432/db
```

### 2. CORS (Cross-Origin Resource Sharing)

```bash
# Development: allows localhost
CORS_ORIGINS=http://localhost:3000,http://localhost:8000

# Production: ONLY HTTPS origins
CORS_ORIGINS=https://yourdomain.com,https://www.yourdomain.com,https://api.yourdomain.com
```

### 3. JWT Secret

```bash
# Generate a strong secret (use a cryptography tool or online generator)
# NEVER use the default value in production!

# Generate a secret (Linux/macOS):
openssl rand -base64 32

# Set it:
JWT_SECRET_KEY=your_generated_secret_here
```

### 4. Environment Secrets

```bash
# NEVER hardcode secrets in the application
# NEVER commit .env to version control
# Use environment-specific secret management:

# Local: .env file (git-ignored)
# Staging: GitHub Secrets / Platform secrets
# Production: Azure Key Vault / AWS Secrets Manager / HashiCorp Vault
```

### 5. API Configuration

```bash
# Disable debug mode in production
DEBUG=false

# Set log level to INFO (not DEBUG)
LOG_LEVEL=INFO

# Disable sourcemaps for security
# (vite.config.js is pre-configured for this)
```

---

## 📦 Frontend Build & Deployment

### Development Build

```bash
cd frontend
npm install        # Install dependencies
npm run dev        # Start dev server with hot reload
```

### Production Build

```bash
cd frontend
npm install        # Install dependencies
npm run build      # Create optimized build in ./dist
npm run preview    # Preview the production build locally
```

**Deploy the `dist/` folder to:**
- Vercel
- Netlify
- AWS S3 + CloudFront
- Azure Static Web Apps
- GitHub Pages

---

## 🚢 Backend Deployment

### Docker Deployment (Recommended)

```dockerfile
# Dockerfile example
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
ENV APP_ENV=production
ENV DEBUG=false

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Manual Deployment

```bash
# SSH into your server
ssh user@production-server

# Clone the repository
git clone https://github.com/yourusername/raven-automation.git
cd raven-automation/backend

# Create virtual environment
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Set environment variables
export APP_ENV=production
export DATABASE_URL=postgresql://...
export JWT_SECRET_KEY=...

# Run with production WSGI server (Gunicorn)
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 main:app
```

---

## 🔍 Verifying Your Configuration

### Check Backend Configuration

```bash
# View current settings
curl http://localhost:8000/

# Check API docs
open http://localhost:8000/docs

# Test database connection
curl http://localhost:8000/api/frames/series
```

### Check Frontend Configuration

```bash
# View current API URL in browser console
# Open http://localhost:3000 and run:
console.log(import.meta.env.VITE_API_URL)
```

### Environment Summary

The backend logs its configuration on startup:

```
╔════════════════════════════════════════════════════════════════╗
║           RAVEN SHOP AUTOMATION - CONFIGURATION SUMMARY         ║
╠════════════════════════════════════════════════════════════════╣
║ Environment:      DEVELOPMENT
║ Debug Mode:       ON
║ Database:         POSTGRESQL
║ DB Host:          localhost
║ Backend Server:   0.0.0.0:8000
║ CORS Origins:     2 configured
║ Features:         PDF=true | Sheets=true | Frames=true
╚════════════════════════════════════════════════════════════════╝
```

---

## 🐛 Troubleshooting

### "Database connection refused"

```bash
# Check if PostgreSQL is running
pg_isready -h localhost -p 5432

# Or check in .env if you're using SQLite
# SQLite doesn't require a server, just change:
DB_PROVIDER=sqlite
SQLITE_DB_PATH=./data/raven_drawings.db
```

### "CORS error on frontend"

```bash
# Check your CORS_ORIGINS in .env
echo $CORS_ORIGINS

# Ensure frontend URL is in the list
# Development: add http://localhost:3000
# Production: add https://yourdomain.com
```

### "API requests returning 404"

```bash
# Check VITE_API_URL in frontend
# Development: should be http://localhost:8000
# Production: should be https://api.yourdomain.com

# Verify backend is running
curl http://localhost:8000/docs
```

### "JWT Secret not set (production error)"

```bash
# Generate a secure secret
openssl rand -base64 32

# Add to .env
JWT_SECRET_KEY=your_generated_secret

# Or set as environment variable before running
export JWT_SECRET_KEY=your_secret
```

---

## 📋 Pre-Deployment Checklist

- [ ] Copy `.env.example` to `.env`
- [ ] Update all environment variables for your deployment environment
- [ ] Set `APP_ENV=production`
- [ ] Generate and set `JWT_SECRET_KEY`
- [ ] Configure `DATABASE_URL` to your production database
- [ ] Update `VITE_API_URL` to your production backend URL
- [ ] Update `CORS_ORIGINS` to your production domain (HTTPS only)
- [ ] Set `DEBUG=false`
- [ ] Set `LOG_LEVEL=INFO`
- [ ] Disable sourcemaps: verify `vite.config.js` has `sourcemap: false`
- [ ] Test the production build locally: `npm run build && npm run preview`
- [ ] Test API connections in production environment
- [ ] Set up database backups
- [ ] Set up monitoring and logging
- [ ] Set up SSL/TLS certificates (HTTPS)
- [ ] Run security audit on dependencies

---

## 📞 Support

For issues or questions, check:
1. Backend logs: `./logs/app.log`
2. Browser console: Press F12 in your browser
3. API documentation: `http://localhost:8000/docs`
4. Configuration summary: Watch backend startup messages

