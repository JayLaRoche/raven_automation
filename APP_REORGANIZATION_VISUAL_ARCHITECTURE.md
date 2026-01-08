# App Reorganization - Visual Architecture

## New App Structure Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                        App.tsx (Root)                       │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌──────────────────────────────────────────────────────┐  │
│  │              Navigation Component                     │  │
│  │  ┌─────────────────────────────────────────────────┐ │  │
│  │  │ Raven Doors & Windows  Dashboard | Generator  │ │  │
│  │  │                        ▔▔▔▔▔▔▔▔ (active)      │ │  │
│  │  └─────────────────────────────────────────────────┘ │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐  │
│  │                Routes (URL-based)                    │  │
│  │                                                       │  │
│  │  /                 → Dashboard Component             │  │
│  │  /generator        → SalesPresentation Component     │  │
│  │  /project/:id      → SalesPresentation Component     │  │
│  │  /projects         → ProjectDashboard Component      │  │
│  │                                                       │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐  │
│  │         Active Component Rendered Below              │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## User Journey Map

### Complete User Flow

```
First Visit
│
├─ http://localhost:3001/
│  │
│  ├─ Navigation renders (Dashboard tab = ACTIVE)
│  └─ Dashboard Component renders
│     │
│     ├─ Hero Section
│     ├─ Quick Action Cards
│     │  ├─ "Start New Drawing" → navigate('/generator')
│     │  └─ "View All Projects" → placeholder
│     └─ Recent Projects List
│        └─ Project Cards with "Open Project" buttons
│
├─ User clicks "Start New Drawing"
│  │
│  └─ navigate('/generator') 
│     │
│     ├─ URL changes to /generator
│     ├─ Navigation detects path, activates "Drawing Generator" tab
│     └─ SalesPresentation Component renders
│        │
│        ├─ Left Panel: Parameters
│        ├─ Right Panel: Canvas Preview
│        ├─ Header: Full Screen toggle
│        └─ Export Options
│
├─ User clicks back on Dashboard tab
│  │
│  └─ navigate('/')
│     │
│     ├─ URL changes to /
│     ├─ Navigation detects path, activates "Dashboard" tab
│     └─ Dashboard Component renders again
│
└─ User clicks "Open Project" on recent project
   │
   └─ navigate(`/project/${id}`)
      │
      ├─ URL changes to /project/1
      ├─ Navigation tabs remain visible
      └─ SalesPresentation Component renders
         │
         ├─ useParams hook reads :id
         ├─ useNavigate available for back navigation
         └─ Full drawing editor with project context
```

---

## Component Hierarchy

```
<App>
  │
  ├─ <BrowserRouter>
  │  │
  │  ├─ <Navigation>
  │  │  ├─ useLocation() → detects current route
  │  │  ├─ useNavigate() → navigation handler
  │  │  │
  │  │  └─ Renders:
  │  │     ├─ Logo ("Raven Doors & Windows")
  │  │     └─ Tabs with active indicator
  │  │        ├─ Dashboard tab
  │  │        └─ Drawing Generator tab
  │  │
  │  ├─ <Routes>
  │  │  │
  │  │  ├─ Route "/" 
  │  │  │  └─ <Dashboard>
  │  │  │     ├─ Hero Section
  │  │  │     ├─ Quick Actions
  │  │  │     ├─ Recent Projects
  │  │  │     └─ Stats
  │  │  │
  │  │  ├─ Route "/generator"
  │  │  │  └─ <SalesPresentation>
  │  │  │     ├─ (no projectId from URL)
  │  │  │     ├─ Left Panel: Drawing Parameters
  │  │  │     └─ Right Panel: Canvas Preview
  │  │  │
  │  │  ├─ Route "/project/:id"
  │  │  │  └─ <SalesPresentation>
  │  │  │     ├─ useParams() → reads :id
  │  │  │     ├─ Left Panel: Drawing Parameters
  │  │  │     └─ Right Panel: Canvas Preview
  │  │  │
  │  │  ├─ Route "/projects"
  │  │  │  └─ <ProjectDashboard>
  │  │  │     ├─ Projects List
  │  │  │     └─ Project Cards
  │  │  │
  │  │  └─ Route "*"
  │  │     └─ <Navigate to="/" />
  │  │
  │  └─ <ToastContainer>
  │
  └─ </BrowserRouter>
```

---

## State Management Flow

```
Navigation Component
    │
    ├─ useLocation()
    │  ├─ Reads current pathname
    │  ├─ Compares against '/dashboard', '/generator'
    │  └─ Sets active tab styling
    │
    └─ useNavigate()
       └─ Provides navigate() function for tab clicks

SalesPresentation Component  
    │
    ├─ useParams()
    │  ├─ Reads :id from URL (/project/:id)
    │  └─ Used to load project-specific data
    │
    ├─ useNavigate()
    │  └─ Provides navigate() for back button, etc.
    │
    └─ useDrawingStore() (Zustand)
       ├─ Drawing parameters
       ├─ Canvas content
       ├─ Auto-update setting
       └─ Presentation mode toggle

Dashboard Component
    │
    └─ useState()
       ├─ Recent projects (mocked, later from API)
       └─ Navigation handlers via useNavigate()
```

---

## Route Comparison

### Before Reorganization
```
/              → ProjectDashboard (projects list)
/project/:id   → SalesPresentation (drawing tool)
```

### After Reorganization
```
/              → Dashboard (home page, recent projects)
/generator     → SalesPresentation (new drawing)
/project/:id   → SalesPresentation (edit project)
/projects      → ProjectDashboard (legacy, kept for compat)
```

**Key Difference**: Dashboard is now the landing page with links to either create new or edit existing projects.

---

## Navigation Tab Behavior

### Tab Click Event Flow
```
User clicks "Dashboard" tab
    ↓
tab.onClick → navigate('/')
    ↓
Router updates location to '/'
    ↓
Navigation component re-renders
    ↓
useLocation().pathname = '/'
    ↓
Dashboard tab className updated with .active
    ↓
useLocation() in route component returns '/'
    ↓
Dashboard component renders
```

### Active State Styling
```
Inactive Tab:
  color: #666
  font-weight: 500
  no ::after pseudo-element

Active Tab (Dashboard):
  color: #1a1a1a
  font-weight: 600
  ::after {
    height: 3px
    background: #1a1a1a
    position: absolute bottom
  }
```

---

## Responsive Layout Changes

### Desktop (1024px+)
```
┌─────────────────────────────────────────┐
│ Raven Doors & Windows  [Dashboard|Gen]  │
├─────────────────────────────────────────┤
│                                          │
│  Welcome Back                            │
│  Manage your projects...                │
│                                          │
│  Quick Actions                           │
│  ┌─────────────────┐  ┌─────────────┐   │
│  │ Start New ...   │  │ View All... │   │
│  └─────────────────┘  └─────────────┘   │
│                                          │
│  Recent Projects (3-column, then rows)   │
│  ...                                     │
└─────────────────────────────────────────┘
```

### Tablet (768px - 1023px)
```
┌──────────────────────────────┐
│ Raven Doors & Windows        │
│ [Dashboard] [Gen]            │
├──────────────────────────────┤
│                               │
│  Welcome Back                 │
│                               │
│  Quick Actions                │
│  ┌───────────────┐            │
│  │ Start New ... │            │
│  └───────────────┘            │
│  ┌───────────────┐            │
│  │ View All...   │            │
│  └───────────────┘            │
│                               │
│  Recent Projects (2-column)   │
│  ...                          │
└──────────────────────────────┘
```

### Mobile (<768px)
```
┌──────────────────┐
│ Raven...         │
│ [Dashboard]      │
│ [Drawing Gen]    │
├──────────────────┤
│ Welcome Back     │
│ Manage your...   │
│                  │
│ Quick Actions    │
│ ┌──────────────┐ │
│ │Start New ... │ │
│ └──────────────┘ │
│ ┌──────────────┐ │
│ │View All...   │ │
│ └──────────────┘ │
│                  │
│ Recent Projects  │
│ (single column)  │
│ ...              │
└──────────────────┘
```

---

## Color & Typography System

```
TYPOGRAPHY HIERARCHY
├─ Navigation Logo
│  └─ Playfair Display, 24px, 600w, black
│
├─ Page Titles (h1)
│  └─ Playfair Display, 48px, 600w, black
│
├─ Section Titles (h2)
│  └─ Playfair Display, 32px, 600w, black
│
├─ Card Titles
│  └─ Playfair Display, 20px, 600w, black
│
├─ Body Text
│  └─ Inter, 16px, 400w, #666
│
└─ Labels/Small Text
   └─ Inter, 13-14px, 500w, #999

COLOR PALETTE
├─ Primary: #1a1a1a (buttons, active states)
├─ Secondary: #666 (body text, supporting)
├─ Light: #f5f5f5, #f9f9f9 (backgrounds)
├─ Border: #e5e5e5
├─ Badge: #f0f0f0 bg, #666 text
└─ Hover: #333333 (darker black for hover states)
```

---

## File Dependency Graph

```
App.tsx
├── imports Navigation from ./components/layout/Navigation
│   └── Navigation.tsx
│       ├── imports Navigation.module.css
│       └── uses: useLocation, useNavigate from react-router-dom
│
├── imports Dashboard from ./components/layout/Dashboard
│   └── Dashboard.tsx
│       ├── imports Dashboard.module.css
│       ├── imports lucide-react icons (Plus, ArrowRight)
│       └── uses: useNavigate from react-router-dom
│
├── imports ProjectDashboard from ./components/dashboard/ProjectDashboard
│   └── ProjectDashboard.tsx (unchanged)
│
├── imports SalesPresentation from ./components/sales/SalesPresentation
│   └── SalesPresentation.tsx (unchanged)
│       ├── imports multiple sub-components
│       └── uses: useParams, useNavigate from react-router-dom
│
└── imports ToastContainer from ./components/ui/Toast
    └── Toast.tsx (unchanged)
```

---

## Summary

The reorganization creates a clearer user experience:

1. **Entry Point**: Dashboard (home, recent projects, stats)
2. **Navigation**: Tab-based system for switching between Dashboard and Drawing Generator
3. **Drawing Creation**: Two paths
   - `/generator` - Create new drawing from scratch
   - `/project/:id` - Edit existing project
4. **Backward Compatibility**: Original `/projects` route still works

All original SalesPresentation features (Full Screen mode, split layout, image validation, PDF export) remain fully intact.
