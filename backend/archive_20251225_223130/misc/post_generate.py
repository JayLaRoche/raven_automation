#!/usr/bin/env python3
"""POST request to generate drawings"""
import requests
import json

url = "http://127.0.0.1:8000/api/drawings/Test_1/generate"

print("=" * 70)
print("SENDING POST REQUEST TO GENERATE DRAWINGS")
print("=" * 70)
print(f"\nURL: POST {url}\n")

try:
    response = requests.post(url, timeout=30)
    
    print(f"Status: {response.status_code}\n")
    
    try:
        data = response.json()
        print("Response:")
        print(json.dumps(data, indent=2))
    except:
        print("Response:")
        print(response.text)
    
    if response.status_code == 200:
        print("\n" + "=" * 70)
        print("✓ SUCCESS! PDFs GENERATED")
        print("=" * 70)
    
except Exception as e:
    print(f"Error: {e}")
