# Projects Dashboard - Quick Setup Guide

## 📦 Installation Steps

### Step 1: Install Icon Library
```bash
cd frontend
npm install lucide-react
```

### Step 2: Add Fonts to HTML
Edit `frontend/index.html` and add this line in the `<head>` section:

```html
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;600&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
```

### Step 3: Start Development Server
```bash
npm run dev
```

### Step 4: Access Dashboard
Open `http://localhost:3000/` in your browser

---

## 🎯 What You'll See

### Landing Page (Home `/`)
A professional projects dashboard with:
- Header with "Raven Doors & Windows" title
- Projects tab (active) and Settings tab
- "Projects" heading with subtitle
- Search bar to find projects
- Grid of 6 sample project cards

### Project Card
Each card shows:
- Client name
- Unit count badge (e.g., "35 units")
- Date with calendar icon
- Address with map pin icon
- "View Details" button
- Delete button

### Clicking "View Details"
Routes to `/project/1` which loads the existing SalesPresentation component with a "← Back" button to return.

---

## 🔄 User Flow

```
Home (/) 
  ↓
ProjectDashboard Page
  ↓ Click "View Details"
/project/1
  ↓
SalesPresentation Editor
  ↓ Click "← Back"
Home (/)
```

---

## 📁 Files Created

```
frontend/src/
├── App.tsx                                 (UPDATED)
├── types/
│   └── project.ts                         (NEW)
└── components/dashboard/
    ├── ProjectDashboard.tsx               (NEW)
    ├── ProjectDashboard.module.css        (NEW)
    ├── ProjectCard.tsx                    (NEW)
    └── ProjectCard.module.css             (NEW)
```

---

## ✨ Features Ready

✅ Dashboard with 6 sample projects
✅ Search by client name or address
✅ Responsive grid layout
✅ Delete projects with confirmation
✅ Navigate to project editor
✅ Back button from editor
✅ Professional styling
✅ Mobile responsive

---

## 🚀 Next: Backend Integration

When you're ready to connect to a real backend:

1. Replace mock data in `ProjectDashboard.tsx`:
   ```typescript
   // Replace MOCK_PROJECTS with API call:
   const { data: projects } = useQuery({
     queryKey: ['projects'],
     queryFn: () => fetch('/api/projects').then(r => r.json())
   })
   ```

2. Update project IDs to match your database
3. Add create/edit endpoints

---

## 🎨 Customization

### Change Colors
Edit `.module.css` files:
- `#1a1a1a` = Primary black
- `#666` = Secondary text
- `#e5e5e5` = Borders

### Change Fonts
Update in `index.html`:
```html
<!-- Change serif font -->
<link href="https://fonts.googleapis.com/css2?family=YOUR-SERIF-FONT&display=swap" rel="stylesheet">
```

### Change Button Text
Edit `ProjectDashboard.tsx` and `ProjectCard.tsx`

---

## 🐛 Troubleshooting

### Icons not showing?
- Make sure lucide-react is installed: `npm install lucide-react`
- Check browser console for import errors

### Fonts not loading?
- Check that fonts link is in `index.html` `<head>`
- Check network tab in DevTools for 404 errors
- Fallback fonts will display if Google Fonts fails

### Navigation not working?
- Make sure you're using the dev server (`npm run dev`)
- Check that React Router is properly installed
- Check browser console for routing errors

---

## 📞 Support

Issues? Check:
1. Console for error messages
2. Network tab for failed requests
3. DevTools for missing CSS/fonts
4. Verify all files were created correctly

---

## ✅ Ready to Go!

You now have a professional Projects Dashboard as your app's entry point. Happy coding! 🎉
