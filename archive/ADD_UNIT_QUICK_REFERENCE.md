# Add Unit Feature - Quick Reference Guide

## 🎯 User Flow

### Step 1: Navigate to Projects Dashboard
- URL: `/projects` or click "All Projects" in navigation
- View list of all client projects with their details

### Step 2: Locate Target Project
- Use search bar to filter by client name or address
- Each project card displays:
  - Client name
  - Date
  - Address
  - Current unit count badge

### Step 3: Click "Add Unit" Button
- Look for the "Add Unit" button in the project card footer
- Button position: Between "View Details" (primary) and Delete icon
- Styling: White background with border, plus icon on left

### Step 4: Fill Unit Details Form

**Required Fields:**
1. **Frame Series** (dropdown)
   - Auto-populated from available series
   - Example: Series 86, Series 135

2. **Product Type** (dropdown)
   - Options: Window, Door, Sliding Door, Sliding Window

3. **Width** (number input)
   - Range: 12-120 inches
   - Placeholder: 36

4. **Height** (number input)
   - Range: 12-120 inches
   - Placeholder: 48

5. **Glass Type** (dropdown)
   - Options: Clear, Low-E, Tinted, Tempered, Laminated

6. **Frame Color** (dropdown)
   - Options: White, Bronze, Black, Gray, Custom

**Optional Fields:**
7. **Configuration** (dropdown)
   - Options: Single, Double, Triple, Custom
   - Pre-selected: Single

### Step 5: Submit or Cancel
- **Add Unit Button:** Saves the unit to the project
  - Dark button in modal footer
  - Updates project unit count immediately
  - Closes modal automatically on success

- **Cancel Button:** Discards changes
  - Light button in modal footer
  - No changes made to project

- **Close Icon (X):** Same as Cancel
  - Top-right corner of modal

---

## 🎨 Visual Design Elements

### Button Styles

**Primary Button** ("View Details", "Add Unit" in modal)
- Background: #1a1a1a (black)
- Text: White
- Border radius: 8px
- Padding: 12px 24px
- Font weight: 600
- Hover: Lifts 2px with enhanced shadow

**Secondary Button** ("Add Unit" on card, "Cancel")
- Background: White
- Border: 2px solid #e5e5e5
- Text: Black
- Border radius: 8px
- Padding: 10px 18px
- Font weight: 600
- Hover: Lifts 1px with subtle shadow

### Modal Design
- **Width:** 600px (95% on mobile)
- **Max height:** 90vh with scroll
- **Backdrop:** 50% opacity black with 2px blur
- **Border radius:** 12px
- **Shadow:** Multi-layer depth effect
- **Animation:** Slide up from bottom (0.3s)

### Form Inputs
- **Border:** 1px solid #e5e5e5
- **Border radius:** 8px
- **Padding:** 10-12px
- **Focus state:** Dark border with shadow ring
- **Font:** Inter, 14px, 500-600 weight

---

## 🔧 Technical Details

### API Endpoint
```
POST /api/projects/{project_id}/units
```

**Request Body:**
```json
{
  "series": "86",
  "productType": "Window",
  "width": 36,
  "height": 48,
  "glassType": "Clear",
  "frameColor": "White",
  "configuration": "Single"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Unit added successfully to project",
  "unit": {
    "id": "unit_1_1738012345.67",
    "series": "86",
    "productType": "Window",
    "width": 36,
    "height": 48,
    "glassType": "Clear",
    "frameColor": "White",
    "configuration": "Single"
  }
}
```

### State Updates
1. API call made to backend
2. On success: Project unitCount incremented locally
3. UI updates immediately (optimistic update pattern ready)
4. Modal closes and clears form

---

## 📱 Responsive Behavior

### Desktop (> 640px)
- Modal: 600px width, centered
- Form: Two-column grid for width/height
- Buttons: Horizontal layout in footer

### Mobile (≤ 640px)
- Modal: 95% width, centered
- Form: Single column layout
- Buttons: Stacked vertically (full width)
- Adjusted padding for smaller screens

---

## ⌨️ Keyboard Shortcuts

- **Escape:** Close modal (when modal is open)
- **Enter:** Submit form (when inside form field)
- **Tab:** Navigate between form fields

---

## 🚨 Error States

### Validation Errors
- Empty required fields: Browser default validation
- Width/Height out of range: Input validation prevents submission
- Invalid numbers: Browser prevents non-numeric input

### API Errors
- Network error: Console log (toast notification ready)
- Server error: Console log with error message
- Modal remains open on error for retry

---

## 🎯 Success Indicators

1. **Modal Closes:** Automatic after successful submission
2. **Unit Count Updates:** Badge on project card increments by 1
3. **Console Log:** Success message in browser console
4. **No Errors:** Clean submission without warnings

---

## 💡 Pro Tips

### For Users
- **Quick Add:** Click "Add Unit" instead of entering full editor
- **Batch Entry:** Can add multiple units sequentially without leaving dashboard
- **Search First:** Use search bar to quickly find target project
- **Validation:** All fields validate before submission prevents errors

### For Developers
- **Reusable Modal:** AddUnitModal component can be used in other contexts
- **Type Safety:** Full TypeScript coverage from frontend to backend
- **Extensible:** Easy to add more fields or validation rules
- **State Pattern:** Clean separation between UI state and data state

---

## 🔍 Troubleshooting

### Modal Won't Open
- Check browser console for errors
- Verify project ID is passed correctly
- Ensure `isAddUnitModalOpen` state is managed

### Form Won't Submit
- Check all required fields are filled
- Verify width/height are within 12-120 range
- Check network tab for API request status

### Unit Count Not Updating
- Verify API response is successful
- Check `handleAddUnitSubmit` updates local state
- Ensure project ID matches correctly

---

## 📊 Component Hierarchy

```
ProjectsListPage
├── SearchInput
├── NewProjectButton
├── ProjectsGrid
│   └── ProjectCard (multiple)
│       ├── ViewDetailsButton
│       ├── AddUnitButton ← Triggers modal
│       └── DeleteButton
├── CreateProjectModal
└── AddUnitModal ← New feature
    ├── SeriesDropdown
    ├── ProductTypeDropdown
    ├── DimensionsInputs
    ├── GlassTypeDropdown
    ├── FrameColorDropdown
    ├── ConfigurationDropdown
    ├── CancelButton
    └── AddButton
```

---

## 🎨 Color Palette

### Primary Colors
- **Black:** #1a1a1a (buttons, text)
- **White:** #ffffff (backgrounds, button text)
- **Gray:** #666666 (secondary text)
- **Light Gray:** #f5f5f5 (backgrounds)
- **Border Gray:** #e5e5e5 (dividers, borders)

### Interactive States
- **Hover Gray:** #333333 (dark buttons)
- **Hover Light:** #f9f9f9 (light buttons)
- **Focus Blue:** rgba(26, 26, 26, 0.1) (focus ring)

---

*Quick Reference Guide - Updated January 23, 2026*
