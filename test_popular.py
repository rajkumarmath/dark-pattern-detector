# test_popular.py
import requests
import time

url = "http://localhost:8000/api/v1"

# Popular websites to test
popular_sites = [
    "https://www.google.com",
    "https://www.youtube.com",
    "https://www.facebook.com",
    "https://www.amazon.com",
    "https://www.wikipedia.org",
    "https://www.reddit.com",
    "https://www.twitter.com",
    "https://www.instagram.com",
    "https://www.linkedin.com",
    "https://www.netflix.com"
]

print("🚀 Testing popular websites...")
print("-" * 50)

for site in popular_sites:
    print(f"\n🌐 {site}")
    try:
        start = time.time()
        response = requests.post(f"{url}/detect", json={"url": site}, timeout=10)
        elapsed = time.time() - start
        
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Pattern: {data['pattern_name']}")
            print(f"   📊 Risk: {data['risk_score']['score']} ({data['risk_score']['level']})")
            print(f"   ⏱️  Time: {elapsed:.1f}s")
        else:
            print(f"   ❌ Error: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Failed: {e}")
    
    time.sleep(1)  # Be polite