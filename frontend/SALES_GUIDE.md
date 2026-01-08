# 🎨 Raven Custom Glass - Sales Presentation Generator

**Version:** 2.0.0 - Professional Sales App  
**Status:** ✅ Production Ready  
**Target User:** Sales Representatives + Customer Meetings  
**Key Feature:** Generate professional shop drawings in ~3 seconds

---

## 🚀 QUICK START

### 1. **Open the App**
   Visit: **http://localhost:3000**

### 2. **The Layout**
   ```
   ┌─────────────────────────────────────────────────┐
   │  HEADER: Raven Logo | Presentation Mode | Export │
   ├──────────────────┬──────────────────────────────┤
   │                  │                              │
   │  PARAMETERS      │     DRAWING PREVIEW          │
   │  (Left - 30%)    │     (Right - 70%)            │
   │                  │                              │
   │  • Frame Series  │  [Professional Technical    │
   │  • Type          │   Drawing with Dimensions]  │
   │  • Dimensions    │                              │
   │  • Glass Type    │  Status: ✅ Ready           │
   │  • Color         │                              │
   │                  │                              │
   └──────────────────┴──────────────────────────────┘
   ```

---

## 📋 HOW TO USE - Sales Meeting Workflow

### **Scenario: Customer in Conference Room**

1. **Open App on Laptop/Tablet**
   - Already loaded at http://localhost:3000
   - Professional Raven branding visible

2. **Customer Says: "I want a 48\" × 60\" window"**
   - Height field shows: `60`
   - Width field shows: `48`
   - ✅ Auto-generates drawing in 2-3 seconds
   - Drawing appears on right side

3. **Customer Asks: "Can we make it bigger? Maybe 72\" wide?"**
   - Click **+** button next to Width (or type `72`)
   - ⚡ Auto-update: Drawing regenerates in 2-3 seconds
   - Drawing smoothly fades to new version
   - No refresh, no lag

4. **Customer: "What if we use the casement style with low-E glass?"**
   - Select **Series 86** (casement)
   - Select **Low-E** glass type
   - Drawing updates immediately
   - Professional title block shows new specs

5. **Customer: "Looks good! Can you email this to me?"**
   - Click **💾 Export** button
   - File downloads as: `PO-2024-001_W-001_2025-12-26.png`
   - Ready to email or print

6. **Next Window in Project?**
   - Enter new Item Number: `W-002`
   - Adjust parameters again
   - Repeat for all windows

---

## 🎯 FEATURES EXPLAINED

### **Smart Parameter Panel (Left Side)**

#### **Quick Presets** - 1-Click Configurations
```
[Standard Bedroom]  → 48×60", Series 86, Double Casement
[Patio Door]        → 96×108", Series 135, 2-Panel Slider
[Entry Door]        → 36×108", Series 65, Hinged Door
```
Perfect for common window types - saves time!

#### **Frame Series Selector** - Card-Based with Icons
```
🪟 86    🪟 80    🚪 65    📐 135
Casement  Fixed   Hinged   Slider
```
Click any card to select. Visual, intuitive, fast.

#### **Dimension Controls** - Touch Friendly
```
Width:  [−] [48] [+]  inches
Height: [−] [60] [+]  inches
```
- **Large buttons** (44px min) - easy on tablets
- **+/− buttons** - quick adjustments without typing
- **Direct input** - type exact values if preferred

#### **Auto-Generate Toggle** - Real-Time Updates
```
⚡ Auto-Generate: [ON]
```
- **ON** (default): Drawing updates 800ms after last change
- **OFF**: Click "🚀 Generate Now" for manual control
- Perfect for discussing options without constant updates

---

### **Instant Drawing Display (Right Side)**

#### **Professional Technical Drawing**
Shows:
- Outer frame (black lines)
- Inner glass opening
- Dimensions (width/height in inches)
- Title block with specs:
  - Company: RAVEN CUSTOM GLASS
  - Series, Product Type, Item #
  - Glass Type, Frame Color

#### **Smooth Transitions**
- Drawing fades smoothly when updating
- Loading indicator shows "Generating drawing... ~3 seconds"
- Old drawing visible during regeneration (no blank flashes)

#### **Export Options**
```
[💾 Export PNG]  → Downloads to computer
```
Smart filename: `PO-NUMBER_ITEM-NUMBER_DATE.png`

---

## ⌨️ KEYBOARD SHORTCUTS - Power User Features

```
Cmd+G (or Ctrl+G)  → Generate Now (skip debounce)
Cmd+E (or Ctrl+E)  → Export Drawing
Cmd+P (or Ctrl+P)  → Enter Presentation Mode
```

### **Presentation Mode** - Full Screen for Projector
```
[ESC or Click Exit] → Return to normal view
```
Perfect for:
- Projecting drawing to customers
- Large screen presentations
- Showing on customer's TV/projector

---

## 💡 SALES TIPS & TRICKS

### **Tip 1: Pre-Load Favorite Configurations**
Save time by remembering:
- Series 86 = Most common (windows)
- Series 135 = Patio doors
- Dual Pane = Standard glass choice

### **Tip 2: Use Quick Presets for Initial Setup**
Click [Standard Bedroom] instead of entering all parameters manually.

### **Tip 3: Make Small Adjustments with +/− Buttons**
Don't retype whole numbers - just click + or − to adjust by 1 inch.

### **Tip 4: Toggle Auto-Update OFF for Discussion**
If customer is debating options, turn OFF auto-update so you can set multiple parameters before showing drawing.

### **Tip 5: Screenshot + Email Workflow**
1. Export PNG
2. Email to customer immediately
3. Customer has reference while thinking
4. No manual CAD drafting needed

---

## ✅ SUCCESS CHECKLIST - Ready for Customer Meeting?

- [ ] Both servers running (Backend :8000, Frontend :3000)
- [ ] App loads at http://localhost:3000
- [ ] Can adjust parameters smoothly
- [ ] Drawing updates in ~3 seconds
- [ ] Can export PNG
- [ ] Presentation mode works (Cmd+P)
- [ ] Touch-friendly controls are responsive
- [ ] Professional appearance suitable for customer

---

## 🎨 DESIGN FEATURES

**Color Palette:**
- Primary Blue: `#1e40af` - Trustworthy, professional
- Success Green: `#10b981` - Positive feedback
- Clean background: `#f8fafc` - Modern, minimal

**Typography:**
- Headers: Bold, clean (16px-20px)
- Body: Readable (14px-16px)
- Dimensions in drawing: Large, clear (24px presentation mode)

**Responsive Design:**
- **Laptop/Desktop** - Full 2-column layout
- **iPad Pro/Tablets** - Touch-optimized, large buttons
- **Minimum touch target** - 44px × 44px (Apple recommendation)

---

## ⚙️ TECHNICAL DETAILS

### **How Auto-Generation Works**
1. User changes parameter
2. App waits 800ms (to avoid too many API calls)
3. Sends request to backend: `/api/drawings/generate`
4. Backend returns drawing data in ~3 seconds
5. Frontend smoothly fades to new drawing

### **Drawing Canvas**
- 800×1000px native canvas
- Rendered with HTML5 Canvas API (no external libraries)
- Professional cross-sections and title block
- Exports to PNG immediately

### **State Management**
- Zustand stores (lightweight, fast)
- No Redux complexity
- Drawing params + Presentation mode
- Instant updates across components

---

## 🔧 TROUBLESHOOTING

### **Drawing doesn't appear**
1. Check console (F12 → Console) for errors
2. Verify backend is running on :8000
3. Ensure all parameters are filled in
4. Try Cmd+G to generate now

### **Auto-update is slow**
1. It's normal to take 3-5 seconds total
2. This includes:
   - 800ms debounce
   - ~3 seconds backend processing
   - Network latency
3. Presentation is smooth - not the delay itself

### **Export button disabled**
- Drawing must be generated first
- Wait for loading spinner to disappear
- Then export should work

### **Touchscreen not responding**
- Buttons are 44px minimum (should work on iPad)
- Try larger movements/taps
- Check if browser is in fullscreen mode

---

## 📞 SUPPORT

**For Issues:**
1. Check this guide first
2. Restart app (refresh browser: F5)
3. Restart servers if needed
4. Check browser console (F12) for error messages

**Performance Notes:**
- First load may take 2-3 seconds
- Subsequent drawings faster (~2 seconds)
- Caching optimizes for speed

---

## 🚀 THE RAVEN DIFFERENCE

**Before:** Manual CAD drafting, customer emails back and forth, days of turnaround  
**After:** Real-time design, instant approval, professional drawings on the spot

**This is the future of sales. You're equipped with the best tool.**

---

**Happy Selling! 🎉**

*Raven Custom Glass - Where speed meets professionalism*
