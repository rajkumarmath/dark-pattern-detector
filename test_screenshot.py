# test_screenshot.py
import requests
import os

# Create a simple test image if you don't have one
def create_test_image():
    try:
        from PIL import Image, ImageDraw, ImageFont
        img = Image.new('RGB', (800, 600), color='white')
        d = ImageDraw.Draw(img)
        d.text((100, 100), "You must accept cookies", fill='black')
        d.text((100, 200), "No thanks, I don't want to save", fill='black')
        d.text((100, 300), "Total: $49.99 plus fees", fill='black')
        
        # Draw a tiny button
        d.rectangle([500, 150, 520, 170], outline='blue', fill='lightblue')
        d.text((505, 155), "OK", fill='black')
        
        img.save('test_screenshot.png')
        return 'test_screenshot.png'
    except Exception as e:
        print(f"Couldn't create test image: {e}")
        return None

print("🔍 Testing Screenshot Analysis")
print("=" * 50)

# Create or use existing screenshot
image_path = create_test_image()
if not image_path:
    image_path = input("Enter path to a screenshot: ").strip('"')

if os.path.exists(image_path):
    try:
        with open(image_path, 'rb') as f:
            files = {'file': (os.path.basename(image_path), f, 'image/png')}
            response = requests.post(
                "http://localhost:8000/api/v1/detect/screenshot",
                files=files
            )
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Screenshot analysis successful!")
            print(f"   Visual Risk: {data.get('overall_visual_risk', 'unknown')}")
            print(f"   Detected Patterns: {len(data.get('detected_patterns', []))}")
            
            if data.get('text_extracted'):
                print(f"   Extracted Text: {data['text_extracted'][:100]}...")
        else:
            print(f"❌ Failed: {response.status_code}")
            print(response.text)
    except Exception as e:
        print(f"❌ Error: {e}")
else:
    print(f"❌ Image not found: {image_path}")