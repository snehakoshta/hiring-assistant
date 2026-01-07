#!/usr/bin/env python3
"""
Test improved API handling with fallbacks
"""

import os
from dotenv import load_dotenv
import google.genai as genai
import time

print("🧪 Testing Improved API Handling...")
print("=" * 50)

# Load environment variables
load_dotenv('.env')

# Get API key
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    with open('.env', 'r', encoding='utf-8') as f:
        content = f.read().strip()
        if 'GOOGLE_API_KEY=' in content:
            api_key = content.split('GOOGLE_API_KEY=')[1].split('\n')[0].strip()

if not api_key:
    print("❌ No API key found!")
    exit(1)

print(f"✅ Using API key: {api_key[:10]}...")

# Test multiple models with retry logic
client = genai.Client(api_key=api_key)

models_to_try = [
    'gemini-2.5-flash',
    'gemini-2.0-flash',
    'gemini-flash-latest',
    'gemini-2.5-pro'
]

test_message = "Hello, I am very excited about this job opportunity!"

print(f"\n🔍 Testing message: '{test_message}'")
print("=" * 50)

response = None
last_error = None

for model_name in models_to_try:
    print(f"\n🧪 Trying model: {model_name}")
    
    for attempt in range(3):
        try:
            print(f"   Attempt {attempt + 1}/3...")
            response = client.models.generate_content(
                model=model_name,
                contents=test_message
            )
            print(f"   ✅ SUCCESS!")
            print(f"   Response: {response.text[:100]}...")
            break
        except Exception as e:
            error_str = str(e).lower()
            print(f"   ❌ Error: {str(e)[:80]}...")
            
            if "overloaded" in error_str or "503" in error_str or "unavailable" in error_str:
                print(f"   ⏳ Model overloaded, waiting {1 + attempt} seconds...")
                time.sleep(1 + attempt)
                continue
            else:
                print(f"   🔄 Different error, trying next model...")
                break
    
    if response:
        print(f"\n🎉 Final success with model: {model_name}")
        break
else:
    print(f"\n❌ All models failed. Last error: {last_error}")
    print("\n💡 This is when the app would show a helpful fallback message.")

print("\n" + "=" * 50)
print("✅ Test completed!")