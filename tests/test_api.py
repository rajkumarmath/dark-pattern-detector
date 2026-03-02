# tests/test_api.py
import requests
import json

def test_detection_api():
    """Test the detection endpoint"""
    base_url = "http://localhost:8000/api/v1"
    
    # Test cases
    test_cases = [
        {
            "name": "Forced Action",
            "text": "You must accept cookies to continue browsing"
        },
        {
            "name": "Confirmshaming",
            "text": "No thanks, I don't want to save money"
        },
        {
            "name": "Hidden Costs",
            "text": "Total: $49.99 plus handling fee"
        },
        {
            "name": "No Pattern",
            "text": "Welcome to our website. Feel free to browse."
        }
    ]
    
    for case in test_cases:
        print(f"\n🔍 Testing: {case['name']}")
        response = requests.post(
            f"{base_url}/detect",
            json={"text": case['text']}
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Pattern: {result['pattern_name']} (type {result['pattern_type']})")
            print(f"📊 Risk: {result['risk_score']['score']} - {result['risk_score']['level']}")
            print(f"💡 Suggestion: {result['ethical_recommendation']['title']}")
        else:
            print(f"❌ Error: {response.status_code}")
            print(response.text)

if __name__ == "__main__":
    test_detection_api()