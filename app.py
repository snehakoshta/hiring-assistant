import streamlit as st
import os
import random
import time

# CSS Cache buster
CSS_VERSION = str(int(time.time()))

# Try to import Google GenAI, if not available, use fallback
try:
    from dotenv import load_dotenv
    import google.generativeai as genai
    
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
/* CSS Version: {CSS_VERSION} */

/* Import Google Fonts */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

/* Global Styles */
.stApp {{
    background:
        linear-gradient(135deg, rgba(15, 23, 42, 0.95) 0%, rgba(30, 41, 59, 0.9) 50%, rgba(51, 65, 85, 0.85) 100%),
        radial-gradient(circle at 20% 80%, rgba(59, 130, 246, 0.15) 0%, transparent 50%),
        radial-gradient(circle at 80% 20%, rgba(168, 85, 247, 0.15) 0%, transparent 50%);
    background-attachment: fixed;
    font-family: 'Inter', sans-serif;
    min-height: 100vh;
}}

/* Hide Streamlit branding */
#MainMenu {{ visibility: hidden; }}
footer {{ visibility: hidden; }}
header {{ visibility: hidden; }}

/* Main glass container */
.main > div {{
    background: rgba(255, 255, 255, 0.1);
    backdrop-filter: blur(15px);
    border-radius: 20px;
    padding: 2.5rem;
    margin: 1rem;
    box-shadow: 0 8px 32px rgba(0,0,0,0.3);
    border: 1px solid rgba(255,255,255,0.1);
}}

/* Titles */
.main-title {{
    text-align: center;
    background: linear-gradient(135deg, #f8fafc, #cbd5e0);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    font-size: 3rem;
    font-weight: 800;
}}

.subtitle {{
    text-align: center;
    color: #e2e8f0;
    font-size: 1.2rem;
    margin-bottom: 3rem;
}}

/* Chat messages */
.stChatMessage {{
    padding: 1.8rem;
    border-radius: 16px;
    margin-bottom: 1.5rem;
    backdrop-filter: blur(6px);
    border: 1px solid rgba(255,255,255,0.25);
}}

.stChatMessage * {{
    color: #ffffff !important;
}}

.stChatMessage[data-testid="user-message"] {{
    background: rgba(59, 130, 246, 0.25);
    margin-left: 3rem;
}}

.stChatMessage[data-testid="assistant-message"] {{
    background: rgba(168, 85, 247, 0.25);
    margin-right: 3rem;
}}

/* Chat input */
.stChatInput > div {{
    background: rgba(255,255,255,0.12);
    backdrop-filter: blur(15px);
    border-radius: 16px;
    border: 2px solid rgba(255,255,255,0.2);
}}

.stChatInput input {{
    color: #ffffff !important;
}}

.stChatInput input::placeholder {{
    color: rgba(255,255,255,0.6);
}}

/* Sidebar */
.css-1d391kg {{
    background: linear-gradient(180deg, rgba(15,23,42,0.98), rgba(30,41,59,0.95));
    backdrop-filter: blur(15px);
}}

.css-1d391kg * {{
    color: #f1f5f9 !important;
}}

/* Buttons */
.stButton > button {{
    background: linear-gradient(135deg, #3b82f6, #7c3aed);
    color: white;
    border-radius: 12px;
    padding: 0.8rem 2.5rem;
    font-weight: 600;
    border: none;
    transition: all 0.3s ease;
}}

.stButton > button:hover {{
    transform: translateY(-2px);
    box-shadow: 0 8px 24px rgba(59,130,246,0.4);
}}

/* Animations */
@keyframes fadeInUp {{
    from {{ opacity: 0; transform: translateY(30px); }}
    to {{ opacity: 1; transform: translateY(0); }}
}}

.fade-in-up {{
    animation: fadeInUp 0.8s ease-out;
}}

/* Responsive */
@media (max-width: 768px) {{
    .main-title {{ font-size: 2.2rem; }}
    .stChatMessage[data-testid="user-message"] {{ margin-left: 1rem; }}
    .stChatMessage[data-testid="assistant-message"] {{ margin-right: 1rem; }}
}}
</style>
""", unsafe_allow_html=True)


# ---------------- SESSION STATE ----------------
if "chat" not in st.session_state:
    st.session_state.chat = []
if "step" not in st.session_state:
    st.session_state.step = 0
if "data" not in st.session_state:
    st.session_state.data = {}

# ---------------- CONSTANTS ----------------
EXIT_KEYWORDS = ["bye", "goodbye", "exit", "quit", "thank you", "thanks"]

# ---------------- SENTIMENT ANALYSIS ----------------
def analyze_sentiment(text):
    try:
        blob = TextBlob(text)
        polarity = blob.sentiment.polarity
        if polarity > 0.1:
            return "positive"
        elif polarity < -0.1:
            return "negative"
        else:
            return "neutral"
    except:
        return "neutral"

# ---------------- LANGUAGE ----------------
def detect_language(text):
    try:
        return detect(text)
    except:
        return "en"

def translate(text, target="en"):
    # Simple fallback translation - just return original text
    # In a real app, you could use Google Translate API or other services
    return text

# ---------------- TECH QUESTIONS ----------------
TECH_QUESTIONS = {
    "python": [
        "Explain Python decorators.",
        "What is the difference between list and tuple?",
        "How does garbage collection work in Python?",
        "What are Python generators and when would you use them?",
        "Explain the difference between @staticmethod and @classmethod."
    ],
    "django": [
        "Explain Django ORM.",
        "What is middleware in Django?",
        "Difference between function-based and class-based views?",
        "How does Django handle database migrations?",
        "What is Django's request-response cycle?"
    ],
    "react": [
        "What are React hooks?",
        "Explain virtual DOM.",
        "Difference between state and props?",
        "What is JSX and how does it work?",
        "Explain React component lifecycle methods."
    ],
    "node": [
        "What is event-driven architecture?",
        "Explain middleware in Express.js.",
        "What is non-blocking I/O?",
        "How does Node.js handle concurrency?",
        "What are streams in Node.js?"
    ],
    "sql": [
        "Difference between INNER JOIN and LEFT JOIN?",
        "What is normalization?",
        "Explain indexing.",
        "What are stored procedures?",
        "Difference between DELETE, DROP, and TRUNCATE?"
    ],
    "javascript": [
        "Explain closures in JavaScript.",
        "What is the difference between let, var, and const?",
        "How does async/await work?",
        "What is event bubbling?",
        "Explain the concept of hoisting."
    ],
    "java": [
        "What is the difference between abstract class and interface?",
        "Explain Java memory management.",
        "What are Java streams?",
        "Difference between ArrayList and LinkedList?",
        "What is polymorphism in Java?"
    ]
}

def generate_questions(stack):
    questions = []
    for tech in stack:
        tech = tech.lower()
        if tech in TECH_QUESTIONS:
            # Get 3 questions per technology instead of 2
            available_questions = TECH_QUESTIONS[tech]
            num_to_select = min(3, len(available_questions))
            questions.extend(random.sample(available_questions, num_to_select))
    # Ensure minimum 4 questions
    if len(questions) < 4:
        # Add general programming questions if not enough tech-specific ones
        general_questions = [
            "Describe your problem-solving approach.",
            "How do you handle debugging complex issues?",
            "What's your experience with version control?",
            "How do you stay updated with new technologies?",
            "Describe a challenging project you worked on."
        ]
        questions.extend(general_questions[:4-len(questions)])
    
    return questions[:6]  # Return up to 6 questions

# ---------------- PERSONALIZED RESPONSE ----------------
def personalize(msg):
    name = st.session_state.data.get("name", "")
    exp = st.session_state.data.get("experience", "")
    stack = st.session_state.data.get("tech_stack", [])

    if name:
        msg = f"{name}, {msg}"
    if exp and exp.isdigit() and int(exp) < 2:
        msg += " "
    if stack:
        msg += f" 💻 Tech focus: {', '.join(stack)}"

    return msg

# ---------------- AI RESPONSE FUNCTION ----------------
def get_ai_response(user_input, context=""):
    """
    Simple AI response function that can answer any question
    """
    user_input_lower = user_input.lower()
    
    # General greetings
    if any(word in user_input_lower for word in ["hello", "hi", "hey", "namaste"]):
        return "Hello! 👋 I'm TalentScout AI Assistant. I can help you with job applications, career advice, or answer any questions you have. How can I assist you today?"
    
    # Career related questions
    if any(word in user_input_lower for word in ["job", "career", "interview", "resume", "cv"]):
        return "Great question about careers! 💼 I can help you with job applications, interview preparation, resume tips, and career guidance. What specific aspect would you like to know more about?"
    
    # Technical questions
    if any(word in user_input_lower for word in ["python", "javascript", "react", "django", "sql", "programming", "coding"]):
        return "Excellent! I love discussing technology. 💻 I can help explain programming concepts, best practices, and technical interview questions. What specific technology or concept would you like to explore?"
    
    # General knowledge questions
    if "?" in user_input:
        return f"That's an interesting question! 🤔 While I specialize in recruitment and career guidance, I'm happy to help with general questions too. Could you provide more context about '{user_input}'? I'll do my best to assist you."
    
    # Default helpful response
    return "I'm here to help! 😊 I can assist with:\n\n• Job applications and career advice\n• Technical questions and programming concepts\n• Interview preparation\n• Resume and CV guidance\n• General questions and conversations\n\nWhat would you like to know more about?"

# ---------------- MAIN UI ----------------
# Title Section
st.markdown("""
<div style="text-align: center; margin-bottom: 3rem;">
    <h1 class="main-title">🤖 TalentScout Hiring Assistant</h1>
    <p class="subtitle">AI-Powered Recruitment Screening</p>
</div>
""", unsafe_allow_html=True)

# Welcome Message (only show if no chat history)
if not st.session_state.chat:
    st.markdown("""
    <div class="chat-container">
        <div class="welcome-message">
            <span class="welcome-icon">🤖</span>
            <span class="welcome-text">Hello! 👋 Welcome to TalentScout - Your AI-Powered Hiring Assistant.</span>
            <div class="welcome-description">
                I'm here to help you with our recruitment process. I'll collect some basic information about you and then ask relevant technical questions based on your skills.
            </div>
            <div class="welcome-prompt">
                Let's get started! Please enter your Full Name:
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Chat History
for role, message in st.session_state.chat:
    with st.chat_message(role):
        st.write(message)

# Chat Input
user_input = st.chat_input("Type your response...")

# ---------------- CHAT LOGIC ----------------
if user_input:
    if any(word in user_input.lower() for word in EXIT_KEYWORDS):
        st.session_state.chat.append(("assistant", "🙏 Thank you for your time! Our HR team will contact you soon."))
        st.stop()

    sentiment = analyze_sentiment(user_input)
    lang = detect_language(user_input)
    text = translate(user_input, "en")

    st.session_state.chat.append(("user", user_input))

    # ---------------- JOB SCREENING FLOW ----------------
    if st.session_state.step == 0:
        st.session_state.data["name"] = text
        reply = f"Nice to meet you, {text}! 😊\n\nPlease provide your email address:"
        st.session_state.step += 1

    elif st.session_state.step == 1:
        st.session_state.data["email"] = text
        reply = "Great! What's your phone number?"
        st.session_state.step += 1

    elif st.session_state.step == 2:
        st.session_state.data["phone"] = text
        reply = "How many years of professional experience do you have?"
        st.session_state.step += 1

    elif st.session_state.step == 3:
        st.session_state.data["experience"] = text
        reply = "What position are you applying for?"
        st.session_state.step += 1

    elif st.session_state.step == 4:
        st.session_state.data["position"] = text
        reply = "What's your current location?"
        st.session_state.step += 1

    elif st.session_state.step == 5:
        st.session_state.data["location"] = text
        reply = "Please list your technical skills/stack (comma separated):"
        st.session_state.step += 1

    elif st.session_state.step == 6:
        stack = [s.strip() for s in text.split(",")]
        st.session_state.data["tech_stack"] = stack
        questions = generate_questions(stack)

        reply = f"Perfect! Based on your skills, here are some technical questions:\n\n"
        for i, q in enumerate(questions, 1):
            reply += f"{i}. {q}\n"
        reply += "\n🎉 Thank you for completing the screening process! Our team will review your responses and get back to you soon."
        st.session_state.step += 1

    elif st.session_state.step >= 7:
        reply = "✅ Your screening is complete! Feel free to ask me any questions about the company or role while you wait for our response."
    
    # Add sentiment-based modifications
    if sentiment == "negative":
        reply = "😊 " + reply
    elif sentiment == "positive":
        reply = "🚀 " + reply

    st.session_state.chat.append(("assistant", reply))
    st.rerun()

# ---------------- ENHANCED SIDEBAR ----------------
with st.sidebar:
    # Header
    st.markdown("""
    <div style="text-align: center; padding: 1rem; background: linear-gradient(135deg, #3b82f6, #a855f7); border-radius: 12px; margin-bottom: 1.5rem;">
        <h2 style="color: white; margin: 0; font-size: 1.5rem;">🤖 TalentScout</h2>
        <p style="color: rgba(255,255,255,0.9); margin: 0; font-size: 0.9rem;">AI Hiring Assistant</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Application Progress Section
    if st.session_state.data or st.session_state.step > 0:
        st.markdown("### 📋 Application Progress")
        
        # Progress indicator with percentage
        progress = min(st.session_state.step / 7, 1.0)
        progress_percentage = int(progress * 100)
        
        st.progress(progress)
        st.markdown(f"""
        <div style="text-align: center; margin: 0.5rem 0;">
            <strong style="color: #3b82f6;">{progress_percentage}% Complete</strong><br>
            <small style="color: #64748b;">Step {st.session_state.step} of 7</small>
        </div>
        """, unsafe_allow_html=True)
        
        # Progress steps with status
        steps = [
            "👤 Personal Info",
            "📧 Contact Details", 
            "📱 Phone Number",
            "💼 Experience",
            "🎯 Position",
            "📍 Location",
            "💻 Tech Skills",
            "✅ Complete"
        ]
        
        st.markdown("#### Progress Steps:")
        for i, step_name in enumerate(steps):
            if i < st.session_state.step:
                st.markdown(f"✅ {step_name}")
            elif i == st.session_state.step:
                st.markdown(f"🔄 {step_name}")
            else:
                st.markdown(f"⏳ {step_name}")
        
        st.markdown("---")
    
    # Candidate Information Section
    if st.session_state.data:
        st.markdown("### 👤 Candidate Profile")
        
        # Personal Information
        if "name" in st.session_state.data:
            st.markdown(f"""
            <div class="candidate-info">
                <strong>👤 Full Name:</strong><br>
                {st.session_state.data['name']}
            </div>
            """, unsafe_allow_html=True)
        
        # Contact Information
        contact_info = []
        if "email" in st.session_state.data:
            contact_info.append(f"📧 {st.session_state.data['email']}")
        if "phone" in st.session_state.data:
            contact_info.append(f"📱 {st.session_state.data['phone']}")
        
        if contact_info:
            st.markdown(f"""
            <div class="candidate-info">
                <strong>📞 Contact Info:</strong><br>
                {' | '.join(contact_info)}
            </div>
            """, unsafe_allow_html=True)
        
        # Professional Information
        if "experience" in st.session_state.data:
            exp_years = st.session_state.data['experience']
            exp_level = "Entry Level" if exp_years.isdigit() and int(exp_years) < 2 else "Experienced"
            st.markdown(f"""
            <div class="candidate-info">
                <strong>💼 Experience:</strong><br>
                {exp_years} years ({exp_level})
            </div>
            """, unsafe_allow_html=True)
        
        if "position" in st.session_state.data:
            st.markdown(f"""
            <div class="candidate-info">
                <strong>🎯 Applied Position:</strong><br>
                {st.session_state.data['position']}
            </div>
            """, unsafe_allow_html=True)
        
        if "location" in st.session_state.data:
            st.markdown(f"""
            <div class="candidate-info">
                <strong>📍 Location:</strong><br>
                {st.session_state.data['location']}
            </div>
            """, unsafe_allow_html=True)
        
        # Technical Skills
        if "tech_stack" in st.session_state.data:
            skills = st.session_state.data['tech_stack']
            skills_html = ""
            for skill in skills:
                skills_html += f'<span style="background: #3b82f6; color: white; padding: 0.2rem 0.5rem; border-radius: 6px; margin: 0.1rem; display: inline-block; font-size: 0.8rem;">{skill.strip()}</span> '
            
            st.markdown(f"""
            <div class="candidate-info">
                <strong>💻 Technical Skills:</strong><br>
                {skills_html}
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
    
    # Application Status
    st.markdown("### 📊 Application Status")
    
    if st.session_state.step >= 7:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #10b981, #059669); padding: 1rem; border-radius: 8px; text-align: center; color: white;">
            <h4 style="margin: 0;">✅ Application Complete!</h4>
            <p style="margin: 0.5rem 0 0 0; font-size: 0.9rem;">Our HR team will review your profile</p>
        </div>
        """, unsafe_allow_html=True)
    elif st.session_state.step > 0:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #f59e0b, #d97706); padding: 1rem; border-radius: 8px; text-align: center; color: white;">
            <h4 style="margin: 0;">🔄 In Progress</h4>
            <p style="margin: 0.5rem 0 0 0; font-size: 0.9rem;">Please complete all steps</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #3b82f6, #2563eb); padding: 1rem; border-radius: 8px; text-align: center; color: white;">
            <h4 style="margin: 0;">🚀 Ready to Start</h4>
            <p style="margin: 0.5rem 0 0 0; font-size: 0.9rem;">Begin your application process</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Chat Statistics
    if st.session_state.chat:
        total_messages = len(st.session_state.chat)
        user_messages = len([msg for role, msg in st.session_state.chat if role == "user"])
        assistant_messages = len([msg for role, msg in st.session_state.chat if role == "assistant"])
        
        st.markdown("### 💬 Chat Statistics")
        st.markdown(f"""
        <div style="background: rgba(59, 130, 246, 0.1); padding: 1rem; border-radius: 8px; border-left: 4px solid #3b82f6;">
            <strong>📊 Conversation Stats:</strong><br>
            💬 Total Messages: {total_messages}<br>
            👤 Your Messages: {user_messages}<br>
            🤖 AI Responses: {assistant_messages}
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
    
    # Action Buttons
    st.markdown("### ⚙️ Actions")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🔄 Restart", use_container_width=True, help="Start the application process over"):
            st.session_state.step = 0
            st.session_state.data = {}
            st.session_state.chat = []
            st.rerun()
    
    with col2:
        if st.button("💾 Export", use_container_width=True, help="Export your application data"):
            if st.session_state.data:
                import json
                data_json = json.dumps(st.session_state.data, indent=2)
                st.download_button(
                    label="📄 Download JSON",
                    data=data_json,
                    file_name=f"application_{st.session_state.data.get('name', 'candidate')}.json",
                    mime="application/json",
                    use_container_width=True
                )
    
    # Help Section
    st.markdown("---")
    st.markdown("### ❓ Need Help?")
    
    with st.expander("📋 Application Process"):
        st.markdown("""
        **Steps to Complete:**
        1. Provide your full name
        2. Enter email address
        3. Share phone number
        4. Mention years of experience
        5. Specify position applying for
        6. Add your location
        7. List technical skills
        
        **Tips:**
        - Be honest and accurate
        - Use comma-separated skills
        - Complete all steps for best results
        """)
    
    with st.expander("🔧 Technical Support"):
        st.markdown("""
        **Common Issues:**
        - Refresh page if chat stops responding
        - Use desktop browser for best experience
        - Ensure stable internet connection
        
        **Contact:** support@talentscout.ai
        """)
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; padding: 1rem; color: #64748b; font-size: 0.8rem;">
        <p>🤖 TalentScout AI v2.0<br>
        Powered by Advanced AI Technology</p>
    </div>
    """, unsafe_allow_html=True

