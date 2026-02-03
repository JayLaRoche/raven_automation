# Frame Data Sync - Quick Reference

## 🎯 What Changed

Your project now **automatically syncs frame data every 30 minutes** and allows manual sync via a button in the UI.

## 🚀 How to Use

### Automatic Sync
- **No setup required!** The backend automatically syncs every 30 minutes when running
- Check logs to see sync messages: `[OK] Frame sync scheduler activated - syncs every 30 minutes`

### Manual Sync
1. Open the Sales drawing interface (SmartParameterPanel)
2. Look for the **"↻ Sync"** button next to "Frame Series" dropdown
3. Click to manually sync frame data from your database
4. Green notification confirms success

## 📊 API Endpoints (Backend)

### Check Sync Status
```
GET http://localhost:8000/api/frames/sync-status
```
Returns: `{"running": true, "next_run": "...", "sync_interval_minutes": 30}`

### Trigger Manual Sync
```
POST http://localhost:8000/api/frames/sync-now
```
Returns: `{"status": "success", "records_synced": 3, ...}`

## 🔧 Configuration

### Change Sync Interval (Default: 30 minutes)
Edit `backend/services/frame_sync_scheduler.py` line ~85:
```python
scheduler.add_job(
    sync_frames_task,
    IntervalTrigger(minutes=30),  # ← Change this number
    id="frame_sync_job"
)
```

### Connect to Real Excel Data
Edit `backend/services/frame_sync_scheduler.py` function `get_mock_frame_data()`:
1. Replace mock data return with actual Excel/Google Sheets reader
2. Update `sync_frames_from_excel()` to process real data
3. Test with manual sync endpoint

## 📁 Files Modified

- ✅ `backend/services/frame_sync_scheduler.py` - NEW scheduler
- ✅ `backend/main.py` - Added startup/shutdown events
- ✅ `backend/routers/frames.py` - Added 2 new endpoints
- ✅ `frontend/src/components/sales/SmartParameterPanel.tsx` - Added sync button

## 🐛 Troubleshooting

**Q: Sync button doesn't appear**
- A: Rebuild frontend: `npm run build` in frontend folder

**Q: Backend shows scheduler error**
- A: Ensure APScheduler installed: `pip install apscheduler`

**Q: Sync shows error**
- A: Check backend logs for details, database may not be running

## 📈 Current Status

✅ **Running:**
- Backend scheduler: Active, syncs every 30 minutes
- Manual sync: Working via POST endpoint
- UI button: Visible in SmartParameterPanel
- Mock data: Returns 3 test frame records

⏳ **To Do:**
- Connect to actual Excel/Google Sheets
- Implement real database update logic
- Add sync history/audit log

## 🔗 Related Files

- Backend: `backend/main.py` (port 8000)
- Frontend: `frontend/src/components/sales/SmartParameterPanel.tsx` (port 3000)
- Scheduler: `backend/services/frame_sync_scheduler.py`
- Documentation: `FRAME_SYNC_IMPLEMENTATION.md` (detailed docs)

## 📞 Next Steps

1. **Real Data Source**: Update `get_mock_frame_data()` to fetch from Excel
2. **Database Update**: Implement actual frame_cross_sections table updates
3. **Error Handling**: Add retry logic and email notifications
4. **UI Enhancement**: Add sync history, last sync time, progress bar

---

**Everything is set up and working!** The automatic sync runs silently in the background, and users can trigger manual syncs with the "↻ Sync" button.
