# demo_showcase.py
import requests
import json
from tabulate import tabulate

url = "http://localhost:8000/api/v1/detect"

# Test cases showing all pattern types
test_cases = [
    {
        "name": "🛒 Forced Action",
        "text": "You must create an account to view this product"
    },
    {
        "name": "😔 Confirmshaming",
        "text": "No thanks, I don't want to save money on my purchase"
    },
    {
        "name": "💰 Hidden Costs",
        "text": "Total: $49.99 plus processing and handling fees"
    },
    {
        "name": "👁️ Interface Interference",
        "text": "Click here to unsubscribe (tiny link at bottom)"
    },
    {
        "name": "🚧 Obstruction",
        "text": "Call during business hours to cancel your subscription"
    },
    {
        "name": "✅ Clean Design",
        "text": "Would you like to sign up for our newsletter? Choose below."
    }
]

print("=" * 80)
print("🚀 DARK PATTERN DETECTOR - DEMO SHOWCASE")
print("=" * 80)

results = []
for case in test_cases:
    print(f"\n🔍 Testing: {case['name']}")
    print(f"   Text: {case['text'][:50]}...")
    
    response = requests.post(url, json={"text": case['text']})
    
    if response.status_code == 200:
        result = response.json()
        results.append([
            case['name'],
            result['pattern_name'],
            f"{result['risk_score']['score']} ({result['risk_score']['level']})",
            result['ethical_recommendation']['title'][:30] + "..."
        ])
        
        print(f"   ✅ Pattern: {result['pattern_name']}")
        print(f"   📊 Risk: {result['risk_score']['score']} - {result['risk_score']['level']}")
        print(f"   💡 Fix: {result['ethical_recommendation']['title']}")
    else:
        print(f"   ❌ Error: {response.status_code}")

print("\n" + "=" * 80)
print("📊 SUMMARY TABLE")
print("=" * 80)
print(tabulate(results, headers=["Test Case", "Pattern", "Risk Score", "Suggestion"]))