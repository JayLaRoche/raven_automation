# Projects Dashboard - Visual & Component Reference

## 🎨 Dashboard Layout

```
┌─────────────────────────────────────────────────────────┐
│ Raven Doors & Windows        Projects  | Settings  ⚙️  │  ← Header
├─────────────────────────────────────────────────────────┤
│                                                          │
│  Projects                                    [+ New Project] │  ← Title
│  Manage your window specification projects              │
│                                                          │
│  ┌────────────────────────────────────────────────────┐ │
│  │ Search by client name or job site address...      │ │  ← Search
│  └────────────────────────────────────────────────────┘ │
│                                                          │
│  ┌──────────────┬──────────────┬──────────────┐        │
│  │              │              │              │        │
│  │ ProjectCard  │ ProjectCard  │ ProjectCard  │        │
│  │              │              │              │        │  ← Grid
│  ├──────────────┼──────────────┼──────────────┤        │
│  │              │              │              │        │
│  │ ProjectCard  │ ProjectCard  │ ProjectCard  │        │
│  │              │              │              │        │
│  └──────────────┴──────────────┴──────────────┘        │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

---

## 📇 ProjectCard Component

```
┌──────────────────────────────────┐
│ Steve Delrosa        [35 units]  │  ← Header (Name + Badge)
├──────────────────────────────────┤
│ 📅 January 15, 2025              │  ← Date row
│ 📍 1234 Maple Avenue...          │  ← Address row
├──────────────────────────────────┤
│ [  View Details  ]  [🗑️]         │  ← Footer (Button + Delete)
└──────────────────────────────────┘
```

---

## 🎯 Component Hierarchy

```
App.tsx
├── BrowserRouter
└── Routes
    ├── Route "/" → ProjectDashboard
    │   ├── Header
    │   │   ├── Logo
    │   │   └── Nav (Projects | Settings)
    │   ├── TitleSection
    │   │   ├── Title + Subtitle
    │   │   └── "New Project" Button
    │   ├── SearchContainer
    │   │   └── Search Input
    │   └── ProjectsGrid
    │       └── ProjectCard[] (6 cards)
    │           ├── CardHeader (Name + Badge)
    │           ├── CardDetails (Date + Address)
    │           └── CardFooter (Button + Delete)
    │
    └── Route "/project/:id" → SalesPresentation
        ├── Header (with Back button)
        ├── Left Panel (Parameters)
        └── Right Panel (Canvas)
```

---

## 📝 Data Flow

### Initial Load: Home Page
```
1. App.tsx renders
2. Router evaluates "/" route
3. ProjectDashboard component renders
4. Local state initialized:
   - projects: [...6 sample projects]
   - searchQuery: ""
   - activeTab: "projects"
5. Grid displays all 6 ProjectCards
6. Icons load from lucide-react
7. CSS modules applied
```

### Search Interaction
```
1. User types in search input
2. onChange handler updates searchQuery state
3. filteredProjects computed:
   - Filter by clientName OR address
   - Case-insensitive matching
4. Grid re-renders with filtered results
5. If no results, show empty state
```

### Navigation to Project
```
1. User clicks "View Details" button
2. onClick handler calls navigate(`/project/${project.id}`)
3. Router switches to "/project/:id" route
4. SalesPresentation component renders
5. useParams hook reads ID from URL
6. useNavigate hook available for back navigation
7. Back button in header calls navigate("/")
8. Returns to dashboard
```

### Delete Project
```
1. User clicks trash icon
2. onClick handler calls handleDelete
3. Prevents event propagation
4. Shows confirmation dialog: "Delete project '...'?"
5. If confirmed:
   - Call onDelete(projectId)
   - Filter projects array
   - Remove from state
   - Grid re-renders
6. If cancelled:
   - Dialog closes
   - State unchanged
```

---

## 🎨 CSS Class Structure

### ProjectDashboard.module.css
```
.container          → Main flex container
.header             → Sticky header
.headerContent      → Max-width wrapper
.logo               → Serif font title
.nav                → Navigation tabs
.navButton          → Tab button with active state
.main               → Main content area
.titleSection       → Title + button row
.pageTitle          → Large serif heading
.subtitle           → Subtitle text
.newProjectButton   → Black button
.searchContainer    → Search wrapper
.searchInput        → Text input field
.projectsGrid       → CSS Grid layout
.emptyState         → No results message
.settingsSection    → Settings tab content
.settingsTitle      → Settings heading
.settingsText       → Settings placeholder
```

### ProjectCard.module.css
```
.card               → Main card container
.cardHeader         → Name + badge row
.clientName         → Project name
.unitBadge          → Grey pill badge
.cardDetails        → Date + address section
.detailRow          → Icon + text row
.icon               → Lucide icon styling
.detailText         → Detail text styling
.cardFooter         → Button row
.viewButton         → Black view button
.deleteButton       → Icon delete button
```

---

## 🎯 State Management

### ProjectDashboard State
```typescript
const [projects, setProjects] = useState<Project[]>(MOCK_PROJECTS)
// → All projects, updated on delete

const [searchQuery, setSearchQuery] = useState('')
// → Current search term, updated on input

const [activeTab, setActiveTab] = useState<'projects' | 'settings'>('projects')
// → Current active tab, updated on click

const filteredProjects = projects.filter(...)
// → Computed, not state
```

### ProjectCard Props
```typescript
interface ProjectCardProps {
  project: Project           // Single project object
  onDelete?: (id) => void   // Delete callback
}
```

---

## 🔌 Hooks Used

### ProjectDashboard
```typescript
import { useState } from 'react'
// useState - manage projects, search, activeTab

import { useNavigate } from 'react-router-dom'
// (Not used in dashboard, but available)
```

### ProjectCard
```typescript
import { useNavigate } from 'react-router-dom'
// useNavigate() - navigate to /project/:id
```

### SalesPresentation
```typescript
import { useParams } from 'react-router-dom'
// useParams() - read :id from URL

import { useNavigate } from 'react-router-dom'
// useNavigate() - navigate back to /
```

---

## 💾 Mock Data Structure

```typescript
interface Project {
  id: number
  clientName: string
  date: string                    // "2025-01-15"
  address: string                 // "1234 Maple Avenue, Springfield, IL 62701"
  unitCount: number               // 35
  status?: 'active' | 'completed' // Optional
}

// Example:
{
  id: 1,
  clientName: "Steve Delrosa",
  date: "2025-01-15",
  address: "1234 Maple Avenue, Springfield, IL 62701",
  unitCount: 35,
  status: "active"
}
```

---

## 🎨 Color Usage Guide

```typescript
// Primary Elements
.logo               → #1a1a1a (Black)
.pageTitle          → #1a1a1a (Black)
.clientName         → #1a1a1a (Black)

// Buttons
.newProjectButton   → #1a1a1a (Black) bg, #fff text
.viewButton         → #1a1a1a (Black) bg, #fff text
.deleteButton       → #f5f5f5 (Light grey) bg
.deleteButton:hover → #e5e5e5 (Darker grey) bg, #d32f2f red

// Text
.subtitle           → #666 (Medium grey)
.detailText         → #666 (Medium grey)
.searchInput        → #999 (Light grey) placeholder

// Borders & Backgrounds
.card               → #ffffff (White) bg, #e5e5e5 border
.header             → #ffffff (White) bg, #e5e5e5 border-bottom
.container          → #f9f9f9 (Off-white) bg
.unitBadge          → #f0f0f0 (Very light grey) bg, #666 text
```

---

## 🔤 Typography Usage

```typescript
// Logo & Headings
font-family: 'Playfair Display', 'Georgia', serif
font-weight: 600 (semi-bold)
font-size: 48px (page title)
font-size: 24px (logo)

// Body & Buttons
font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif
font-weight: 400 (regular) or 600 (bold)
font-size: 16px (body)
font-size: 14px (small)
font-size: 13px (labels)
```

---

## 📏 Spacing Reference

```
Header padding:     20px vertical, 40px horizontal
Main padding:       60px vertical, 40px horizontal
Card padding:       24px
Title gap:          40px (below)
Grid gap:           24px (between cards)
Detail row gap:     12px (icon to text)
Card section gap:   20px (header to details to footer)
Border padding:     16px (top/bottom)
Button padding:     12px vertical, 24px horizontal
```

---

## 🔄 Event Flow Diagram

```
User opens http://localhost:3000/
        ↓
App.tsx mounts
        ↓
Router matches "/"
        ↓
ProjectDashboard renders
        ↓
useState initializes (projects, search, tab)
        ↓
Component displays with 6 ProjectCards
        ↓
┌─ User interaction ──────────────────┐
│                                      │
│ Search:      Input → State → Filter │
│              ↓                       │
│              Grid updates            │
│                                      │
│ View Details: Click → navigate()    │
│              ↓                       │
│              "/project/1" route     │
│              ↓                       │
│              SalesPresentation      │
│                                      │
│ Delete:      Click → Confirm → State│
│              ↓                       │
│              Grid updates            │
│                                      │
│ Back Button: Click → navigate()     │
│              ↓                       │
│              "/" route              │
│              ↓                       │
│              ProjectDashboard       │
│                                      │
└──────────────────────────────────────┘
```

---

## 📱 Responsive Breakpoints

```
Desktop   1024px+
  │
  └─ Grid: repeat(auto-fill, minmax(320px, 1fr))
     Max-width: 1400px
     Padding: 40px

Tablet    768px - 1023px
  │
  └─ Grid: repeat(auto-fill, minmax(280px, 1fr))
     Padding: 24px
     Font: -2px

Mobile    480px - 767px
  │
  └─ Grid: 1 column
     Padding: 16px
     Stacked header
     Full-width buttons

Small     < 480px
  │
  └─ Grid: 1 column
     Padding: 16px
     Compact spacing
     Small fonts
```

---

## ✨ Interaction States

### Button States
```
Default:  #1a1a1a bg, #fff text
Hover:    #333333 bg, #fff text, translateY(-1px)
Active:   #333333 bg, #fff text, translateY(0)
```

### Card States
```
Default:  #fff bg, 1px #e5e5e5 border, shadow-sm
Hover:    #fff bg, 1px #e5e5e5 border, shadow-md, translateY(-2px)
```

### Input States
```
Default:  #fff bg, 1px #e5e5e5 border
Focus:    #fff bg, 1px #1a1a1a border, box-shadow outline
```

---

## 🚀 Performance Considerations

- Grid uses CSS Grid (GPU accelerated)
- Search filtering is O(n) - fine for <1000 projects
- No heavy JavaScript computations
- Icons are SVG (minimal file size)
- CSS modules prevent style conflicts
- Mock data is hardcoded (no API overhead)

---

## 📖 Component Documentation Template

When you add new components, follow this pattern:

```typescript
interface ComponentProps {
  // Props with JSDoc comments
  /** Description of prop */
  prop: type
}

/**
 * Component description
 * 
 * @example
 * <Component prop="value" />
 */
export function Component({ prop }: ComponentProps) {
  return <div>{prop}</div>
}
```

---

## 🎯 Summary

The Projects Dashboard provides:
- **Elegant Entry Point** - Professional first impression
- **Easy Navigation** - Intuitive routing and back buttons
- **Responsive Design** - Works on all devices
- **Mock Data Ready** - Can be replaced with API calls
- **Extensible** - Easy to add features
- **Type Safe** - Full TypeScript support
- **Well Documented** - Multiple guides available

All files are created and ready to use! 🎉
