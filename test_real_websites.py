# test_real_websites.py
import requests
import json
from urllib.parse import urlparse
from tabulate import tabulate
import time

url = "http://localhost:8000/api/v1"

# Real websites to test
websites = [
    {
        "name": "Amazon",
        "url": "https://www.amazon.com",
        "note": "Checkout flow, prime signup"
    },
    {
        "name": "LinkedIn",
        "url": "https://www.linkedin.com/signup",
        "note": "Signup flow with premium upsell"
    },
    {
        "name": "Netflix",
        "url": "https://www.netflix.com/signup",
        "note": "Subscription plans with hidden terms"
    },
    {
        "name": "Booking.com",
        "url": "https://www.booking.com",
        "note": "Urgency messages, limited time deals"
    },
    {
        "name": "GitHub",
        "url": "https://github.com/join",
        "note": "Signup with plan selection"
    },
    {
        "name": "The New York Times",
        "url": "https://www.nytimes.com",
        "note": "Paywall, subscription prompts"
    },
    {
        "name": "Spotify",
        "url": "https://www.spotify.com/signup",
        "note": "Premium vs free comparison"
    },
    {
        "name": "Etsy",
        "url": "https://www.etsy.com",
        "note": "Checkout flow, shipping calculations"
    }
]

print("=" * 100)
print("🌐 TESTING DARK PATTERN DETECTOR ON REAL WEBSITES")
print("=" * 100)

results = []

for site in websites:
    print(f"\n🔍 Analyzing: {site['name']}")
    print(f"   URL: {site['url']}")
    print(f"   Note: {site['note']}")
    
    try:
        # Call your API
        start_time = time.time()
        response = requests.post(
            f"{url}/detect", 
            json={"url": site['url']},
            timeout=15  # 15 second timeout
        )
        elapsed = time.time() - start_time
        
        if response.status_code == 200:
            data = response.json()
            
            # Extract key info
            pattern = data['pattern_name']
            risk_score = data['risk_score']['score']
            risk_level = data['risk_score']['level']
            
            results.append([
                site['name'],
                pattern,
                f"{risk_score} ({risk_level})",
                f"{elapsed:.1f}s",
                data['explanation'][:60] + "..."
            ])
            
            # Print detailed info
            print(f"   ✅ Status: 200 OK")
            print(f"   📊 Pattern: {pattern}")
            print(f"   📈 Risk: {risk_score} - {risk_level}")
            print(f"   ⏱️  Time: {elapsed:.1f}s")
            print(f"   💡 Suggestion: {data['ethical_recommendation']['title']}")
            
            # Show a snippet of what was analyzed
            if 'url' in data:
                print(f"   📝 Text analyzed: {len(str(data))} chars")
                
        else:
            print(f"   ❌ Error: {response.status_code}")
            print(f"   Response: {response.text}")
            
    except requests.exceptions.Timeout:
        print(f"   ⏰ Timeout - Site took too long")
        results.append([site['name'], "TIMEOUT", "-", "-", "Request timed out"])
    except Exception as e:
        print(f"   ❌ Exception: {str(e)}")
        results.append([site['name'], "ERROR", "-", "-", str(e)[:50]])
    
    # Be polite to servers
    time.sleep(2)

# Print summary table
print("\n" + "=" * 100)
print("📊 REAL WEBSITE TEST SUMMARY")
print("=" * 100)
print(tabulate(results, 
               headers=["Website", "Pattern", "Risk", "Time", "Insight"],
               tablefmt="grid"))
print("=" * 100)