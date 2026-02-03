# 📋 Git Commit Guide - What to Push to GitHub

## ✅ Current .gitignore Status

Your `.gitignore` is **comprehensive and secure**. It properly excludes:

### Secrets & Environment
- ✅ `.env` (and all variants: .env.local, .env.*.local)
- ✅ `credentials/` folder
- ✅ `*.key` and `*.pem` files
- ✅ `secrets/` folder

### Dependencies
- ✅ `node_modules/` (Node)
- ✅ `venv/`, `ENV/`, `env/`, `.venv` (Python)
- ✅ `dist/` (Build output)
- ✅ `.pytest_cache/` (Test cache)

### System Files
- ✅ `.DS_Store` (macOS)
- ✅ `Thumbs.db` (Windows)
- ✅ `.history/` (VSCode history)

### Temporary Files
- ✅ `*.log` (All logs)
- ✅ `*.db`, `*.sqlite` (Local databases)
- ✅ `.idea/`, `.vscode/` (IDE config)

---

## 📁 Files to Commit to GitHub

### ✅ Root Level Files (COMMIT THESE)

```
✅ .env.example              ← CRITICAL: Template for others
✅ .gitignore                ← Already configured
✅ README.md                 ← Project documentation
✅ docker-compose.yml        ← Database setup
✅ package.json              ← Frontend dependencies
✅ requirements.txt          ← Backend dependencies
✅ ENVIRONMENT_SETUP.md      ← Deployment guide
✅ ENVIRONMENT_*.md          ← All env documentation
✅ PRE_DEPLOYMENT_CHECKLIST.md
✅ start_dev.sh              ← Developer startup script
```

### ✅ Backend Files (COMMIT THESE)

```
backend/
├── ✅ main.py                ← FastAPI entry point
├── ✅ requirements.txt        ← Python dependencies
├── ✅ app/
│   ├── ✅ __init__.py
│   ├── ✅ config.py           ← Configuration management
│   ├── ✅ database.py         ← Database setup
│   └── ✅ models/             ← SQLAlchemy models
├── ✅ routers/                ← API endpoints
│   ├── ✅ frames.py
│   ├── ✅ drawings.py
│   └── ✅ projects.py
├── ✅ services/               ← Business logic
│   ├── ✅ frame_sync_scheduler.py
│   ├── ✅ google_sheets_services.py
│   └── ✅ reference_shop_drawing_generator.py
├── ✅ alembic/                ← Database migrations
│   ├── ✅ env.py
│   ├── ✅ script.py.mako
│   └── ✅ versions/           ← Migration files
├── ✅ alembic.ini             ← Alembic config
├── ✅ init_db.py              ← Database initialization
└── ❌ static/                 ← See note below
    └── ❌ frames/             ← Large image files (DON'T COMMIT)
```

**Note on `backend/static/`:**
- ❌ Do NOT commit large frame image files
- ✅ DO commit `.gitkeep` file to keep folder structure
- ✅ DO create `README.md` in `static/frames/` explaining the folder

### ✅ Frontend Files (COMMIT THESE)

```
frontend/
├── ✅ package.json            ← Npm dependencies
├── ✅ package-lock.json       ← Locked versions
├── ✅ vite.config.js          ← Build configuration
├── ✅ index.html              ← HTML template
├── ✅ .env.example            ← Environment template
├── ✅ src/
│   ├── ✅ App.jsx
│   ├── ✅ main.jsx
│   ├── ✅ index.css
│   ├── ✅ components/         ← All components
│   ├── ✅ pages/              ← All pages
│   ├── ✅ services/           ← API client
│   ├── ✅ store/              ← State management (Zustand)
│   └── ✅ hooks/              ← Custom hooks
├── ✅ public/                 ← Static assets
│   ├── ✅ favicon.ico
│   └── ✅ static/frames/      ← Frame reference images (see note)
├── ✅ tailwind.config.js      ← Tailwind configuration
└── ❌ dist/                   ← Build output (DON'T COMMIT)
    ❌ node_modules/           ← Dependencies (DON'T COMMIT)
```

### ✅ Configuration & Documentation (COMMIT THESE)

```
✅ .github/                   ← GitHub config
│   └── ✅ copilot-instructions.md
├── ✅ ENVIRONMENT_SETUP.md
├── ✅ ENV_QUICK_REFERENCE.md
├── ✅ PRE_DEPLOYMENT_CHECKLIST.md
├── ✅ ENVIRONMENT_CONFIGURATION_SUMMARY.md
├── ✅ ENVIRONMENT_DOCUMENTATION_INDEX.md
├── ✅ README.md
├── ✅ API_DOCUMENTATION.md
├── ✅ docker-compose.yml
├── ✅ Dockerfile (if you have one)
└── ✅ nginx/                 ← Reverse proxy config (if applicable)
```

---

## ❌ Files/Folders to EXCLUDE (Already in .gitignore)

```
❌ .env                       ← Secrets! NEVER commit
❌ .env.*                     ← Local overrides with secrets
❌ credentials/               ← API keys and service accounts
❌ node_modules/              ← Install via npm install
❌ venv/                      ← Install via python -m venv venv
❌ dist/                      ← Build output (regenerate on deploy)
❌ backend/static/frames/     ← Large image files (see note)
❌ *.log                      ← Log files
❌ *.db, *.sqlite             ← Local databases
❌ .DS_Store, Thumbs.db       ← System files
❌ __pycache__/               ← Python cache
❌ .pytest_cache/             ← Test cache
```

---

## 🎯 Special Cases

### Large Assets (Frame Images)

**Problem:** Frame images are large (shouldn't commit)
**Solution:** 

```bash
# 1. Create placeholder structure
mkdir -p backend/static/frames
mkdir -p frontend/public/static/frames

# 2. Add README explaining where to get images
cat > backend/static/frames/README.md << 'EOF'
# Frame Images

Place frame reference images here with naming convention:
- series_86_HEAD.png
- series_86_SILL.png
- series_86_JAMB.png
- series_135_HEAD.png
etc.

Images should be downloaded from the frame library or
generated using the frame sync process.

See: ../../init_db.py
EOF

# 3. Add .gitkeep to preserve folder
touch backend/static/frames/.gitkeep
```

### Credentials Files

**Do this:**
```bash
# 1. Create credentials template
mkdir -p backend/credentials
cat > backend/credentials/README.md << 'EOF'
# Service Account Credentials

Place your Google Sheets service account JSON here:
- google-sheets-credentials.json

Download from: https://console.cloud.google.com/iam-admin/serviceaccounts

Never commit this file - it's in .gitignore
EOF

# 2. Add .gitkeep
touch backend/credentials/.gitkeep
```

---

## 📝 Minimal Viable Repo for Another Developer

A new developer cloning your repo needs these to succeed:

### Minimum Files Required

```
raven-shop-automation/
├── .env.example              ← Copy to .env and configure
├── .gitignore
├── README.md                 ← Startup instructions
├── requirements.txt          ← pip install -r requirements.txt
├── package.json              ← npm install
├── docker-compose.yml        ← docker-compose up
├── backend/
│   ├── main.py
│   ├── app/
│   ├── routers/
│   ├── services/
│   └── alembic/
├── frontend/
│   ├── package.json
│   ├── vite.config.js
│   ├── index.html
│   └── src/
├── ENVIRONMENT_SETUP.md      ← How to set up
└── START_SERVERS.bat         ← Quick start (Windows)
    or start_dev.sh           ← Quick start (Linux/Mac)
```

### Setup Instructions for New Developer

After cloning, they should:

```bash
# 1. Copy environment template
cp .env.example .env

# 2. Edit .env with their config
nano .env  # Set DATABASE_URL, API endpoints, etc.

# 3. Backend setup
cd backend
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
alembic upgrade head

# 4. Frontend setup
cd ../frontend
npm install
npm run dev

# 5. Start backend (separate terminal)
cd backend
uvicorn main:app --reload
```

---

## ✅ Git Workflow - What to Commit

### Good Commits (Include These)

```bash
git add .
git add backend/app/config.py          ✅ Configuration code
git add backend/routers/frames.py       ✅ Business logic
git add frontend/src/components/        ✅ React components
git add ENVIRONMENT_SETUP.md            ✅ Documentation
git add .env.example                   ✅ Template

git commit -m "Add feature: X"
git push origin main
```

### Bad Commits (Never Do This)

```bash
git add .env                           ❌ NEVER - secrets!
git add backend/credentials/*.json     ❌ NEVER - API keys!
git add node_modules/                 ❌ NEVER - too large!
git add venv/                          ❌ NEVER - too large!
git add *.log                          ❌ NEVER - noise!

# If you accidentally did this:
git rm --cached .env
git commit --amend
# Regenerate your .env secrets since they were exposed!
```

---

## 🚀 Quick Start for New Developer

Create a `README.md` with this:

```markdown
# Raven Shop Automation

## Quick Start

### Prerequisites
- Python 3.9+
- Node.js 18+
- PostgreSQL (or Docker)

### Setup

1. Clone and configure:
   ```bash
   git clone https://github.com/yourusername/raven-automation.git
   cd raven-automation
   cp .env.example .env
   nano .env  # Add your configuration
   ```

2. Backend:
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   alembic upgrade head
   uvicorn main:app --reload
   ```

3. Frontend (new terminal):
   ```bash
   cd frontend
   npm install
   npm run dev
   ```

4. Open http://localhost:3000

## Documentation
- [Environment Setup](ENVIRONMENT_SETUP.md)
- [API Documentation](API_DOCUMENTATION.md)
- [Deployment Guide](PRE_DEPLOYMENT_CHECKLIST.md)
```

---

## ✨ Final Checklist Before First Commit

Before pushing to GitHub:

- [ ] `.env` is NOT staged
  ```bash
  git status  # Should NOT show .env
  ```

- [ ] `.gitignore` is correct
  ```bash
  git check-ignore -v .env  # Should show it's ignored
  ```

- [ ] Sensitive files are excluded
  ```bash
  git check-ignore -v backend/credentials/*.json
  git check-ignore -v *.log
  git check-ignore -v node_modules/
  ```

- [ ] All necessary files are included
  ```bash
  git add .
  git status  # Verify only good files are staged
  ```

- [ ] Push clean commit
  ```bash
  git commit -m "Initial commit: Raven Shop Automation"
  git push -u origin main
  ```

---

## 📊 Summary

| Category | Commit? | Why |
|----------|---------|-----|
| Source Code | ✅ YES | Other devs need it |
| Dependencies (package.json, requirements.txt) | ✅ YES | Reproducible builds |
| Configuration Templates (.env.example) | ✅ YES | Setup instructions |
| Documentation | ✅ YES | Setup/deployment help |
| .gitignore | ✅ YES | Protects secrets |
| node_modules, venv | ❌ NO | Too large, regenerate with install |
| .env, credentials | ❌ NO | Secrets! Never commit |
| Build output (dist/) | ❌ NO | Regenerate on build |
| Log files | ❌ NO | Runtime artifacts |
| System files (.DS_Store) | ❌ NO | Machine-specific |

