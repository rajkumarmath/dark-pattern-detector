# debug_demo.py
import requests
import traceback

url = "http://localhost:8000/api/v1/detect"

test_cases = [
    ("Forced Action", "You must create an account to view this product"),
    ("Confirmshaming", "No thanks, I don't want to save money on my purchase"),
    ("Hidden Costs", "Total: $49.99 plus processing and handling fees"),
    ("Interface Interference", "Click here to unsubscribe (tiny link at bottom)"),
    ("Obstruction", "Call during business hours to cancel your subscription"),
    ("Clean Design", "Would you like to sign up for our newsletter? Choose below.")
]

for name, text in test_cases:
    print(f"\n🔍 Testing: {name}")
    print(f"Text: {text[:50]}...")
    
    try:
        response = requests.post(url, json={"text": text})
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Success: {result['pattern_name']}")
        else:
            print(f"❌ Error Response: {response.text}")
    except Exception as e:
        print(f"💥 Exception: {str(e)}")