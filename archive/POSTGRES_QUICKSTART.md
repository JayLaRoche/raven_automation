# 🚀 PostgreSQL Quick Start Guide

## ✅ System Status: **OPERATIONAL**

Your Raven Custom Glass drawing system is now running on PostgreSQL with comprehensive reference data.

---

## 📦 What's Running

- **PostgreSQL 15** on `localhost:5432`
- **pgAdmin 4** on `http://localhost:5050`
- **Reference Data**: 60+ records for accurate drawings

---

## 🎯 Quick Commands

### Start/Stop Database
```bash
# Start containers
cd c:\Users\larochej3\Desktop\raven-shop-automation
docker-compose up -d

# Stop containers
docker-compose down

# View status
docker ps
```

### Generate Drawings
```bash
cd backend

# Demo drawing with reference data
python quick_start_postgres.py

# From Google Sheets
python generate_from_sheet.py "Sheet Name"

# Integration test
python test_postgres_integration.py
```

### Database Access
```bash
# Via pgAdmin (browser)
http://localhost:5050
Email: admin@ravencustomglass.com
Password: admin2025

# Via command line
docker exec -it raven_postgres psql -U raven_user -d raven_drawings
```

---

## 📊 Reference Data Available

### Frame Series (5)
- Series 80 (80mm) - Fixed windows
- Series 86 (86mm) - Casements
- Series 90 (90mm) - Sliders
- Series 135 (135mm) - Patio doors  
- Series 200 (200mm) - Commercial

### Configurations (13)
- Fixed, Casement, Slider, Bifold, Accordion, etc.

### Glass Types (9)
- Single/Dual/Triple Pane
- Low-E coatings
- Tempered, Laminated, Impact Resistant

### Hardware (12+)
- Locks, Operators, Hinges, Handles

### Colors (9)
- White, Bronze, Black, Silver, etc.

---

## 🔍 Sample Queries

```sql
-- View all frame series
SELECT series_name, frame_width_mm, nail_fin_width_mm 
FROM frame_series 
ORDER BY series_code;

-- Find slider configurations
SELECT config_name, panel_count, operable_panels
FROM configuration_types 
WHERE config_name LIKE '%Slider%';

-- Glass options with U-factors
SELECT glass_name, u_factor, shgc 
FROM glass_types 
ORDER BY u_factor;

-- All white hardware
SELECT hardware_name, hardware_type, finish
FROM hardware_options 
WHERE finish LIKE '%White%';
```

---

## 📝 Generate Drawing Example

```python
from services.drawing_engine import ProfessionalDrawingGenerator

window = {
    'width': 48,
    'height': 60,
    'configuration': 'Slider 4-Panel',
    'frame_series': 'Series 90',       # ← From reference data
    'glass_type': 'Low-E Dual Pane',   # ← From reference data
    'hardware': 'Slider Window Lock',  # ← From reference data
    'frame_color': 'White'             # ← From reference data
}

generator = ProfessionalDrawingGenerator()
pdf = generator.generate_window_drawing(window, project_data)
```

---

## 🆘 Troubleshooting

### Database won't start
```bash
docker-compose down
docker-compose up -d
docker logs raven_postgres
```

### Reference data missing
```bash
cd backend
python database/init_db.py
Get-Content database/init/02_seed_reference_data.sql | docker exec -i raven_postgres psql -U raven_user -d raven_drawings
```

### Connection refused
Check `.env` file:
```env
DATABASE_URL=postgresql://raven_user:raven_password_2025@localhost:5432/raven_drawings
```

---

## 📚 Documentation

- [POSTGRES_MIGRATION.md](POSTGRES_MIGRATION.md) - Complete migration guide
- [docker-compose.yml](docker-compose.yml) - Container configuration
- [backend/.env.example](backend/.env.example) - Environment template

---

**Last Updated**: December 24, 2025  
**Status**: Production Ready ✅
