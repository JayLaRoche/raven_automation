# 🚀 Render.com Deployment Guide

Complete step-by-step guide to deploy Raven Shop Automation to Render.com and get a **public URL**.

---

## 📋 Prerequisites

- ✅ GitHub repository: https://github.com/JayLaRoche/raven_automation.git
- ✅ Render.com account (free to create)
- ✅ All code committed and pushed to main branch

---

## 🎯 Deployment Steps

### **Step 1: Create Render Account**

1. Go to https://render.com
2. Click **"Get Started"**
3. Sign up with your **GitHub account** (recommended for easy integration)
4. Authorize Render to access your GitHub repositories

---

### **Step 2: Create New Web Service (Backend)**

1. **In Render Dashboard:**
   - Click **"New +"** → **"Web Service"**

2. **Connect Repository:**
   - Select **"JayLaRoche/raven_automation"**
   - Click **"Connect"**

3. **Configure Backend Service:**
   ```
   Name:               raven-backend
   Region:             Ohio (US East)
   Branch:             main
   Root Directory:     backend
   Runtime:            Docker
   Dockerfile Path:    backend/Dockerfile.prod
   Instance Type:      Starter ($7/month) or Free
   ```

4. **Add Environment Variables:**
   Click **"Advanced"** → **"Add Environment Variable"**
   
   Add these variables:
   ```
   DATABASE_URL         = [Will set after PostgreSQL creation]
   CORS_ORIGINS         = https://raven-shop.onrender.com
   PYTHON_ENV           = production
   DEBUG                = false
   LOG_LEVEL            = INFO
   SECRET_KEY           = [Click "Generate" for random value]
   JWT_SECRET           = [Click "Generate" for random value]
   ```

5. **Click "Create Web Service"**
   - ⏳ Wait 5-10 minutes for first build
   - ✅ You'll get URL like: `https://raven-backend.onrender.com`

---

### **Step 3: Create PostgreSQL Database**

1. **In Render Dashboard:**
   - Click **"New +"** → **"PostgreSQL"**

2. **Configure Database:**
   ```
   Name:               raven-db
   Database:           raven_shop_production
   User:               raven_user
   Region:             Ohio (US East) - SAME as backend
   PostgreSQL Version: 15
   Plan:               Starter ($7/month) or Free (90 days)
   ```

3. **Click "Create Database"**
   - ⏳ Wait 2-3 minutes for provisioning
   - ✅ Database URL will be auto-generated

4. **Copy Internal Database URL:**
   - Click on **"raven-db"** in dashboard
   - Copy the **"Internal Database URL"** (starts with `postgresql://`)
   - Example: `postgresql://raven_user:abc123@dpg-xyz/raven_shop_production`

---

### **Step 4: Update Backend Environment**

1. **Go back to "raven-backend" service**
2. Click **"Environment"** tab
3. **Update DATABASE_URL:**
   - Find `DATABASE_URL` variable
   - Paste the Internal Database URL from Step 3
   - Click **"Save Changes"**

4. **Render will auto-redeploy** backend with database connection

---

### **Step 5: Create Static Site (Frontend)**

1. **In Render Dashboard:**
   - Click **"New +"** → **"Static Site"**

2. **Connect Repository:**
   - Select **"JayLaRoche/raven_automation"**
   - Click **"Connect"**

3. **Configure Frontend Service:**
   ```
   Name:               raven-shop
   Region:             Ohio (US East)
   Branch:             main
   Root Directory:     frontend
   Build Command:      npm ci && npm run build
   Publish Directory:  dist
   ```

4. **Add Environment Variables:**
   Click **"Advanced"** → **"Add Environment Variable"**
   ```
   VITE_API_URL = https://raven-backend.onrender.com
   ```

5. **Add Rewrite Rules:**
   Click **"Redirects/Rewrites"** → **"Add Rule"**
   
   **Rule 1 - API Proxy:**
   ```
   Source:      /api/*
   Destination: https://raven-backend.onrender.com/api/:splat
   Action:      Rewrite
   ```
   
   **Rule 2 - SPA Routing:**
   ```
   Source:      /*
   Destination: /index.html
   Action:      Rewrite
   ```

6. **Click "Create Static Site"**
   - ⏳ Wait 3-5 minutes for build
   - ✅ You'll get URL like: `https://raven-shop.onrender.com`

---

### **Step 6: Update Backend CORS**

1. **Update backend to allow frontend URL:**
   
   In Render Dashboard → **raven-backend** → **Environment**:
   
   Update `CORS_ORIGINS`:
   ```
   CORS_ORIGINS = https://raven-shop.onrender.com
   ```

2. **Save Changes** - Backend will redeploy

---

### **Step 7: Test Deployment**

1. **Open your frontend URL:**
   ```
   https://raven-shop.onrender.com
   ```

2. **Check health endpoint:**
   ```
   https://raven-backend.onrender.com/health
   ```
   
   Should return:
   ```json
   {
     "status": "healthy",
     "timestamp": "2026-02-02T...",
     "database": "connected"
   }
   ```

3. **Test API docs:**
   ```
   https://raven-backend.onrender.com/docs
   ```

4. **Try creating a project:**
   - Go to your frontend URL
   - Navigate to Projects dashboard
   - Create a test project
   - Verify it saves to database

---

## 🎉 Your Public URLs

After successful deployment, you'll have:

```
Frontend (Main App):     https://raven-shop.onrender.com
Backend API:             https://raven-backend.onrender.com
API Documentation:       https://raven-backend.onrender.com/docs
Health Check:            https://raven-backend.onrender.com/health
Database:                Internal only (not publicly accessible)
```

---

## 🔄 Auto-Deployment

**Automatic deployments are now enabled!**

Every time you push to GitHub:
```bash
git add .
git commit -m "Update feature"
git push origin main
```

Render will automatically:
1. Detect the push via webhook
2. Rebuild backend and frontend
3. Deploy new versions (takes 3-5 minutes)
4. URL stays the same

---

## 💰 Pricing Summary

### **Free Tier (Good for Testing):**
- ✅ Frontend: Free forever
- ✅ Backend: Free (sleeps after 15min inactivity, wakes on request)
- ✅ Database: Free for 90 days, then $7/month

**Total: $0/month for 90 days, then $7/month**

### **Starter Tier (Recommended for Production):**
- ✅ Frontend: Free forever
- ✅ Backend: $7/month (always-on, no sleep)
- ✅ Database: $7/month (persistent data, backups)

**Total: $14/month**

### **Sleep Behavior (Free Tier):**
- Backend sleeps after 15 minutes of inactivity
- First request after sleep takes 30-60 seconds to wake up
- Frontend always loads instantly (static files)
- Database doesn't sleep (data always available)

---

## 🔧 Troubleshooting

### **Issue: Frontend shows blank page**

**Solution:**
1. Check browser console for errors (F12)
2. Verify `VITE_API_URL` is set correctly in frontend environment
3. Check rewrite rules are configured

### **Issue: API calls return CORS errors**

**Solution:**
1. Verify backend `CORS_ORIGINS` includes exact frontend URL (with https://)
2. No trailing slashes in URLs
3. Redeploy backend after CORS changes

### **Issue: Database connection failed**

**Solution:**
1. Verify `DATABASE_URL` uses **Internal Database URL** (not External)
2. Check database and backend are in same region (Ohio)
3. View backend logs: Dashboard → raven-backend → Logs

### **Issue: Build fails**

**Solution:**
1. Check build logs in Render dashboard
2. Verify `package.json` and `requirements.txt` are up to date
3. Ensure Dockerfile paths are correct

### **Issue: 404 on page refresh**

**Solution:**
1. Add SPA rewrite rule: `/* → /index.html`
2. This tells Render to serve index.html for all routes (React Router handling)

---

## 📊 Monitoring Your Deployment

### **View Logs:**
1. Dashboard → Select service (raven-backend or raven-shop)
2. Click **"Logs"** tab
3. Real-time log streaming

### **View Metrics:**
1. Dashboard → Select service
2. Click **"Metrics"** tab
3. See CPU, memory, request rate

### **Health Checks:**
Render automatically monitors:
- Backend: `/health` endpoint every 30 seconds
- If unhealthy for 3 checks, service auto-restarts

---

## 🔐 Security Best Practices

### **Secrets Management:**
- ✅ Never commit `.env` files to Git
- ✅ Use Render's environment variables (encrypted at rest)
- ✅ Use "Generate" button for SECRET_KEY and JWT_SECRET
- ✅ Rotate secrets every 90 days

### **Database Security:**
- ✅ Use Internal Database URL (not External)
- ✅ Database is not publicly accessible
- ✅ Automatic daily backups (Starter plan)
- ✅ Point-in-time recovery available

### **HTTPS:**
- ✅ Automatically enabled (free SSL certificate)
- ✅ Auto-renews before expiration
- ✅ Redirects HTTP → HTTPS

---

## 📱 Custom Domain (Optional)

Want `yourdomain.com` instead of `onrender.com`?

1. **Buy domain** (Namecheap, Google Domains, etc.)

2. **In Render Dashboard:**
   - Go to **raven-shop** (frontend)
   - Click **"Settings"** → **"Custom Domain"**
   - Enter: `yourdomain.com`
   - Follow DNS instructions

3. **Update DNS records:**
   ```
   Type: CNAME
   Name: @
   Value: raven-shop.onrender.com
   ```

4. **Update CORS:**
   ```
   CORS_ORIGINS = https://yourdomain.com
   ```

5. **Wait 10-60 minutes** for DNS propagation

---

## 🎯 Next Steps After Deployment

1. **Test all features:**
   - Create projects
   - Add units
   - Generate drawings
   - Save to database

2. **Monitor performance:**
   - Check logs for errors
   - Review metrics for slow endpoints

3. **Set up monitoring alerts:**
   - Render → Settings → Notifications
   - Get email alerts for downtime

4. **Share your URL:**
   - Give clients access: `https://raven-shop.onrender.com`
   - Add to business cards/emails

---

## 📞 Support

- **Render Documentation:** https://render.com/docs
- **Render Community:** https://community.render.com
- **Your Repository:** https://github.com/JayLaRoche/raven_automation

---

## ✅ Deployment Checklist

Before going live:

- [ ] Backend deployed and healthy
- [ ] Database created and connected
- [ ] Frontend deployed and loads
- [ ] CORS configured correctly
- [ ] API calls work from frontend
- [ ] Test project creation
- [ ] Test drawing generation
- [ ] Health endpoint returns "connected"
- [ ] Environment variables set
- [ ] Auto-deploy enabled (push to main triggers rebuild)

---

**🎉 Congratulations! Your app is now live on the internet!**

Share this URL with your team: `https://raven-shop.onrender.com`
