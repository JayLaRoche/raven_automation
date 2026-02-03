# Production Deployment Guide

## 🚀 Quick Start

Your application is now ready for production deployment using Docker!

### Prerequisites
- Docker Desktop installed ([download here](https://www.docker.com/products/docker-desktop))
- Git repository: https://github.com/JayLaRoche/raven_automation.git

### Deployment Steps

#### 1. Configure Environment
```powershell
# Copy the template
cp .env.production.example .env.production

# Edit .env.production and set:
# - Strong passwords for PostgreSQL
# - Your production domain in CORS_ORIGINS
# - Generate secret keys using: python -c "import secrets; print(secrets.token_urlsafe(32))"
```

#### 2. Deploy with One Command
```powershell
# Build and start production containers
.\deploy.ps1 -Build

# Or manually:
docker-compose -f docker-compose.prod.yml build
docker-compose -f docker-compose.prod.yml up -d
```

#### 3. Access Your Application
- **Frontend**: http://localhost
- **API**: http://localhost/api
- **Health Check**: http://localhost/api/health

### Deployment Script Commands

```powershell
# Build and deploy
.\deploy.ps1 -Build

# Check status
.\deploy.ps1 -Status

# View logs
.\deploy.ps1 -Logs

# Stop containers
.\deploy.ps1 -Stop

# Clean rebuild (removes all data!)
.\deploy.ps1 -Clean
```

## 📁 Docker Infrastructure

### Services
1. **postgres**: PostgreSQL 15 Alpine database with persistent volume
2. **backend**: FastAPI server with automatic Alembic migrations
3. **frontend**: React app served by Nginx with reverse proxy

### Files Created
- `backend/Dockerfile.prod` - Backend container image
- `frontend/Dockerfile.prod` - Frontend container image (multi-stage build)
- `frontend/nginx.conf` - Nginx reverse proxy configuration
- `docker-compose.prod.yml` - Service orchestration
- `.env.production.example` - Environment template
- `deploy.ps1` - Automated deployment script

## 🔧 Configuration Details

### Backend (port 8000 internal)
- Python 3.11 slim base
- PostgreSQL client installed
- Runs Alembic migrations on startup
- Health check at `/health`

### Frontend (port 80)
- Multi-stage build (Node 20 Alpine → Nginx Alpine)
- Nginx serves static files
- Reverse proxy: `/api/*` → `backend:8000`
- SPA routing with fallback to index.html

### Database
- PostgreSQL 15 Alpine
- Persistent volume: `postgres_data_prod`
- Healthcheck: `pg_isready`
- Credentials from `.env.production`

## 🔐 Security Checklist

- [ ] Changed default PostgreSQL password in `.env.production`
- [ ] Generated strong `SECRET_KEY` and `JWT_SECRET`
- [ ] Updated `CORS_ORIGINS` to include your domain
- [ ] `.env.production` is in `.gitignore` (already configured)
- [ ] Reviewed exposed ports in `docker-compose.prod.yml`

## 🌐 Production Domain Setup

To use a custom domain instead of localhost:

1. Update `.env.production`:
```bash
CORS_ORIGINS=https://yourdomain.com,https://www.yourdomain.com
FRONTEND_URL=https://yourdomain.com
```

2. Update `docker-compose.prod.yml` (frontend service):
```yaml
ports:
  - "80:80"
  - "443:443"  # For HTTPS
```

3. Add SSL/TLS certificates to nginx.conf (recommended: use Certbot/Let's Encrypt)

## 📊 Health Monitoring

The `/health` endpoint returns:
```json
{
  "status": "healthy",
  "timestamp": "2024-01-01T12:00:00",
  "database": "connected"
}
```

Status codes:
- `healthy` - All systems operational
- `degraded` - Database connection issues

## 🔍 Troubleshooting

### Build Failures
```powershell
# Clean rebuild
.\deploy.ps1 -Clean
.\deploy.ps1 -Build
```

### Database Connection Issues
```powershell
# Check PostgreSQL logs
docker-compose -f docker-compose.prod.yml logs postgres

# Verify environment variables
docker-compose -f docker-compose.prod.yml config
```

### Frontend Not Loading
```powershell
# Check nginx logs
docker-compose -f docker-compose.prod.yml logs frontend

# Verify build completed
docker-compose -f docker-compose.prod.yml exec frontend ls -la /usr/share/nginx/html
```

### API Calls Failing
```powershell
# Test health endpoint
curl http://localhost/api/health

# Check backend logs
docker-compose -f docker-compose.prod.yml logs backend
```

## 📝 Development vs Production

| Feature | Development | Production |
|---------|------------|------------|
| Database | SQLite | PostgreSQL |
| Frontend Server | Vite dev server | Nginx |
| Backend Server | Uvicorn reload | Uvicorn stable |
| CORS | Permissive | Restricted |
| Logging | DEBUG | INFO |
| Static Files | Dev server | Nginx optimized |

## 🔄 Update Workflow

```powershell
# 1. Pull latest code
git pull origin main

# 2. Rebuild containers
.\deploy.ps1 -Build

# 3. Check health
.\deploy.ps1 -Status
```

## 💾 Backup & Restore

### Backup Database
```powershell
docker-compose -f docker-compose.prod.yml exec postgres pg_dump -U raven_user raven_shop_production > backup.sql
```

### Restore Database
```powershell
cat backup.sql | docker-compose -f docker-compose.prod.yml exec -T postgres psql -U raven_user raven_shop_production
```

## 🎯 Next Steps

1. **Local Testing**: Run `.\deploy.ps1 -Build` to test deployment locally
2. **Domain Setup**: Configure your domain DNS to point to your server
3. **SSL Certificate**: Set up HTTPS with Let's Encrypt
4. **Monitoring**: Add application monitoring (e.g., Sentry, Datadog)
5. **CI/CD**: Set up GitHub Actions for automated deployments

## 📚 Additional Resources

- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [Nginx Configuration Guide](https://nginx.org/en/docs/)
- [FastAPI Deployment](https://fastapi.tiangolo.com/deployment/)
- [PostgreSQL Docker Guide](https://hub.docker.com/_/postgres)

---

**Repository**: https://github.com/JayLaRoche/raven_automation.git  
**Latest Commit**: Production deployment with Docker infrastructure  
**Status**: ✅ Ready for deployment
