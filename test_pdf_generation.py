#!/usr/bin/env python3
"""
Test PDF generation and diagnose errors
"""
import requests
import json
import time

def test_pdf_generation():
    """Test the PDF generation endpoint"""
    
    base_url = "http://localhost:8000"
    endpoint = "/api/drawings/generate-pdf"
    
    # Test parameters (same as frontend would send)
    test_params = {
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
    
    print(f"[TEST] Sending PDF generation request...")
    print(f"[TEST] URL: {base_url}{endpoint}")
    print(f"[TEST] Parameters: {json.dumps(test_params, indent=2)}")
    print("-" * 60)
    
    try:
        response = requests.post(
            f"{base_url}{endpoint}",
            json=test_params,
            timeout=30
        )
        
        print(f"[RESPONSE] Status Code: {response.status_code}")
        print(f"[RESPONSE] Headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            print(f"[SUCCESS] PDF generated! Size: {len(response.content)} bytes")
            
            # Save PDF for inspection
            with open("test_drawing.pdf", "wb") as f:
                f.write(response.content)
            print(f"[SUCCESS] Saved to: test_drawing.pdf")
            
        else:
            print(f"[ERROR] Failed to generate PDF")
            try:
                error_data = response.json()
                print(f"[ERROR] Response: {json.dumps(error_data, indent=2)}")
            except:
                print(f"[ERROR] Response text: {response.text}")
                
    except requests.exceptions.Timeout:
        print("[ERROR] Request timeout - PDF generation took too long")
    except requests.exceptions.ConnectionError:
        print("[ERROR] Connection refused - Backend not running on port 8000")
    except Exception as e:
        print(f"[ERROR] Exception: {type(e).__name__}: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print("=" * 60)
    print("PDF GENERATION DIAGNOSTIC TEST")
    print("=" * 60)
    test_pdf_generation()
