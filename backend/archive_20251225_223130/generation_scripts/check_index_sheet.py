#!/usr/bin/env python3
"""Check !!Index sheet for compatibility"""
import sys
sys.path.insert(0, '.')
from dotenv import load_dotenv
import os
load_dotenv()

from services.google_sheets_services import GoogleSheetsService

service = GoogleSheetsService()

# Check the !!Index sheet
ws = service.get_worksheet('!!Index')
print(f"Sheet: '{ws.title}'")

header = ws.row_values(1)
print(f"\nHeader ({len(header)} cols):")
for i, h in enumerate(header[:10], 1):
    print(f"  {i}. {repr(h)}")

# Check for duplicates
seen = {}
dups = []
for i, col in enumerate(header, 1):
    if col and col in seen:
        dups.append(f"{repr(col)} at columns {seen[col]} and {i}")
    if col:
        seen[col] = i

if dups:
    print(f"\nDuplicate headers: {dups}")
else:
    print(f"\n✓ No duplicate headers!")

# Try to get records
try:
    records = ws.get_all_records()
    print(f"\n✓ Successfully read {len(records)} records!")
    if records:
        first = records[0]
        print(f"\nFirst record keys: {list(first.keys())[:5]}")
except Exception as e:
    print(f"\n✗ Error: {e}")
