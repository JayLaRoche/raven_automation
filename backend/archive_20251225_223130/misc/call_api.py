#!/usr/bin/env python3
"""Call the API endpoint to generate drawings"""
import requests
import json
import time

print("=" * 70)
print("CALLING API TO GENERATE DRAWINGS FROM Test_1")
print("=" * 70)
print()

api_url = "http://127.0.0.1:8000/api/drawings/Test_1/generate"

try:
    print(f"[1] Calling: POST {api_url}")
    response = requests.post(api_url, timeout=30)
    
    print(f"\n[2] Response Status: {response.status_code}")
    
    try:
        data = response.json()
        print(f"\n[3] Response:")
        print(json.dumps(data, indent=2))
    except:
        print(f"\n[3] Response:")
        print(response.text)
    
    if response.status_code == 200:
        print("\n" + "=" * 70)
        print("✓ PDF GENERATION SUCCESSFUL!")
        print("=" * 70)
    else:
        print("\n✗ Error: See response above")
        
except requests.exceptions.ConnectionError:
    print("\n✗ ERROR: Cannot connect to server at http://127.0.0.1:8000")
    print("\n[Solution] Start the FastAPI server first:")
    print("  cd c:\\Users\\larochej3\\Desktop\\raven-shop-automation\\backend")
    print("  python -m uvicorn main:app --reload")
    
except requests.exceptions.Timeout:
    print("\n✗ ERROR: Request timed out (server may be processing)")
    
except Exception as e:
    print(f"\n✗ ERROR: {e}")
