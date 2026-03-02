# test_upgrades.py
import requests
import json
from tabulate import tabulate

base_url = "http://localhost:8000/api/v1"

print("=" * 80)
print("🔍 TESTING UPGRADED MULTI-MODAL API")
print("=" * 80)

# Test 1: Health Check
print("\n📊 1. Health Check")
try:
    response = requests.get(f"{base_url}/health")
    print(f"   Status: {response.status_code}")
    print(f"   Response: {response.json()}")
except Exception as e:
    print(f"   ❌ Failed: {e}")

# Test 2: Text Detection (All Patterns)
print("\n📊 2. Testing Text Detection - All Patterns")
test_texts = [
    ("Forced Action", "You must create an account to continue"),
    ("Confirmshaming", "No thanks, I don't want to save money"),
    ("Hidden Costs", "Total: $49.99 plus processing fee"),
    ("Interface Interference", "Unsubscribe (tiny link at bottom)"),
    ("Obstruction", "Call during business hours to cancel"),
    ("Clean Design", "Welcome to our website")
]

text_results = []
for pattern_name, text in test_texts:
    try:
        response = requests.post(f"{base_url}/detect", 
                               json={"text": text})
        if response.status_code == 200:
            data = response.json()
            text_results.append([
                pattern_name,
                data['pattern_name'],
                f"{data['risk_score']['score']}",
                data['risk_score']['level']
            ])
            print(f"   ✅ {pattern_name:20} -> {data['pattern_name']:15} ({data['risk_score']['score']})")
        else:
            print(f"   ❌ {pattern_name}: Status {response.status_code}")
    except Exception as e:
        print(f"   ❌ {pattern_name}: {e}")

# Test 3: Solutions API
print("\n📊 3. Testing Solutions API")
test_patterns = [1, 2, 3, 4, 5]  # All pattern types
for pattern_type in test_patterns:
    try:
        response = requests.post(f"{base_url}/solutions",
                               json={"pattern_type": pattern_type})
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Pattern {pattern_type}: Got {len(data.get('solutions', []))} solutions")
            if data.get('solutions'):
                print(f"      First solution: {data['solutions'][0]['title'][:50]}...")
        else:
            print(f"   ❌ Pattern {pattern_type}: Status {response.status_code}")
    except Exception as e:
        print(f"   ❌ Pattern {pattern_type}: {e}")

# Test 4: Complete Analysis + Solutions
print("\n📊 4. Testing Complete Analysis + Solutions")
try:
    response = requests.post(f"{base_url}/analyze-with-solutions",
                           json={"text": "You must accept cookies to continue"})
    if response.status_code == 200:
        data = response.json()
        print("   ✅ Got complete analysis")
        print(f"      Pattern: {data['detection']['pattern_name']}")
        print(f"      Risk: {data['detection']['risk_score']['score']}")
        print(f"      Solutions: {len(data['solutions'].get('solutions', []))} available")
        if 'improvement_report' in data:
            print(f"      Report preview: {data['improvement_report'][:100]}...")
    else:
        print(f"   ❌ Status: {response.status_code}")
except Exception as e:
    print(f"   ❌ {e}")

# Test 5: Batch Processing
print("\n📊 5. Testing Batch Processing")
try:
    response = requests.post(f"{base_url}/detect/batch",
                           json={"texts": [t[1] for t in test_texts[:3]]})
    if response.status_code == 200:
        data = response.json()
        print(f"   ✅ Processed {data['total']} texts in batch")
        for i, result in enumerate(data['results']):
            if 'result' in result:
                print(f"      {i+1}. {result['result']['pattern_name']}")
    else:
        print(f"   ❌ Status: {response.status_code}")
except Exception as e:
    print(f"   ❌ {e}")

# Test 6: List Patterns
print("\n📊 6. Testing List Patterns Endpoint")
try:
    response = requests.get(f"{base_url}/patterns")
    if response.status_code == 200:
        data = response.json()
        print(f"   ✅ Found {len(data['patterns'])} patterns")
        for p in data['patterns'][:3]:  # Show first 3
            print(f"      {p['id']}: {p['name']} - {p['description'][:30]}...")
    else:
        print(f"   ❌ Status: {response.status_code}")
except Exception as e:
    print(f"   ❌ {e}")

print("\n" + "=" * 80)
print("📊 TEXT DETECTION SUMMARY")
print("=" * 80)
print(tabulate(text_results, headers=["Expected", "Detected", "Risk", "Level"]))
print("=" * 80)

print("\n✅ Testing Complete!")