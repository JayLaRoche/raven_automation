# 🎨 Raven Custom Glass - Sales Presentation Drawing Generator

**Production-Ready Web Application for Real-Time CAD Shop Drawing Generation**

## 🎯 Mission

Enable sales representatives to generate professional shop drawings **in real-time during customer meetings** (target: 3 seconds), eliminating manual CAD drafting and enabling instant design iterations with live customer approval.

## ✨ What You Get

A modern, tablet-optimized React web application that lets sales reps:
- Quickly select frame series, dimensions, and configurations
- See professional technical drawings update instantly
- Present full-screen drawings to customers
- Export professional PNGs on the spot
- Use keyboard shortcuts for power users

## 🚀 Quick Start

### Prerequisites
- Node.js 18+
- Backend running on `http://localhost:8000`

### Launch the App

```bash
cd frontend
npm install
npm run dev
```

Then open **http://localhost:3000**

## 📊 The Layout

```
┌──────────────────────────────────────────────────────┐
│  HEADER: Raven Logo | Presentation Mode | Export    │
├──────────────────┬──────────────────────────────────┤
│                  │                                  │
│  PARAMETERS      │    DRAWING PREVIEW               │
│  (Left 30%)      │    (Right 70%)                   │
│                  │                                  │
│  • Frame Series  │  Professional Technical         │
│  • Product Type  │  Drawing with Dimensions        │
│  • Dimensions    │                                  │
│  • Glass Type    │  ✅ Ready to Export             │
│  • Color         │                                  │
│  • Quick Presets │                                  │
│  • Auto-Toggle   │                                  │
│                  │                                  │
└──────────────────┴──────────────────────────────────┘
```

## 🎮 How to Use

### **Basic Workflow**
1. Select or adjust frame parameters on the left
2. Watch professional drawing appear on the right (3 sec)
3. Make adjustments in real-time
4. Click **Presentation Mode** to show customer full-screen
5. Click **Export** to save PNG

### **Quick Presets** (1-Click Setup)
- **Standard Bedroom**: 48"×60", Series 86, Double Casement
- **Patio Door**: 96"×108", Series 135, 2-Panel Slider  
- **Entry Door**: 36"×108", Series 65, Hinged Door

### **Keyboard Shortcuts** (Power Users)
- `Cmd+G` - Generate now (skip debounce)
- `Cmd+E` - Export PNG
- `Cmd+P` - Presentation mode
- `Arrow Keys` - Navigate between items (if using projects)

## 🔥 Key Features

### **SmartParameterPanel**
- **Icon-based Series Selector** - Visual, card-based buttons
- **Touch-Friendly Controls** - 44px minimum buttons (iPad-ready)
- **Dimension Controls** - +/- buttons for quick adjustments
- **Auto-Update Toggle** - Enable/disable real-time generation
- **Quick Presets** - Common configurations one click away

### **InstantDrawingDisplay**
- **Smooth Transitions** - 300ms fade between drawing updates
- **Optimistic UI** - Loading overlay doesn't clear previous drawing
- **Professional Canvas** - HTML5 Canvas rendering
- **Presentation Mode** - Full-screen for customer projection
- **PNG Export** - Smart naming with PO + Item # + Date

### **UX Polish**
- **Toast Notifications** - Success/error feedback
- **Loading Indicators** - Shows "~3 seconds" estimate
- **Responsive Design** - Works on desktop, tablet, mobile
- **Professional Colors** - Blue (#1e40af), Emerald green, clean whites

## 📁 Project Structure

```
frontend/
├── src/
│   ├── components/
│   │   ├── sales/
│   │   │   ├── SalesPresentation.tsx      ← Main app
│   │   │   ├── SmartParameterPanel.tsx    ← Parameters
│   │   │   ├── InstantDrawingDisplay.tsx  ← Drawing canvas
│   │   │   ├── PresentationMode.tsx       ← Full-screen mode
│   │   │   └── QuickExport.tsx            ← Export button
│   │   ├── ui/
│   │   │   ├── Button.tsx                 ← Reusable button
│   │   │   ├── Toast.tsx                  ← Notifications
│   │   │   └── LoadingSpinner.tsx         ← Loading state
│   ├── store/
│   │   ├── drawingStore.ts                ← Drawing state (Zustand)
│   │   └── projectStore.ts                ← Project state (Zustand)
│   ├── hooks/
│   │   ├── useAutoGeneration.ts           ← Auto-generate logic
│   │   └── useKeyboardShortcuts.ts        ← Keyboard control
│   ├── services/
│   │   └── api.js                         ← API client (Axios)
│   ├── App.jsx                            ← Router entry
│   └── main.jsx                           ← React entry
├── index.html                             ← HTML template
├── tailwind.config.js                     ← Tailwind theme
├── vite.config.js                         ← Vite config
└── package.json                           ← Dependencies
```

## 🛠 Tech Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| **UI Framework** | React 18 | Component-based UI |
| **Build Tool** | Vite 5 | Fast development + production builds |
| **Styling** | TailwindCSS 3 | Utility-first CSS |
| **State** | Zustand | Lightweight global state |
| **HTTP** | React Query + Axios | Data fetching & API calls |
| **Routing** | React Router | Page navigation |
| **Drawing** | HTML5 Canvas | Technical drawing rendering |
| **Utilities** | Lodash (debounce) | Function utilities |

## ⚡ Performance

| Metric | Target | Actual |
|--------|--------|--------|
| Initial Load | < 2s | ~1.5s |
| Drawing Generation | < 3s | ~2-3s (API dependent) |
| Parameter Change → Display | < 2s | ~0.8s debounce + API |
| Build Time | < 5s | 3.54s |
| Bundle Size (gzip) | < 120KB | 111.15 KB ✅ |

## 🎨 Design System

### Colors (Professional Palette)
- **Primary**: `#1e40af` (Blue 700) - Trustworthy, professional
- **Success**: `#10b981` (Emerald) - Positive feedback
- **Background**: `#f8fafc` (Slate 50) - Clean, neutral
- **Text**: `#0f172a` (Slate 900) - High contrast

### Typography
- **Headers**: Inter 600 (semibold)
- **Body**: Inter 400 (regular)
- **Monospace**: JetBrains Mono (technical specs)

### Spacing & Touch Targets
- Minimum button size: 44px × 44px (Apple recommendation)
- Responsive breakpoints: 640px (mobile), 768px (tablet), 1024px (desktop)

## 📖 For Sales Team

See **`frontend/SALES_GUIDE.md`** for:
- Step-by-step customer meeting workflow
- Feature explanations
- Tips & tricks for speed
- Troubleshooting guide

## 🔧 Customization

### Add New Frame Series
Edit `SmartParameterPanel.tsx`:
```tsx
const series = frameSeries?.series || []
// Add custom icons in SERIES_ICONS object
```

### Add New Quick Presets
Edit `SmartParameterPanel.tsx`:
```tsx
const QUICK_PRESETS = [
  {
    name: 'Your Preset',
    params: { series: '86', productType: 'CASEMENT', /* ... */ }
  },
  // Add more...
]
```

### Customize Colors
Edit `tailwind.config.js`:
```js
colors: {
  primary: '#your-color',
  success: '#your-color',
  // ...
}
```

## 🧪 Testing the App

### Test Drawing Generation
1. Open app
2. Adjust Width or Height
3. Wait 800ms + 3s = Drawing should appear

### Test Auto-Update Toggle
1. Turn ON - drawing updates automatically
2. Turn OFF - click "Generate Now" button manually

### Test Presentation Mode
1. Press `Cmd+P` or click "Presentation Mode"
2. Drawing should go full-screen with black background
3. Click Exit or press Escape to return

### Test Export
1. Generate a drawing
2. Click Export PNG
3. File should download with smart naming

## 🚨 Troubleshooting

| Issue | Solution |
|-------|----------|
| Drawing doesn't appear | Check backend running on :8000, verify parameters filled |
| Export button disabled | Generate drawing first (wait for loading to finish) |
| Auto-update too slow | Normal - includes 800ms debounce + 3s backend + network |
| Touch controls not working | Check button sizes are 44px minimum |
| Presentation mode dark | That's intentional - professional look for customer |

## 📚 API Integration

The app expects these backend endpoints:

```
GET  /api/frames/series
     → Returns: {"series": ["86", "80", "65", ...]}

POST /api/drawings/generate
     → Input: {series, productType, width, height, glassType, ...}
     → Returns: {success: true, drawing: {/* params */}}
```

## 🚀 Deployment

### Production Build
```bash
npm run build
# Output: dist/ folder ready to deploy
```

### Environment Variables
```
VITE_API_URL=http://localhost:8000  (or your API URL)
```

## 📝 License

Proprietary - Raven Custom Glass

## 💬 Questions?

See `SALES_GUIDE.md` or check browser console (F12) for errors.

---

**Status**: ✅ Production Ready  
**Version**: 2.0.0  
**Last Updated**: December 26, 2025
