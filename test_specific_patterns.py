# test_specific_patterns.py
import requests
from tabulate import tabulate

url = "http://localhost:8000/api/v1"

# Real-world dark pattern examples
test_cases = [
    {
        "name": "Forced Account Creation",
        "text": "You must create a Walmart account to complete your purchase",
        "site": "Walmart"
    },
    {
        "name": "Confirmshaming",
        "text": "No thanks, I don't want to save 15% on my order",
        "site": "Various retailers"
    },
    {
        "name": "Hidden Fees",
        "text": "Your total is $29.99 plus $4.99 processing fee and $3.50 service fee",
        "site": "Ticketmaster"
    },
    {
        "name": "Interface Interference",
        "text": "Unsubscribe from emails (link at bottom of email in 6pt font)",
        "site": "Newsletters"
    },
    {
        "name": "Obstruction",
        "text": "To delete your account, please call us at 1-800-XXX-XXXX Mon-Fri 9-5",
        "site": "Gym memberships"
    },
    {
        "name": "Pre-selected Options",
        "text": "Yes, I want to receive promotional emails (pre-checked)",
        "site": "Airline booking"
    },
    {
        "name": "Urgency",
        "text": "Only 2 rooms left at this price! Book now before they're gone!",
        "site": "Hotel booking"
    },
    {
        "name": "Forced Continuity",
        "text": "Your free trial will automatically convert to paid subscription",
        "site": "Software as a Service"
    }
]

print("=" * 100)
print("🎯 TESTING REAL-WORLD DARK PATTERN EXAMPLES")
print("=" * 100)

results = []
for case in test_cases:
    print(f"\n🔍 Testing: {case['name']}")
    print(f"   Example from: {case['site']}")
    print(f"   Text: {case['text'][:80]}...")
    
    try:
        response = requests.post(f"{url}/detect", json={"text": case['text']})
        
        if response.status_code == 200:
            data = response.json()
            
            results.append([
                case['name'],
                case['site'],
                data['pattern_name'],
                f"{data['risk_score']['score']} ({data['risk_score']['level']})",
                data['ethical_recommendation']['title'][:40] + "..."
            ])
            
            print(f"   ✅ Pattern: {data['pattern_name']}")
            print(f"   📊 Risk: {data['risk_score']['score']} - {data['risk_score']['level']}")
            print(f"   💡 Suggestion: {data['ethical_recommendation']['title']}")
            
        else:
            print(f"   ❌ Error: {response.status_code}")
            
    except Exception as e:
        print(f"   ❌ Exception: {e}")

print("\n" + "=" * 100)
print("📊 REAL-WORLD EXAMPLES SUMMARY")
print("=" * 100)
print(tabulate(results, 
               headers=["Pattern Type", "Found In", "Detected", "Risk", "Solution"],
               tablefmt="grid"))
print("=" * 100)