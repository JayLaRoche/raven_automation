# 🎨 How to Generate a Drawing in Raven Shop Drawing

## Step-by-Step Instructions

### 🌐 Open Your App

1. **Both servers are running:**
   - Frontend: http://localhost:3000 ✅
   - Backend: http://localhost:8000 ✅

2. **In your browser, visit:**
   ```
   http://localhost:3000
   ```

   You should see the Raven Shop Drawing interface with two panels:
   - **LEFT**: Parameter selection form
   - **RIGHT**: Drawing preview canvas

---

## 📋 Generate a Drawing

### Step 1️⃣: Select Frame Series

Look at the **LEFT PANEL** and find the first dropdown labeled **"Frame Series"**

**Available Options:**
- 135
- 150
- 4518
- 58
- 65
- 68
- 86
- Other

**Action:** Click the dropdown and select **"150"** (or any series)

```
┌─────────────────────────┐
│ Frame Series            │
│ ┌─────────────────────┐ │
│ │ 150        ▼       │ │
│ └─────────────────────┘ │
└─────────────────────────┘
```

---

### Step 2️⃣: Select Product Type

Find the dropdown labeled **"Product Type"**

**Available Options:**
- FIXED (single stationary pane)
- CASEMENT (side-opening window)
- SLIDER (horizontal sliding)
- DOOR (door frame)
- AWNING (top-opening)
- HOPPER (bottom-opening)
- DOUBLE_HUNG (vertical sliding)
- PICTURE (non-operating)
- CUSTOM

**Action:** Select **"CASEMENT"**

---

### Step 3️⃣: Set Dimensions

Find the **"Width (inches)"** and **"Height (inches)"** input fields

**Action:**
- **Width**: Enter **48** (must be 12-300)
- **Height**: Enter **60** (must be 12-300)

```
Width:  [48        ] inches
Height: [60        ] inches
```

---

### Step 4️⃣: Choose Glass Type

Find the dropdown labeled **"Glass Type"**

**Available Options:**
- Single Pane
- Dual Pane
- Low-E
- Tempered
- Laminated
- Frosted

**Action:** Select **"Dual Pane"**

---

### Step 5️⃣: Choose Frame Color

Find the dropdown labeled **"Frame Color"**

**Available Options:**
- White
- Bronze
- Black
- Tan
- Gray

**Action:** Select **"White"**

---

### Step 6️⃣: Optional - Add Grids

Find the checkbox labeled **"Add Grids/Muntins"**

**Action:** Check the box if you want grid lines in the drawing (optional)

```
☐ Add Grids/Muntins
```

---

### Step 7️⃣: Optional - Add Item Info

Find the text inputs for:
- **Item Number**: Your product SKU or ID
- **PO Number**: Purchase order number

**Action:** 
- Item Number: `CASE-150-48x60`
- PO Number: `PO-12345`

---

## 🎬 Step 8️⃣: Generate Drawing

Once you've filled in all parameters:

1. Look at the **RIGHT PANEL** - You should already see a preview updating!
2. Find the **"Generate Drawing"** button (bottom of LEFT PANEL)
3. Click **"Generate Drawing"**

```
┌──────────────────────┐
│  GENERATE DRAWING    │
│   (Blue Button)      │
└──────────────────────┘
```

---

## ✨ What You'll See

### On the RIGHT PANEL (Drawing Canvas):

Your CAD drawing will show:

```
┌─────────────────────────────────────┐
│  RAVEN CUSTOM GLASS - SHOP DRAWING   │ ← Title Block
├─────────────────────────────────────┤
│                                     │
│  Series: 150                        │ ← Drawing Info
│  Product: CASEMENT                  │
│  ┌─────────────────────────────┐    │
│  │                             │    │ ← Outer Frame
│  │    ┌─────────────────────┐  │    │
│  │    │                     │  │    │ ← Glass Opening
│  │    │    (Muntins here    │  │    │    (if grids enabled)
│  │    │     if enabled)     │  │    │
│  │    │                     │  │    │
│  │    └─────────────────────┘  │    │
│  │                             │    │
│  └─────────────────────────────┘    │
│                                     │
│         ↔ 48"                       │ ← Width Dimension
│                                     │
│  Item: CASE-150-48x60               │
│  Glass: Dual Pane                   │
│  Color: White                       │
└─────────────────────────────────────┘
↕
60"
```

---

## 💾 Export Your Drawing

Once the drawing is generated:

1. Look for the **"Export to PNG"** button (below the canvas)
2. Click it
3. The drawing will download as a PNG file to your downloads folder

```
📥 EXPORT TO PNG (Button)
```

---

## 🔄 Create Another Drawing

1. Change any parameter on the LEFT PANEL
2. The drawing on the RIGHT will update in **real-time**
3. Click **"Generate Drawing"** again
4. Or click **"Export to PNG"** to save it

---

## 📱 View Projects (Bonus)

At the top, click **"Projects"** in the navigation menu:
- See all your saved projects
- View project details (name, PO number, creation date)
- Future: Create/edit projects

---

## ✅ Complete Example

**Final Parameters:**

| Parameter | Value |
|-----------|-------|
| Frame Series | 150 |
| Product Type | CASEMENT |
| Width | 48 inches |
| Height | 60 inches |
| Glass Type | Dual Pane |
| Frame Color | White |
| Grids | ✓ Checked |
| Item Number | CASE-150-48x60 |
| PO Number | PO-12345 |

**Result:** A complete CAD shop drawing showing a 48"x60" casement window with dual pane glass, white frame, grid muntins, and all specifications in the title block.

---

## 🎯 What's Happening Behind the Scenes

1. **Frontend** (React) collects your parameters
2. **Vite dev server** runs on port 3000
3. Frontend sends parameters to **Backend API** (port 8000)
4. **FastAPI backend** processes the request
5. **Canvas renderer** draws the window based on specifications
6. **PNG export** saves the drawing to your computer

---

## 🐛 Troubleshooting

### Drawing not showing?
- ✓ Make sure you clicked "Generate Drawing" button
- ✓ Check browser console (F12 → Console tab) for errors
- ✓ Verify both backend and frontend are running

### Can't see the app?
- ✓ Try http://localhost:3000 in your browser
- ✓ Check both terminal windows show "running"
- ✓ If not, run the startup commands again

### Parameters not updating?
- ✓ Try refreshing the page (F5)
- ✓ Check browser console for JavaScript errors
- ✓ Restart the dev servers

---

## 🚀 Next Features (Coming Soon)

- ✅ Save drawings to database
- ✅ Load previous drawings
- ✅ PDF export
- ✅ Team collaboration
- ✅ Drawing templates
- ✅ Batch generation

---

**Happy drawing! 🎨**

Version 1.0.0 | December 26, 2025
