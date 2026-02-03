#!/usr/bin/env python3
"""
Debug PDF generation step by step
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from services.reference_shop_drawing_generator import ReferenceShopDrawingGenerator
import logging

# Enable debug logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

params = {
    "series": "86",
    "product_type": "FIXED",
    "width": 36,
    "height": 48,
    "glass_type": "Clear 5mm",
    "frame_color": "White",
    "configuration": "XX",
    "item_number": "P-001",
    "po_number": "PO-12345",
    "notes": "Test drawing"
}

print("[DEBUG] Creating generator...")
generator = ReferenceShopDrawingGenerator(db_connection=None, parameters=params)

print("[DEBUG] Generating PDF...")
try:
    pdf_buffer = generator.generate_pdf()
    print(f"[SUCCESS] PDF generated: {len(pdf_buffer.getvalue())} bytes")
except Exception as e:
    print(f"[ERROR] {type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()
