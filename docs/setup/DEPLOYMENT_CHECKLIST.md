# Deployment Checklist - Frame Series Database Integration

## Pre-Deployment Verification

### Code Review
- [x] Backend endpoint implemented
- [x] Frontend API function implemented  
- [x] Component updated with new logic
- [x] All imports correct
- [x] Error handling in place
- [x] Fallback defaults included
- [x] TypeScript types correct
- [x] No breaking changes

### Local Testing
- [ ] Start backend: `python main.py`
- [ ] Start frontend: `npm run dev`
- [ ] Open http://localhost:3001
- [ ] Navigate to Sales Presentation
- [ ] Frame Series dropdown shows "Loading..."
- [ ] Dropdown populates with series from database
- [ ] Selecting a series shows preview image (if available)
- [ ] View selector (HEAD/SILL/JAMB) still works
- [ ] Quick presets still work
- [ ] Form submission still works

### Browser Console
- [ ] No JavaScript errors
- [ ] No network errors
- [ ] API call completes successfully
- [ ] Response data is correct

### Network Tab (DevTools)
- [ ] API endpoint responds: `/api/frames/series-with-images`
- [ ] Status code: 200 OK
- [ ] Response time: < 200ms
- [ ] Payload size reasonable

## Production Deployment

### Step 1: Code Deployment
- [ ] Merge PR to main branch
- [ ] Pull latest code on production server
- [ ] Verify file changes:
  - [ ] `backend/routers/frames.py` has new endpoint
  - [ ] `frontend/src/services/api.js` has new function
  - [ ] `frontend/src/components/sales/SmartParameterPanel.tsx` updated

### Step 2: Dependencies
- [ ] Frontend dependencies: `npm install` (already installed)
- [ ] Backend dependencies: `pip install -r requirements.txt` (already installed)
- [ ] Python packages check:
  - [ ] fastapi
  - [ ] sqlalchemy
  - [ ] psycopg2 (PostgreSQL)

### Step 3: Database Verification
- [ ] PostgreSQL is running
- [ ] Database URL in `.env` is correct
- [ ] `frame_cross_sections` table exists
- [ ] Table has data: `SELECT COUNT(DISTINCT series) FROM frame_cross_sections;`
- [ ] Results > 0

### Step 4: Static Files
- [ ] Directory exists: `backend/static/frames/`
- [ ] Frame images placed in directory:
  - [ ] `series-86-thumbnail.png` or `series-86-head.png`
  - [ ] `series-135-thumbnail.png` or `series-135-head.png`
  - [ ] Other series images as available
- [ ] File permissions correct (readable)
- [ ] Total image file size reasonable

### Step 5: Environment Configuration
- [ ] `.env` file correct:
  - [ ] `DATABASE_URL` points to production database
  - [ ] `VITE_API_URL` = `http://backend-domain:8000` (if needed)
- [ ] CORS configuration correct in `main.py`
  - [ ] Allow origins include frontend domain
- [ ] Static files mounting enabled in `main.py`

### Step 6: Service Start
- [ ] Backend service starts: `python main.py`
  - [ ] Check logs for: "✅ Database tables created/verified"
  - [ ] Check logs for: "✅ Static files mounted at /static"
- [ ] Frontend service starts: `npm run dev` or production build
  - [ ] Check for build errors
  - [ ] Verify bundle size acceptable

### Step 7: API Verification
Test endpoints directly:

```bash
# Test 1: Database query endpoint
curl http://localhost:8000/api/frames/series | jq '.'

# Test 2: New series-with-images endpoint
curl http://localhost:8000/api/frames/series-with-images | jq '.'

# Test 3: Static file serving
curl http://localhost:8000/static/frames/series-86-thumbnail.png \
  -H "Accept: image/png" -w "\nStatus: %{http_code}\n"

# Test 4: Health check
curl http://localhost:8000/health | jq '.'
```

### Step 8: Frontend Testing
- [ ] Open application in browser
- [ ] Navigate to Sales Presentation page
- [ ] Frame Series dropdown appears
- [ ] Dropdown shows "Loading frame series..." initially
- [ ] After ~1 second, dropdown populates
- [ ] Options show: "Series 86", "Series 135", etc.
- [ ] Selecting a series works
- [ ] Image appears below dropdown (or "No preview..." message)
- [ ] View selector buttons still work
- [ ] Drawing generation still works
- [ ] No console errors

### Step 9: Cross-Browser Testing
- [ ] Chrome - Works
- [ ] Firefox - Works
- [ ] Safari - Works
- [ ] Edge - Works
- [ ] Mobile browser - Works

### Step 10: Performance Check
- [ ] Page load time: < 3 seconds
- [ ] API response time: < 500ms
- [ ] No memory leaks
- [ ] Image load time: < 1 second per image

## Rollback Plan

If issues occur, execute in order:

### Immediate Rollback (< 5 minutes)
```bash
# 1. Revert code to previous version
git revert <commit-hash>
git push

# 2. Restart services
supervisorctl restart all
# OR
systemctl restart raven-backend raven-frontend
```

### If Database Issues
```bash
# 1. Check database connection
psql -U raven_user -d raven_drawings -c "SELECT COUNT(*) FROM frame_cross_sections;"

# 2. Check table structure
psql -U raven_user -d raven_drawings -c "\d frame_cross_sections;"

# 3. Restore from backup if needed
psql -U raven_user -d raven_drawings < database_backup.sql
```

### If Static Files Missing
```bash
# Verify directory
ls -la backend/static/frames/

# Check permissions
chmod 755 backend/static/frames/
chmod 644 backend/static/frames/*.png

# Restart backend to remount
supervisorctl restart raven-backend
```

## Post-Deployment Verification

### Day 1 (24 hours)
- [ ] No error reports from users
- [ ] API response times normal
- [ ] Database queries performant
- [ ] Image loading works
- [ ] No database connection errors in logs

### Week 1
- [ ] Stable operation
- [ ] No performance degradation
- [ ] User feedback positive
- [ ] Error logs clean

## Success Metrics

✅ **Deployment Successful if:**
1. All API endpoints return 200 OK
2. Frame series appear in dropdown
3. Images load correctly (if available)
4. No JavaScript console errors
5. No backend error logs
6. Response times < 500ms
7. Database queries working
8. Static file serving working
9. CORS not blocking requests
10. All existing functionality still works

## Monitoring After Deployment

### Log Files to Monitor
```
backend/
├── logs/
│   ├── api.log (API request/response)
│   ├── database.log (SQL queries)
│   ├── error.log (Errors)
│   └── access.log (HTTP requests)

frontend/
└── logs/
    ├── build.log
    └── error.log (Browser console errors)
```

### Alerts to Setup
- [ ] High API response time (> 1 second)
- [ ] Database connection errors
- [ ] Static file 404 errors
- [ ] CORS errors
- [ ] Missing image files

### Metrics to Track
- [ ] API endpoint hit rate
- [ ] Image load success rate
- [ ] Average response time
- [ ] Error rate
- [ ] User complaints

## Verification Commands

```bash
# Check backend is running
curl -s http://localhost:8000/health | jq '.'

# Check API endpoint
curl -s http://localhost:8000/api/frames/series-with-images | jq '.series | length'

# Check image serving
curl -I http://localhost:8000/static/frames/series-86-thumbnail.png | grep -i content-type

# Check database connection
psql -c "SELECT COUNT(*) FROM frame_cross_sections;"

# Check logs for errors
tail -f backend/logs/error.log

# Monitor API performance
curl -w "@curl-format.txt" -o /dev/null -s http://localhost:8000/api/frames/series-with-images
```

## Communication

### Notify Team
- [ ] Deployment completed to team Slack
- [ ] Link to documentation provided
- [ ] Known limitations mentioned
- [ ] Rollback procedure shared

### User Documentation
- [ ] Updated README with new feature
- [ ] Created user guide for frame images
- [ ] Added screenshots to documentation
- [ ] FAQ updated with new feature info

## Final Checklist

- [ ] Code changes reviewed
- [ ] Local tests passed
- [ ] Production database verified
- [ ] Static files in place
- [ ] Services started successfully
- [ ] API endpoints responding
- [ ] Frontend loading correctly
- [ ] Feature working as expected
- [ ] No errors in logs
- [ ] Team notified
- [ ] Monitoring configured

---

## Sign-Off

| Role | Name | Date | Signature |
|------|------|------|-----------|
| Developer | | | |
| QA/Tester | | | |
| DevOps | | | |
| Project Manager | | | |

---

**Status:** Ready for Deployment ✅
**Last Reviewed:** December 27, 2025
**Version:** 1.0

**Notes:**
- Ensure database backup exists before deployment
- Have rollback plan ready before starting
- Deploy during low-traffic hours if possible
- Monitor closely for first 24 hours
