#!/usr/bin/env python3
"""Check Google Sheet structure and columns"""
import sys
import os

sys.path.insert(0, '.')
from dotenv import load_dotenv

load_dotenv()

from services.google_sheets_services import get_sheets_service

print("=" * 70)
print("GOOGLE SHEET STRUCTURE ANALYSIS")
print("=" * 70)

service = get_sheets_service()
worksheet = service.get_worksheet()

print(f"\nSheet: '{worksheet.title}'")
print(f"Dimensions: {worksheet.row_count} rows × {worksheet.col_count} columns")

# Get the header row
header = worksheet.row_values(1)
print(f"\nHeader Row ({len(header)} columns):")
for i, col in enumerate(header[:20], 1):  # Show first 20
    print(f"  {i}. {repr(col)}")

# Check for duplicates
print(f"\nChecking for duplicate headers...")
seen = {}
duplicates = []
for i, col in enumerate(header, 1):
    if col in seen:
        duplicates.append((col, seen[col], i))
    else:
        seen[col] = i

if duplicates:
    print(f"  Found {len(duplicates)} duplicate(s):")
    for col_name, first_pos, second_pos in duplicates[:10]:
        print(f"    - '{col_name}': columns {first_pos} and {second_pos}")
else:
    print(f"  ✓ No duplicates found!")

# Try to read first row of data with raw values
print(f"\nFirst data row (raw values):")
first_data = worksheet.row_values(2)
for i, val in enumerate(first_data[:10], 1):
    print(f"  Col {i}: {repr(val)}")

print(f"\n" + "=" * 70)
