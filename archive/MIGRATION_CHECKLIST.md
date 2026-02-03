# Project Cleanup & Migration Checklist

**Date Started**: _________________  
**Completed By**: _________________  
**Status**: 🔄 In Progress

---

## Pre-Cleanup Tasks

### 1. Backup & Safety
- [ ] Create Git branch for cleanup work
  ```bash
  git checkout -b cleanup/organize-documentation
  ```
- [ ] Verify all changes are committed
  ```bash
  git status
  ```
- [ ] Create backup of current state
  ```bash
  git tag backup-before-cleanup-$(date +%Y%m%d)
  ```
- [ ] Document current file count
  ```bash
  Get-ChildItem *.md | Measure-Object | Select-Object Count
  ```

### 2. Environment Check
- [ ] All servers stopped (backend, frontend, database)
- [ ] No active development work in progress
- [ ] Team notified of upcoming changes (if applicable)

---

## Cleanup Execution

### Phase 1: Fix Missing CSS Module ✅
- [x] Create `SalesPresentation.module.css`
- [ ] Verify TypeScript error resolved
- [ ] Test SalesPresentation component renders correctly

### Phase 2: Run Cleanup Script
- [ ] Review `cleanup_project.ps1` script
- [ ] Execute cleanup script
  ```powershell
  .\cleanup_project.ps1
  ```
- [ ] Review console output for errors
- [ ] Verify `docs/` folder structure created
- [ ] Verify `scripts/` folder populated

### Phase 3: Review Archived Files
- [ ] Navigate to `docs/archived/`
- [ ] Scan archived files for any critical content
- [ ] Check if any archived files needed in new locations
- [ ] Document any files to rescue before deletion

**Files to Rescue (if any)**:
- _______________________________________
- _______________________________________

### Phase 4: Verify New Structure
- [ ] Check `docs/architecture/` - Contains 3 key files
- [ ] Check `docs/features/` - Contains feature docs
- [ ] Check `docs/setup/` - Contains setup guides
- [ ] Check `docs/api/` - Contains API documentation
- [ ] Check `docs/database/` - Contains database docs
- [ ] Check `scripts/` - Contains utility scripts
- [ ] Verify root `INDEX.md` still accessible

### Phase 5: Update References
- [ ] Review `INDEX.md` for broken links
- [ ] Update any hard-coded documentation paths in code
- [ ] Check `README.md` references (if exists)
- [ ] Update any bookmark/documentation URLs

---

## Testing Phase

### Functional Testing
- [ ] Start backend server
  ```bash
  cd backend && uvicorn main:app --reload
  ```
- [ ] Start frontend server
  ```bash
  cd frontend && npm run dev
  ```
- [ ] Verify SalesPresentation page loads
- [ ] Test drawing generation functionality
- [ ] Verify no console errors related to missing files

### Documentation Verification
- [ ] Open main `INDEX.md` - links work
- [ ] Check `docs/setup/GETTING_STARTED.md` - steps accurate
- [ ] Review `docs/api/API_DOCUMENTATION.md` - endpoints correct
- [ ] Verify `GIT_COMMIT_GUIDE.md` location updated

### Git Verification
- [ ] Run `git status` - see organized changes
- [ ] Verify no critical files accidentally deleted
- [ ] Check `.gitignore` updated (Phase 6)

---

## Phase 6: Update .gitignore

- [ ] Add documentation clutter prevention rules
- [ ] Add script temp file exclusions
- [ ] Test gitignore rules work
- [ ] Commit `.gitignore` updates

---

## Finalization

### Cleanup Archived Files
- [ ] Review cleanup report: `docs/CLEANUP_REPORT.md`
- [ ] Final confirmation - nothing needed from archived/
- [ ] Delete archived folder
  ```powershell
  Remove-Item 'docs/archived' -Recurse -Force
  ```

### Git Commit
- [ ] Stage all changes
  ```bash
  git add .
  git status  # Review staged changes
  ```
- [ ] Commit with descriptive message
  ```bash
  git commit -m "docs: organize project documentation and remove redundant files

  - Created organized docs/ structure (architecture, features, setup, api, database)
  - Moved utility scripts to scripts/ folder
  - Removed ~40 redundant documentation files
  - Fixed missing SalesPresentation.module.css
  - Updated .gitignore to prevent future clutter
  
  Closes #[issue-number]"
  ```
- [ ] Push to remote
  ```bash
  git push origin cleanup/organize-documentation
  ```

### Create Pull Request (if using PRs)
- [ ] Create PR with cleanup summary
- [ ] Link to `CLEANUP_REPORT.md`
- [ ] Request review from team
- [ ] Merge after approval

### Post-Merge Tasks
- [ ] Update local main branch
  ```bash
  git checkout main
  git pull origin main
  ```
- [ ] Delete cleanup branch
  ```bash
  git branch -d cleanup/organize-documentation
  ```
- [ ] Notify team of new documentation structure

---

## Rollback Plan (If Needed)

If issues arise, rollback using:

```bash
# Restore from backup tag
git checkout backup-before-cleanup-[date]

# Or reset to previous commit
git log  # Find commit hash before cleanup
git reset --hard [commit-hash]
```

---

## Documentation Updates

### Files to Update After Cleanup
- [ ] `README.md` - Update "Documentation" section
- [ ] `CONTRIBUTING.md` - Update file structure references (if exists)
- [ ] Team Wiki/Confluence - Update links
- [ ] Onboarding docs - Update file paths

### Communication
- [ ] Announce new structure to team (Slack/Email)
- [ ] Update team documentation links
- [ ] Add note in next standup/meeting

---

## Success Criteria

✅ **Cleanup is successful when**:
- All TypeScript/build errors resolved
- Application runs without errors
- Documentation is organized and accessible
- Git history is clean
- Team can find documentation easily
- ~40+ redundant files removed
- .gitignore prevents future clutter

---

## Notes & Issues

**Issues Encountered**:
1. _______________________________________
2. _______________________________________

**Lessons Learned**:
1. _______________________________________
2. _______________________________________

**Future Improvements**:
1. _______________________________________
2. _______________________________________

---

## Completion Sign-Off

- [ ] All checklist items completed
- [ ] Application tested and working
- [ ] Team notified
- [ ] Documentation updated

**Completed Date**: _________________  
**Sign-Off**: _________________

✅ **Project cleanup complete!**
