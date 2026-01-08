import streamlit as st
import os
import random
import time

# CSS Cache buster
CSS_VERSION = str(int(time.time()))

# Try to import Google GenAI, if not available, use fallback
try:
    from dotenv import load_dotenv
    import google.genai as genai
    
    # Advanced Features Imports
    from textblob import TextBlob
    from langdetect import detect
    import re
    
    # Import fallback system
    from fallback_responses import get_fallback_response
    
    # Load environment variables with explicit path
    load_dotenv('.env')
    
    # Get API key from environment or Streamlit secrets (prioritize Streamlit secrets for cloud deployment)
    api_key = None
    
    # First try Streamlit secrets (for Streamlit Cloud)
    try:
        api_key = st.secrets["GOOGLE_API_KEY"]
        print("✅ API key loaded from Streamlit secrets")
    except Exception as e:
        print(f"⚠️ Streamlit secrets not available: {e}")
        
        # Fallback to environment variable
        api_key = os.getenv("GOOGLE_API_KEY")
        if api_key:
            print("✅ API key loaded from environment variable")
        else:
            print("❌ No API key found in environment or secrets")
    
    # Configure GenAI if API key is available
    if api_key:
        genai.configure(api_key=api_key)
        print("✅ Google GenAI configured successfully")
    else:
        print("⚠️ Running without Google GenAI - using fallback responses")

except ImportError as e:
    print(f"⚠️ Import error: {e}")
    print("📦 Installing required packages...")
    
    # Fallback imports
    import random
    
    def analyze_sentiment(text):
        return "neutral"
    
    def detect_language(text):
        return "en"
    
    def translate(text, target="en"):
        return text

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="TalentScout Hiring Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ---------------- CUSTOM CSS ----------------
st.markdown(f"""
<style>
/* CSS Version: {CSS_VERSION} - Force reload */
/* Import Google Fonts */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

/* Global Styles with Background Image */
.stApp {{
    background: linear-gradient(135deg, rgba(15, 23, 42, 0.95) 0%, rgba(30, 41, 59, 0.9) 50%, rgba(51, 65, 85, 0.85) 100%),
                url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><defs><pattern id="grid" width="10" height="10" patternUnits="userSpaceOnUse"><path d="M 10 0 L 0 0 0 10" fill="none" stroke="%23334155" stroke-width="0.5" opacity="0.2"/></pattern></defs><rect width="100" height="100" fill="url(%23grid)"/></svg>'),
                radial-gradient(circle at 20% 80%, rgba(59, 130, 246, 0.15) 0%, transparent 50%),
                radial-gradient(circle at 80% 20%, rgba(168, 85, 247, 0.15) 0%, transparent 50%);
    background-attachment: fixed;
    background-size: cover, 50px 50px, 800px 800px, 600px 600px;
    font-family: 'Inter', sans-serif;
    min-height: 100vh;
}}

/* Hide Streamlit branding */
#MainMenu {{visibility: hidden;}}
footer {{visibility: hidden;}}
header {{visibility: hidden;}}

/* Main container with glass effect */
.main > div {{
    background: rgba(255, 255, 255, 0.1);
    backdrop-filter: blur(15px);
    border-radius: 20px;
    padding: 2.5rem;
    margin: 1rem;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3),
                0 4px 16px rgba(0, 0, 0, 0.2),
                inset 0 1px 0 rgba(255, 255, 255, 0.1);
    border: 1px solid rgba(255, 255, 255, 0.1);
    position: relative;
}}

/* Professional header styling */
.main-title {{
    text-align: center;
    background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 50%, #cbd5e0 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    font-size: 3rem;
    font-weight: 800;
    margin-bottom: 0.5rem;
    letter-spacing: -0.02em;
    position: relative;
}}

.main-title::after {{
    content: '';
    position: absolute;
    bottom: -10px;
    left: 50%;
    transform: translateX(-50%);
    width: 80px;
    height: 3px;
    background: linear-gradient(90deg, #3b82f6, #a855f7);
    border-radius: 2px;
}}

.subtitle {{
    text-align: center;
    color: #e2e8f0;
    font-size: 1.2rem;
    margin-bottom: 3rem;
    font-weight: 500;
    opacity: 0.9;
}}

/* Chat container */
.chat-container {{
    background: rgba(30, 41, 59, 0.8);
    border-radius: 20px;
    padding: 2rem;
    margin: 2rem 0;
    border: 1px solid rgba(148, 163, 184, 0.2);
    backdrop-filter: blur(10px);
    box-shadow: 0 8px 32px rgba(0,0,0,0.3);
}}

/* Welcome message */
.welcome-message {{
    background: rgba(59, 130, 246, 0.1);
    border-left: 4px solid #3b82f6;
    padding: 1.5rem;
    border-radius: 12px;
    margin-bottom: 2rem;
}}

.welcome-icon {{
    display: inline-block;
    background: #f97316;
    color: white;
    width: 40px;
    height: 40px;
    border-radius: 8px;
    text-align: center;
    line-height: 40px;
    font-size: 1.2rem;
    margin-right: 1rem;
    vertical-align: top;
}}

.welcome-