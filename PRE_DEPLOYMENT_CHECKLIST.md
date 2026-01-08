# 🚀 Pre-Deployment Checklist

Use this checklist before deploying to staging or production.

---

## 📋 Pre-Deployment Verification

### Environment Configuration

- [ ] `.env` file created from `.env.example`
- [ ] All required variables are set (no empty values)
- [ ] No hardcoded secrets in code or configuration files
- [ ] `.env` is in `.gitignore` and won't be committed
- [ ] `APP_ENV` is set correctly (staging or production)

### Database

- [ ] Database server is running and accessible
- [ ] `DATABASE_URL` is correct and tested
  ```bash
  psql "$DATABASE_URL" -c "SELECT 1;" # Test connection
  ```
- [ ] Database user has appropriate permissions
- [ ] Database backups are configured
- [ ] Database is empty or migrations have been run
  ```bash
  cd backend && alembic upgrade head
  ```

### Backend Configuration

- [ ] `DEBUG` is set to `false` in non-development environments
- [ ] `JWT_SECRET_KEY` is set and strong (not default value)
  ```bash
  # Verify it's not the default:
  grep "JWT_SECRET_KEY" .env | grep -v "dev-secret-key"
  ```
- [ ] `CORS_ORIGINS` includes your frontend domain(s)
- [ ] All `CORS_ORIGINS` use HTTPS in production
- [ ] `LOG_LEVEL` is appropriate (INFO for production)
- [ ] Static files directory exists and is readable
  ```bash
  test -d backend/static && echo "✓ Static files directory exists"
  ```

### Frontend Configuration

- [ ] `VITE_API_URL` points to correct backend URL
  ```bash
  grep "VITE_API_URL" .env
  ```
- [ ] API URL uses HTTPS in production
- [ ] Build completes without errors
  ```bash
  cd frontend && npm install && npm run build
  ```
- [ ] Build output is optimized (minified, no sourcemaps)
  ```bash
  ls -lh frontend/dist/ | head -5
  ```

### Security

- [ ] No `.env` files will be deployed (check deployment config)
- [ ] Secrets are managed via environment variables or secrets manager
- [ ] Database password is strong and unique
- [ ] JWT secret is strong and unique
- [ ] HTTPS/TLS certificates are valid and installed
- [ ] SSL/TLS is enforced (redirect HTTP to HTTPS)
- [ ] CORS is restricted to known domains only

### Application Testing

- [ ] Backend starts without errors
  ```bash
  export APP_ENV=production && cd backend && python main.py
  ```
- [ ] Frontend builds successfully
  ```bash
  cd frontend && npm run build && npm run preview
  ```
- [ ] API endpoints are accessible
  ```bash
  curl https://your-api-domain.com/api/frames/series
  ```
- [ ] Database connection works
  ```bash
  curl https://your-api-domain.com/api/frames/series
  # Should return frame data, not error
  ```
- [ ] Frontend can reach backend
  ```
  Open https://your-frontend-domain.com
  Check browser console for no CORS errors
  ```

### Monitoring & Logging

- [ ] Log files directory exists and is writable
  ```bash
  mkdir -p backend/logs && test -w backend/logs
  ```
- [ ] Logging is configured
  ```bash
  grep "LOG_" .env
  ```
- [ ] Monitoring/alerting is set up
  ```
  Check: Sentry, DataDog, New Relic, or similar
  ```
- [ ] Error tracking is enabled
- [ ] Performance monitoring is enabled (optional but recommended)

### Infrastructure

- [ ] Server has sufficient resources
  ```
  CPU: 2+ cores recommended
  RAM: 2GB+ for FastAPI + PostgreSQL
  Storage: 10GB+ for database
  ```
- [ ] Firewall rules allow necessary ports (80, 443, 5432 if applicable)
- [ ] Database is backed up
  ```bash
  # Verify backup job exists
  crontab -l | grep postgres
  ```
- [ ] Load balancer is configured (if applicable)
- [ ] CDN is configured (if applicable)

---

## 🔒 Security Checklist

### Secrets Management

- [ ] All secrets are in environment variables, not code
- [ ] `.env` files are never committed to git
- [ ] Production secrets are stored in secrets manager
  - [ ] AWS Secrets Manager
  - [ ] Azure Key Vault
  - [ ] HashiCorp Vault
  - [ ] Or equivalent

### Network Security

- [ ] HTTPS/TLS is enforced (no HTTP access)
- [ ] CORS is properly configured (specific domains, not `*`)
- [ ] API rate limiting is configured (optional but recommended)
- [ ] Database is not publicly accessible
- [ ] SSH keys are used for server access (no passwords)

### Application Security

- [ ] Debug mode is OFF in production
- [ ] Error messages don't expose sensitive info
- [ ] Database credentials are not in error messages
- [ ] API endpoints validate input properly
- [ ] SQL injection prevention is in place (SQLAlchemy handles this)

---

## 📝 Deployment Process

### Before Deploying

1. **Run this checklist** ← You are here
2. **Test locally**
   ```bash
   export APP_ENV=production
   cd backend && python main:app
   cd frontend && npm run build && npm run preview
   ```
3. **Commit and push** (but NOT `.env`)
   ```bash
   git add .
   git commit -m "Pre-deployment verification complete"
   git push
   ```

### During Deployment

1. **Set environment variables** on deployment server
2. **Pull latest code** from repository
3. **Run migrations** if needed
   ```bash
   alembic upgrade head
   ```
4. **Start services** (backend first, then frontend)
5. **Verify services** are running
   ```bash
   curl https://your-api-domain.com/
   ```

### After Deployment

1. **Test critical flows**
   - [ ] Can load homepage
   - [ ] Can access API
   - [ ] Can generate drawing
   - [ ] Can download PDF
2. **Check logs** for errors
   ```bash
   tail -f backend/logs/app.log
   ```
3. **Monitor metrics** for the first hour
4. **Be ready to rollback** if issues occur

---

## 🆘 Emergency Rollback

If deployment fails:

```bash
# 1. Stop services
systemctl stop backend frontend

# 2. Revert to previous version
git checkout HEAD~1

# 3. Restart services
systemctl start backend frontend

# 4. Monitor logs
tail -f backend/logs/app.log
```

---

## ✅ Sign-Off

| Item | Owner | Date | Status |
|------|-------|------|--------|
| Environment Configuration | [ ] | _____ | [ ] Complete |
| Security Review | [ ] | _____ | [ ] Complete |
| Testing | [ ] | _____ | [ ] Complete |
| Database Backup | [ ] | _____ | [ ] Complete |
| Monitoring Setup | [ ] | _____ | [ ] Complete |

---

## 📞 Support Contacts

In case of production issues:

- **Backend Issues**: Check `backend/logs/app.log`
- **Frontend Issues**: Check browser console (F12)
- **Database Issues**: Check PostgreSQL logs
- **Deployment Issues**: Review deployment platform logs

**Escalation Path:**
1. Check logs first
2. Verify environment variables
3. Test database connectivity
4. Review recent changes
5. Consider rollback if critical

