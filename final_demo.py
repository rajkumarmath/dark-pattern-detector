import requests
from tabulate import tabulate

url = "http://localhost:8000/api/v1/detect"

test_cases = [
    ("Forced Action 1", "You must create an account to continue"),
    ("Forced Action 2", "Please login to view this content"),
    ("Confirmshaming 1", "No thanks, I don't want to save money"),
    ("Confirmshaming 2", "Skip and miss out on this deal"),
    ("Hidden Costs 1", "Total: $49.99 plus $5.99 processing fee"),
    ("Hidden Costs 2", "Additional convenience fee applies at checkout"),
    ("Interface Interference 1", "Unsubscribe (tiny link at bottom)"),
    ("Interface Interference 2", "Cancel subscription - hidden in settings"),
    ("Obstruction 1", "Call us during business hours to cancel"),
    ("Obstruction 2", "Please fill out this 10-page form"),
    ("Clean Design 1", "Would you like to sign up for our newsletter?"),
    ("Clean Design 2", "Choose your preferences below")
]

print("\n" + "="*100)
print("🎯 DARK PATTERN DETECTOR - COMPLETE TEST")
print("="*100)

results = []
for expected, text in test_cases:
    try:
        response = requests.post(url, json={"text": text})
        if response.status_code == 200:
            data = response.json()
            results.append([
                expected[:15],
                data['pattern_name'],
                f"{data['risk_score']['score']} ({data['risk_score']['level']})",
                text[:40] + "..."
            ])
            print(f"✅ {expected[:20]:<20} -> {data['pattern_name']:<15} ({data['risk_score']['score']})")
        else:
            print(f"❌ {expected} - Error: {response.status_code}")
    except Exception as e:
        print(f"❌ {expected} - Exception: {e}")

print("\n" + "="*100)
print("📊 SUMMARY TABLE")
print("="*100)
print(tabulate(results, headers=["Test Case", "Detected", "Risk Score", "Text Preview"]))