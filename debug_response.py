#!/usr/bin/env python3
"""
Debug why correct responses are not being generated
"""

import os
from dotenv import load_dotenv
import google.genai as genai

# Load environment variables
load_dotenv('.env')

# Get API key
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    with open('.env', 'r', encoding='utf-8') as f:
        content = f.read().strip()
        if 'GOOGLE_API_KEY=' in content:
            api_key = content.split('GOOGLE_API_KEY=')[1].split('\n')[0].strip()

print(f"✅ API Key: {api_key[:10]}...")

# Test the exact same logic as the app
client = genai.Client(api_key=api_key)

user_message = "happy"
context = ""

system_prompt = """You are a professional AI hiring assistant for TalentScout, a fictional recruitment agency. 
You help with recruitment processes, answer questions about jobs, career advice, and hiring procedures.
Be helpful, professional, and friendly. Keep responses concise but informative.

Advanced Features Active:
- Sentiment Analysis: Adapt tone based on user sentiment
- Multilingual Support: Respond in user's preferred language
- Personalization: Use context for personalized responses

Key guidelines:
- Stay focused on recruitment and career-related topics
- Provide accurate technical information when asked
- Be encouraging and supportive to candidates
- Maintain professional tone throughout
- If asked about non-recruitment topics, politely redirect to career/job-related discussions

Remember: You represent TalentScout recruitment agency."""

if context:
    system_prompt += f"\n\nContext: {context}"

full_prompt = f"{system_prompt}\n\nUser Question: {user_message}\n\nAssistant:"

print("🧪 Testing AI Response Generation...")
print(f"User message: '{user_message}'")
print("-" * 50)

# Test with multiple models like the app does
models_to_try = [
    'gemini-2.0-flash',      
    'gemini-flash-latest',   
    'gemini-2.0-flash-lite', 
    'gemini-2.5-flash'       
]

response = None
last_error = None

for model_name in models_to_try:
    print(f"\n🔍 Trying model: {model_name}")
    
    for attempt in range(3):
        try:
            print(f"   Attempt {attempt + 1}/3...")
            response = client.models.generate_content(
                model=model_name,
                contents=full_prompt
            )
            print(f"   ✅ SUCCESS!")
            print(f"   Response: {response.text}")
            break
        except Exception as e:
            error_str = str(e).lower()
            print(f"   ❌ Error: {str(e)}")
            last_error = e
            
            if "overloaded" in error_str or "503" in error_str or "unavailable" in error_str:
                print(f"   ⏳ Model overloaded, waiting {1 + attempt} seconds...")
                import time
                time.sleep(1 + attempt)
                continue
            elif "quota" in error_str or "429" in str(e):
                print(f"   💰 Quota exceeded for this model")
                break
            else:
                print(f"   🔄 Different error, trying next model...")
                break
    
    if response:
        print(f"\n🎉 Final success with model: {model_name}")
        break
else:
    print(f"\n❌ All models failed. Last error: {last_error}")
    print("\n💡 This is why the app shows fallback responses.")

print("\n" + "=" * 50)