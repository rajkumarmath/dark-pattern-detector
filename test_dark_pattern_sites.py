# test_dark_pattern_sites.py
import requests
import json
from tabulate import tabulate

url = "http://localhost:8000/api/v1"

# Sites known for dark patterns
test_sites = [
    {
        "name": "Amazon Prime Cancellation",
        "url": "https://www.amazon.com/gp/help/customer/display.html?nodeId=202076080",
        "expected": "Obstruction"
    },
    {
        "name": "LinkedIn Premium Upsell",
        "url": "https://www.linkedin.com/premium/products/",
        "expected": "Forced Action"
    },
    {
        "name": "Booking.com Deals",
        "url": "https://www.booking.com/deals.html",
        "expected": "Confirmshaming"
    },
    {
        "name": "NYT Subscription",
        "url": "https://www.nytimes.com/subscription",
        "expected": "Hidden Costs"
    },
    {
        "name": "GoDaddy Checkout",
        "url": "https://www.godaddy.com/checkout",
        "expected": "Interface Interference"
    }
]

print("=" * 100)
print("🎯 TESTING KNOWN DARK PATTERN SITES")
print("=" * 100)

for site in test_sites:
    print(f"\n🔍 Testing: {site['name']}")
    print(f"   URL: {site['url']}")
    print(f"   Expected: {site['expected']}")
    
    try:
        response = requests.post(
            f"{url}/detect", 
            json={"url": site['url']},
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            
            print(f"   ✅ Detected: {data['pattern_name']}")
            print(f"   📊 Risk: {data['risk_score']['score']} - {data['risk_score']['level']}")
            
            if data['pattern_name'] == site['expected'].lower().replace(' ', '_'):
                print(f"   ✅ MATCH! Correctly identified")
            else:
                print(f"   ⚠️  Different pattern detected")
                
            print(f"   💡 Suggestion: {data['ethical_recommendation']['title']}")
            
        else:
            print(f"   ❌ Error: {response.status_code}")
            
    except Exception as e:
        print(f"   ❌ Exception: {str(e)}")

print("\n" + "=" * 100)