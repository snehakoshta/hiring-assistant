#!/usr/bin/env python3
"""
Debug API configuration
"""

import os
from dotenv import load_dotenv
import google.genai as genai

print("🔍 Debugging API Configuration...")
print("=" * 50)

# Load environment variables
load_dotenv('.env')

# Check API key loading
api_key = None

# Method 1: Environment variable
api_key_env = os.getenv("GOOGLE_API_KEY")
print(f"Environment variable: {'✅ Found' if api_key_env else '❌ Not found'}")
if api_key_env:
    print(f"   Value: {api_key_env[:10]}...")

# Method 2: Direct file reading
try:
    with open('.env', 'r', encoding='utf-8') as f:
        content = f.read().strip()
        if 'GOOGLE_API_KEY=' in content:
            api_key_file = content.split('GOOGLE_API_KEY=')[1].split('\n')[0].strip()
            print(f"Direct file read: ✅ Found")
            print(f"   Value: {api_key_file[:10]}...")
        else:
            print("Direct file read: ❌ Not found")
except Exception as e:
    print(f"Direct file read: ❌ Error - {e}")

# Use the found API key
api_key = api_key_env or api_key_file

if not api_key:
    print("\n❌ No API key found!")
    exit(1)

print(f"\n✅ Using API key: {api_key[:10]}...")

# Test API connection
try:
    print("\n🧪 Testing API connection...")
    client = genai.Client(api_key=api_key)
    
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents="Hello, this is a test message"
    )
    
    print("✅ API connection successful!")
    print(f"Response: {response.text[:100]}...")
    
except Exception as e:
    print(f"❌ API connection failed: {e}")
    print(f"Error type: {type(e).__name__}")
    
    # Check specific error types
    error_str = str(e).lower()
    if "api_key" in error_str or "401" in error_str or "403" in error_str:
        print("🔧 Suggestion: Check if API key is valid")
    elif "quota" in error_str or "billing" in error_str:
        print("🔧 Suggestion: Check Google Cloud billing/quota")
    elif "404" in error_str:
        print("🔧 Suggestion: Model name might be incorrect")
    else:
        print("🔧 Suggestion: Check internet connection and API service status")