# SHOP DRAWING UPGRADE - QUICK REFERENCE & ROADMAP

## 📋 IMPLEMENTATION CHECKLIST

### Phase 1: Core Layout (Week 1) ✓ PRIORITY
- [ ] Set up 3-column grid layout (30% / 45% / 25%)
- [ ] Create matplotlib figure with proper DPI (300)
- [ ] Configure axes for 8 distinct zones
- [ ] Test basic layout rendering

**Deliverable:** Blank layout template with correct proportions

---

### Phase 2: Static Elements (Week 1)
- [ ] Company header (logo, address, phone)
- [ ] Specification table structure (7 rows)
- [ ] Project information table (6 rows)
- [ ] "Drawn from inside view" label

**Deliverable:** Drawing with all static text and branding

---

### Phase 3: Elevation View (Week 1-2)
- [ ] Draw main frame rectangle (scaled to fit)
- [ ] Add panel divisions (for multi-panel units)
- [ ] Implement X/O notation system
- [ ] Calculate and display dimensions
- [ ] Add dimension lines with arrows

**Deliverable:** Functional elevation view with dimensions

---

### Phase 4: Dimension Lines (Week 2)
- [ ] Extension lines (0.5pt, extends beyond dimension line)
- [ ] Dimension lines with arrow heads
- [ ] Horizontal dimension helper function
- [ ] Vertical dimension helper function
- [ ] Proper CAD-style text placement

**Deliverable:** Professional dimension notation

---

### Phase 5: Cross-Sections (Week 2)
- [ ] Frame series 65 (hinged door) template
- [ ] Frame series 80 (fixed window) template
- [ ] Frame series 86 (casement) template
- [ ] Frame series 135 (slider) template
- [ ] Hardware details (hinges, locks)
- [ ] Thermal break visualization

**Deliverable:** Accurate technical cross-sections

---

### Phase 6: Person Silhouette (Week 2)
- [ ] Draw person figure (head, body, arms, legs)
- [ ] Scale to 5'8"-6'0" height
- [ ] Position relative to door/window
- [ ] Add curved swing arrow
- [ ] Direction indicators (left/right/in/out)

**Deliverable:** Scale reference with swing direction

---

### Phase 7: Plan View (Week 3)
- [ ] Horizontal section view
- [ ] Multiple frame assemblies
- [ ] Track systems (for sliders)
- [ ] Depth dimensions
- [ ] Panel overlap zones

**Deliverable:** Plan view showing frame depth

---

### Phase 8: Thumbnails (Week 3)
- [ ] Create 6-8 small window/door icons
- [ ] Single fixed window
- [ ] Casement window
- [ ] Slider window
- [ ] Hinged door
- [ ] French door
- [ ] Multi-panel slider
- [ ] Highlight current item type

**Deliverable:** Visual reference icons

---

### Phase 9: Data Integration (Week 3)
- [ ] Parse Google Sheets data
- [ ] Map fields to WindowDoorItem class
- [ ] Populate specification table
- [ ] Populate project information table
- [ ] Determine correct drawing template
- [ ] Handle edge cases (missing data)

**Deliverable:** Fully automated data flow

---

### Phase 10: Polish & Testing (Week 4)
- [ ] Line weight differentiation
- [ ] Color consistency
- [ ] Text legibility check
- [ ] Layout spacing refinement
- [ ] Test all window types
- [ ] Test all door types
- [ ] Edge case validation
- [ ] Client review & feedback

**Deliverable:** Production-ready system

---

## 🎯 CRITICAL SUCCESS FACTORS

### Must-Have Features:
1. ✅ **Exact layout match** to reference example
2. ✅ **CAD-standard dimensions** (arrows, extension lines, text)
3. ✅ **Accurate cross-sections** matching frame series
4. ✅ **Person silhouette** for scale (5'8"-6'0")
5. ✅ **Swing direction arrows** for doors/casements
6. ✅ **Complete specification table** from Google Sheets
7. ✅ **Professional branding** (logo, contact info)
8. ✅ **Print-ready quality** (300 DPI)

### Nice-to-Have Enhancements:
- Color-coded panel types
- Automated thumbnail generation
- Dynamic legend for X/O notation
- Multi-page support for complex units
- Batch generation for entire projects

---

## 🚀 QUICK START GUIDE

### 1. Set Up Environment
```bash
pip install matplotlib reportlab numpy pandas
pip install google-auth google-auth-oauthlib google-api-python-client
```

### 2. Use Starter Template
Copy `shop_drawing_generator.py` and modify:
- Company branding constants
- Google Sheets connection
- Cross-section templates for your specific frame series

### 3. Test with Sample Data
```python
from shop_drawing_generator import WindowDoorItem, generate_shop_drawing

# Create test item
test_data = {
    'item_id': 'W001',
    'width': 72,
    'height': 60,
    'type': 'DOUBLE CASEMENT',
    # ... more fields
}

item = WindowDoorItem(test_data)
generate_shop_drawing(item, 'test_output.pdf')
```

### 4. Integrate with Google Sheets
```python
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

# Fetch data from sheet
creds = Credentials.from_service_account_file('credentials.json')
service = build('sheets', 'v4', credentials=creds)

result = service.spreadsheets().values().get(
    spreadsheetId='YOUR_SHEET_ID',
    range='Windows!A:Z'
).execute()

rows = result.get('values', [])
```

---

## ⚠️ COMMON PITFALLS TO AVOID

### Layout Issues:
- ❌ Don't use fixed pixel coordinates - use normalized 0-100 scale
- ❌ Don't forget to turn off axes (ax.axis('off'))
- ❌ Don't overlap text or drawing elements
- ✅ Use GridSpec for proper layout management

### Dimension Lines:
- ❌ Don't use simple lines without arrows
- ❌ Don't center text below dimension line (should be above)
- ❌ Don't skip extension lines
- ✅ Follow CAD standards exactly

### Cross-Sections:
- ❌ Don't use placeholder rectangles in production
- ❌ Don't mix up frame series templates
- ❌ Don't forget thermal break visualization
- ✅ Match technical specifications from reference PDF

### Data Handling:
- ❌ Don't hardcode sample data in production
- ❌ Don't skip validation of Google Sheets data
- ❌ Don't ignore missing or malformed fields
- ✅ Implement robust error handling

### Scale & Proportions:
- ❌ Don't make person silhouette wrong height
- ❌ Don't draw elevation views at incorrect scale
- ❌ Don't forget to maintain aspect ratio
- ✅ Calculate proper scaling for each item size

---

## 📊 TESTING STRATEGY

### Unit Tests:
- [ ] Dimension line function accuracy
- [ ] Cross-section rendering for each series
- [ ] Person silhouette proportions
- [ ] Swing arrow placement
- [ ] Data parsing from Google Sheets

### Integration Tests:
- [ ] End-to-end generation from sheet to PDF
- [ ] Batch processing multiple items
- [ ] Error handling for missing data
- [ ] Edge cases (very large/small items)

### Visual Inspection:
- [ ] Compare output to reference example side-by-side
- [ ] Verify all text is legible at print size
- [ ] Check dimension accuracy with ruler
- [ ] Ensure professional appearance
- [ ] Client approval on sample drawings

### Test Cases:
1. **Small Fixed Window**: 18" x 24", Series 80
2. **Standard Casement**: 36" x 60", Series 86
3. **Large Double Casement**: 72" x 72", Series 86
4. **Single Hinged Door**: 36" x 108", Series 65
5. **Double French Door**: 72" x 108", Series 65
6. **2-Panel Slider**: 96" x 108", Series 135
7. **4-Panel Slider**: 240" x 108", MD100H

---

## 🔍 QUALITY ASSURANCE CHECKLIST

Before client demo:
- [ ] All drawings match reference format exactly
- [ ] Dimensions are accurate to input data
- [ ] Cross-sections match specified frame series
- [ ] Person silhouette is proportional and visible
- [ ] Swing arrows indicate correct direction
- [ ] Specification tables are complete
- [ ] Company branding is correct
- [ ] Project information is populated
- [ ] PDFs are print-ready (300 DPI)
- [ ] File naming follows convention
- [ ] No placeholder or dummy text
- [ ] All line weights are differentiated
- [ ] Text is legible and properly aligned

---

## 📞 CLIENT COMMUNICATION

### Demo Preparation:
1. Generate 5-10 sample drawings covering:
   - Different window types
   - Different door types
   - Various sizes (small to very large)
   - Different frame series

2. Prepare comparison:
   - Before: Current simple drawings
   - After: New professional format
   - Highlight key improvements

3. Have backup plan:
   - Screen share capability tested
   - PDF viewer ready
   - Ability to show source data in Google Sheets

### Key Talking Points:
- ✓ Matches professional CAD drawing standards
- ✓ Shows all necessary technical details
- ✓ Includes scale reference (person silhouette)
- ✓ Ready for fabrication shop use
- ✓ Automated from Google Sheets data
- ✓ Print-ready quality (300 DPI)

### Questions to Ask Client:
1. Does this match your expectations?
2. Are there any missing details?
3. Are the cross-sections accurate for your frame series?
4. Is the specification table complete?
5. Should we adjust any dimensions or scales?
6. Are there additional views needed?

---

## 📈 PERFORMANCE METRICS

### Target Performance:
- Generation time: < 5 seconds per drawing
- File size: 200-500 KB per PDF
- Quality: 300 DPI (print-ready)
- Accuracy: 100% data match to Google Sheets

### Monitoring:
- Track generation time for each drawing
- Monitor file sizes for optimization
- Log any errors or warnings
- Collect client feedback

---

## 🔄 ITERATION & IMPROVEMENT

### After Phase 1 Demo:
1. Gather client feedback
2. Prioritize requested changes
3. Update technical specifications
4. Re-test with new requirements

### Continuous Improvement:
- Add more frame series templates
- Enhance thumbnail library
- Optimize rendering performance
- Improve error handling
- Add validation rules

---

## 🎓 LEARNING RESOURCES

### Matplotlib References:
- Official docs: https://matplotlib.org/
- Grid layouts: GridSpec documentation
- Patches: Rectangle, Circle, Arc, Arrow
- Text formatting: fontsize, fontweight, alignment

### CAD Standards:
- ANSI Y14.5 (Dimensioning standards)
- Architectural drawing conventions
- Technical drawing best practices

### Python Libraries:
- matplotlib: Drawing and rendering
- reportlab: Alternative PDF generation
- google-api-python-client: Google Sheets API
- pandas: Data manipulation

---

## 📝 DOCUMENTATION UPDATES

As you implement:
- Document any deviations from spec (and why)
- Update helper function signatures if changed
- Add comments for complex calculations
- Create docstrings for all functions
- Maintain changelog of major changes

---

## 🏁 DEFINITION OF DONE

Phase 1 is complete when:
1. ✅ Layout matches reference example
2. ✅ All static elements are rendered
3. ✅ Elevation view shows correct dimensions
4. ✅ Specification table is populated
5. ✅ Company header is formatted
6. ✅ Project info table is complete
7. ✅ PDF exports at 300 DPI
8. ✅ Client approves Phase 1 demo

Full project is complete when:
1. ✅ All 10 phases are implemented
2. ✅ All test cases pass
3. ✅ Client approves final output
4. ✅ System is deployed and accessible
5. ✅ Documentation is complete
6. ✅ Training is provided (if needed)
7. ✅ Final payment is received

---

## 🆘 TROUBLESHOOTING

### Common Issues:

**Issue**: Text overlapping or cut off
**Solution**: Adjust text positions, reduce font size, or expand zone

**Issue**: Dimensions not aligned
**Solution**: Check extension line offsets, verify arrow positions

**Issue**: Cross-section doesn't match series
**Solution**: Verify series mapping, check reference PDF details

**Issue**: Person silhouette wrong size
**Solution**: Recalculate scale factor, verify height parameter

**Issue**: Layout doesn't match reference
**Solution**: Verify GridSpec ratios (3, 4.5, 2.5) and heights (2, 3, 2)

**Issue**: PDF quality is low
**Solution**: Ensure DPI=300, use bbox_inches='tight'

**Issue**: Google Sheets data not loading
**Solution**: Check service account permissions, verify sheet ID

---

## 🎉 SUCCESS INDICATORS

You know it's working when:
- Client says "This looks professional!"
- Fabrication shop can use drawings without questions
- Sales team can generate drawings during customer meetings
- No manual editing needed after generation
- Drawings print clearly at full size
- All data flows automatically from Google Sheets

---

**Version:** 1.0  
**Last Updated:** December 24, 2024  
**Next Review:** After Phase 1 Demo  
**Owner:** Jeremiah (Project Lead)  
**Client:** Raven Custom Glass (Zion)
