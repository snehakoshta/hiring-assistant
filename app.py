import streamlit as st
import random
import time

# ---------------- CONFIG ----------------
st.set_page_config(
    page_title="TalentScout Hiring Assistant", 
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Force sidebar to be visible
st.markdown("""
<script>
    // Force sidebar to be visible
    const sidebar = document.querySelector('[data-testid="stSidebar"]');
    if (sidebar) {
        sidebar.style.display = 'block';
        sidebar.style.visibility = 'visible';
        sidebar.style.opacity = '1';
    }
</script>
""", unsafe_allow_html=True)

# ---------------- CSS ----------------
st.markdown("""
<style>
/* Import Professional Fonts */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

/* Global Professional Styles */
.stApp {
    background: 
        linear-gradient(135deg, rgba(15, 23, 42, 0.97) 0%, rgba(30, 41, 59, 0.95) 50%, rgba(51, 65, 85, 0.93) 100%),
        radial-gradient(circle at 20% 80%, rgba(59, 130, 246, 0.1) 0%, transparent 50%),
        radial-gradient(circle at 80% 20%, rgba(168, 85, 247, 0.1) 0%, transparent 50%);
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    min-height: 100vh;
    color: #f8fafc;
}

/* Hide Streamlit Branding */
#MainMenu { visibility: hidden; }
footer { visibility: hidden; }
header { visibility: hidden; }
.stDeployButton { visibility: hidden; }

/* Professional Main Container */
.main .block-container {
    padding: 2rem 3rem;
    max-width: none;
    background: rgba(255, 255, 255, 0.02);
    backdrop-filter: blur(20px);
    border-radius: 24px;
    border: 1px solid rgba(255, 255, 255, 0.08);
    box-shadow: 
        0 20px 40px rgba(0, 0, 0, 0.3),
        inset 0 1px 0 rgba(255, 255, 255, 0.1);
    margin: 1rem;
}

/* ENHANCED SIDEBAR STYLING - SIMPLE TOGGLE */
.css-1d391kg, 
.css-1lcbmhc, 
.css-1outpf7, 
.css-k1vhr4,
.css-17eq0hr,
[data-testid="stSidebar"],
section[data-testid="stSidebar"],
.css-1cypcdb,
.css-1d391kg,
.css-1lcbmhc {
    display: block !important;
    visibility: visible !important;
    opacity: 1 !important;
    width: 320px !important;
    min-width: 320px !important;
    max-width: 320px !important;
    position: relative !important;
    left: 0 !important;
    transform: translateX(0) !important;
    background: 
        linear-gradient(180deg, rgba(15, 23, 42, 0.98) 0%, rgba(30, 41, 59, 0.96) 100%) !important;
    backdrop-filter: blur(20px) !important;
    border-right: 1px solid rgba(255, 255, 255, 0.12) !important;
    box-shadow: 
        4px 0 20px rgba(0, 0, 0, 0.3),
        inset -1px 0 0 rgba(255, 255, 255, 0.05) !important;
    z-index: 999 !important;
    transition: transform 0.3s ease-in-out !important;
}

/* Collapsed sidebar state */
.sidebar-collapsed .css-1d391kg,
.sidebar-collapsed .css-1lcbmhc,
.sidebar-collapsed .css-1outpf7,
.sidebar-collapsed .css-k1vhr4,
.sidebar-collapsed .css-17eq0hr,
.sidebar-collapsed [data-testid="stSidebar"],
.sidebar-collapsed section[data-testid="stSidebar"] {
    transform: translateX(-300px) !important;
}

/* Sidebar Toggle Button */
.sidebar-toggle {
    position: fixed !important;
    top: 20px !important;
    left: 330px !important;
    z-index: 1001 !important;
    background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%) !important;
    border: none !important;
    border-radius: 8px !important;
    width: 40px !important;
    height: 40px !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    cursor: pointer !important;
    box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3) !important;
    transition: all 0.3s ease-in-out !important;
    color: white !important;
    font-size: 16px !important;
    font-weight: bold !important;
}

.sidebar-toggle:hover {
    background: linear-gradient(135deg, #2563eb 0%, #1e40af 100%) !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 20px rgba(59, 130, 246, 0.4) !important;
}

/* Collapsed state toggle button position */
.sidebar-collapsed .sidebar-toggle {
    left: 20px !important;
}

/* Force sidebar container to be visible */
.css-1d391kg > div,
.css-1lcbmhc > div,
[data-testid="stSidebar"] > div,
section[data-testid="stSidebar"] > div {
    display: block !important;
    visibility: visible !important;
    opacity: 1 !important;
    padding: 1.5rem !important;
}

/* Ensure sidebar toggle button doesn't hide sidebar */
.css-1rs6os,
.css-vk3wp9,
[data-testid="collapsedControl"] {
    display: none !important;
}

/* Professional Sidebar Text */
[data-testid="stSidebar"] *,
section[data-testid="stSidebar"] * {
    color: #f1f5f9 !important;
    font-family: 'Inter', sans-serif !important;
}

/* Sidebar Headers */
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 {
    color: #ffffff !important;
    font-weight: 600 !important;
    margin-bottom: 1rem !important;
    padding-bottom: 0.5rem !important;
    border-bottom: 1px solid rgba(255, 255, 255, 0.1) !important;
}

/* Professional Cards in Sidebar */
[data-testid="stSidebar"] .element-container {
    background: rgba(255, 255, 255, 0.05) !important;
    border-radius: 12px !important;
    padding: 1rem !important;
    margin: 0.5rem 0 !important;
    border: 1px solid rgba(255, 255, 255, 0.08) !important;
    backdrop-filter: blur(10px) !important;
}

/* Sidebar Buttons */
[data-testid="stSidebar"] .stButton > button {
    background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 0.75rem 1.5rem !important;
    font-weight: 500 !important;
    font-size: 0.9rem !important;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
    box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3) !important;
    width: 100% !important;
}

[data-testid="stSidebar"] .stButton > button:hover {
    background: linear-gradient(135deg, #2563eb 0%, #1e40af 100%) !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 20px rgba(59, 130, 246, 0.4) !important;
}

/* Professional Progress Bar */
[data-testid="stSidebar"] .stProgress > div > div > div {
    background: linear-gradient(90deg, #3b82f6 0%, #8b5cf6 50%, #06b6d4 100%) !important;
    border-radius: 6px !important;
    height: 8px !important;
}

[data-testid="stSidebar"] .stProgress > div > div {
    background: rgba(255, 255, 255, 0.1) !important;
    border-radius: 6px !important;
    height: 8px !important;
}

/* Professional Status Indicators */
.status-indicator {
    display: inline-flex;
    align-items: center;
    padding: 0.5rem 1rem;
    border-radius: 20px;
    font-size: 0.85rem;
    font-weight: 500;
    margin: 0.25rem 0;
}

.status-complete {
    background: linear-gradient(135deg, #10b981, #059669);
    color: white;
    box-shadow: 0 4px 12px rgba(16, 185, 129, 0.3);
}

.status-progress {
    background: linear-gradient(135deg, #f59e0b, #d97706);
    color: white;
    box-shadow: 0 4px 12px rgba(245, 158, 11, 0.3);
}

.status-ready {
    background: linear-gradient(135deg, #3b82f6, #2563eb);
    color: white;
    box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
}

/* Professional Chat Messages */
.stChatMessage {
    padding: 1.5rem !important;
    border-radius: 16px !important;
    margin-bottom: 1.5rem !important;
    backdrop-filter: blur(10px) !important;
    border: 1px solid rgba(255, 255, 255, 0.1) !important;
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.2) !important;
}

.stChatMessage[data-testid="user-message"] {
    background: linear-gradient(135deg, rgba(59, 130, 246, 0.15), rgba(37, 99, 235, 0.1)) !important;
    border-left: 4px solid #3b82f6 !important;
    margin-left: 2rem !important;
}

.stChatMessage[data-testid="assistant-message"] {
    background: linear-gradient(135deg, rgba(168, 85, 247, 0.15), rgba(147, 51, 234, 0.1)) !important;
    border-left: 4px solid #a855f7 !important;
    margin-right: 2rem !important;
}

/* Professional Chat Input */
.stChatInput > div {
    background: rgba(255, 255, 255, 0.08) !important;
    backdrop-filter: blur(15px) !important;
    border-radius: 16px !important;
    border: 2px solid rgba(255, 255, 255, 0.12) !important;
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.2) !important;
}

.stChatInput input {
    color: #ffffff !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 1rem !important;
}

.stChatInput input::placeholder {
    color: rgba(255, 255, 255, 0.5) !important;
}

/* Professional Buttons */
.stButton > button {
    background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%) !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 0.75rem 2rem !important;
    font-weight: 500 !important;
    font-family: 'Inter', sans-serif !important;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
    box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3) !important;
}

.stButton > button:hover {
    background: linear-gradient(135deg, #2563eb 0%, #1e40af 100%) !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 20px rgba(59, 130, 246, 0.4) !important;
}

/* Professional Typography */
h1, h2, h3, h4, h5, h6 {
    font-family: 'Inter', sans-serif !important;
    font-weight: 600 !important;
    color: #ffffff !important;
}

/* Code and Technical Text */
code, pre {
    font-family: 'JetBrains Mono', monospace !important;
    background: rgba(255, 255, 255, 0.1) !important;
    border-radius: 6px !important;
    padding: 0.25rem 0.5rem !important;
}

/* Professional Animations */
@keyframes slideInRight {
    from { opacity: 0; transform: translateX(30px); }
    to { opacity: 1; transform: translateX(0); }
}

@keyframes fadeInUp {
    from { opacity: 0; transform: translateY(20px); }
    to { opacity: 1; transform: translateY(0); }
}

.slide-in-right {
    animation: slideInRight 0.6s ease-out;
}

.fade-in-up {
    animation: fadeInUp 0.8s ease-out;
}

/* Professional Scrollbar */
::-webkit-scrollbar {
    width: 8px;
}

::-webkit-scrollbar-track {
    background: rgba(255, 255, 255, 0.05);
    border-radius: 4px;
}

::-webkit-scrollbar-thumb {
    background: linear-gradient(135deg, #3b82f6, #8b5cf6);
    border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
    background: linear-gradient(135deg, #2563eb, #7c3aed);
}

/* Responsive Design */
@media (max-width: 768px) {
    [data-testid="stSidebar"] {
        width: 300px !important;
        min-width: 300px !important;
    }
    
    .main .block-container {
        padding: 1rem 1.5rem;
        margin: 0.5rem;
    }
    
    .stChatMessage[data-testid="user-message"] {
        margin-left: 1rem !important;
    }
    
    .stChatMessage[data-testid="assistant-message"] {
        margin-right: 1rem !important;
    }
}

/* Professional Loading States */
.loading-shimmer {
    background: linear-gradient(90deg, rgba(255,255,255,0.1) 25%, rgba(255,255,255,0.2) 50%, rgba(255,255,255,0.1) 75%);
    background-size: 200% 100%;
    animation: shimmer 2s infinite;
}

@keyframes shimmer {
    0% { background-position: -200% 0; }
    100% { background-position: 200% 0; }
}

/* Force sidebar visibility on load */
body {
    --sidebar-width: 320px;
}

/* Additional sidebar force rules */
.stApp > div:first-child {
    display: flex !important;
}

.stApp > div:first-child > div:first-child {
    display: block !important;
    width: 320px !important;
    min-width: 320px !important;
}
</style>

<script>
// Enhanced sidebar visibility and toggle script
function ensureSidebarVisible() {
    const sidebar = document.querySelector('[data-testid="stSidebar"]');
    const sidebarSection = document.querySelector('section[data-testid="stSidebar"]');
    const collapsedControl = document.querySelector('[data-testid="collapsedControl"]');
    
    // Hide collapse control
    if (collapsedControl) {
        collapsedControl.style.display = 'none';
    }
    
    // Force sidebar visibility
    [sidebar, sidebarSection].forEach(element => {
        if (element) {
            element.style.display = 'block';
            element.style.visibility = 'visible';
            element.style.opacity = '1';
            element.style.width = '320px';
            element.style.minWidth = '320px';
        }
    });
    
    // Add sidebar toggle functionality
    addSidebarToggle();
}

function addSidebarToggle() {
    // Remove existing toggle if present
    const existingToggle = document.querySelector('.sidebar-toggle');
    if (existingToggle) {
        existingToggle.remove();
    }
    
    // Create toggle button
    const toggleButton = document.createElement('button');
    toggleButton.className = 'sidebar-toggle';
    toggleButton.innerHTML = '<<';
    toggleButton.title = 'Toggle Sidebar';
    
    // Add click handler
    toggleButton.addEventListener('click', function() {
        const body = document.body;
        const isCollapsed = body.classList.contains('sidebar-collapsed');
        
        if (isCollapsed) {
            body.classList.remove('sidebar-collapsed');
            toggleButton.innerHTML = '<<';
            // Store state
            sessionStorage.setItem('sidebarCollapsed', 'false');
        } else {
            body.classList.add('sidebar-collapsed');
            toggleButton.innerHTML = '>>';
            // Store state
            sessionStorage.setItem('sidebarCollapsed', 'true');
        }
    });
    
    // Add to page
    document.body.appendChild(toggleButton);
    
    // Restore previous state
    const savedState = sessionStorage.getItem('sidebarCollapsed');
    if (savedState === 'true') {
        document.body.classList.add('sidebar-collapsed');
        toggleButton.innerHTML = '>>';
    }
}

// Run on page load
document.addEventListener('DOMContentLoaded', ensureSidebarVisible);

// Run after Streamlit updates
setTimeout(ensureSidebarVisible, 100);
setTimeout(ensureSidebarVisible, 500);
setTimeout(ensureSidebarVisible, 1000);

// Watch for changes and re-apply
const observer = new MutationObserver(ensureSidebarVisible);
observer.observe(document.body, { childList: true, subtree: true });
</script>
""", unsafe_allow_html=True)

EXIT_KEYWORDS = ["exit", "quit", "bye", "stop", "end"]
GREETING_KEYWORDS = ["hello", "hi", "hey", "good morning", "good afternoon", "good evening", "namaste", "greetings", "hola", "bonjour", "guten tag", "ciao", "konnichiwa", "salaam", "shalom"]

# ---------------- SESSION STATE ----------------
if "chat" not in st.session_state:
    st.session_state.chat = []
if "step" not in st.session_state:
    st.session_state.step = 0
if "data" not in st.session_state:
    st.session_state.data = {}
if "tech_questions" not in st.session_state:
    st.session_state.tech_questions = []
if "current_question_index" not in st.session_state:
    st.session_state.current_question_index = 0
if "question_answers" not in st.session_state:
    st.session_state.question_answers = []
if "sidebar_collapsed" not in st.session_state:
    st.session_state.sidebar_collapsed = False

# ---------------- SIMPLE SENTIMENT ANALYSIS ----------------
def analyze_sentiment(text):
    """Simple keyword-based sentiment analysis"""
    text_lower = text.lower()
    
    positive_words = ['happy', 'excited', 'great', 'excellent', 'amazing', 'wonderful', 'good', 'love', 'like', 'awesome', 'fantastic']
    negative_words = ['sad', 'angry', 'frustrated', 'disappointed', 'terrible', 'awful', 'bad', 'hate', 'dislike', 'worried', 'stressed']
    nervous_words = ['nervous', 'anxious', 'worried', 'scared', 'afraid', 'tension', 'stress', 'panic', 'overwhelmed', 'intimidated', 'jittery', 'uneasy', 'apprehensive', 'restless', 'fidgety']
    excited_words = ['excited', 'thrilled', 'pumped', 'enthusiastic', 'energetic', 'eager', 'stoked', 'hyped', 'elated', 'ecstatic', 'overjoyed', 'exhilarated']
    
    positive_count = sum(1 for word in positive_words if word in text_lower)
    negative_count = sum(1 for word in negative_words if word in text_lower)
    nervous_count = sum(1 for word in nervous_words if word in text_lower)
    excited_count = sum(1 for word in excited_words if word in text_lower)
    
    if nervous_count > 0:
        return "nervous"
    elif excited_count > 0:
        return "excited"
    elif positive_count > negative_count:
        return "positive"
    elif negative_count > positive_count:
        return "negative"
    else:
        return "neutral"

# ---------------- GREETING DETECTION ----------------
def detect_greeting(text):
    """Detect if user input contains greeting words"""
    text_lower = text.lower().strip()
    
    # Check for exact greetings or greetings at start of message
    for greeting in GREETING_KEYWORDS:
        if text_lower == greeting or text_lower.startswith(greeting + " ") or text_lower.startswith(greeting + ","):
            return True
    
    # Also check if greeting is anywhere in short messages (3 words or less)
    if len(text_lower.split()) <= 3:
        for greeting in GREETING_KEYWORDS:
            if greeting in text_lower:
                return True
    
    return False

def get_excited_response():
    """Return a random energetic response for excited users"""
    excited_messages = [
        "🎉 WOW! I love your energy! That excitement is contagious - let's channel it into this conversation! ⚡",
        "🚀 AMAZING! Your enthusiasm is fantastic! This is going to be such a great conversation! 🌟",
        "🔥 YES! I can feel your excitement through the screen! Let's keep this energy going! 💫",
        "⭐ INCREDIBLE! Your excitement is absolutely wonderful! This positive energy is exactly what we love to see! 🎊",
        "🎯 FANTASTIC! Your enthusiasm is inspiring! I'm excited to learn more about you too! 🌈",
        "💥 BOOM! That excitement is PERFECT! You're bringing such great energy to this conversation! ✨",
        "🎪 WOOHOO! I'm getting excited just from your message! This is going to be an awesome chat! 🎭",
        "🌟 SPECTACULAR! Your excitement is lighting up the conversation! Let's ride this wave of positive energy! 🏄‍♂️"
    ]
    return random.choice(excited_messages)

def get_comforting_response():
    """Return a random comforting response for nervous users"""
    comforting_messages = [
        "💙 Don't worry, it's completely normal to feel nervous! Take a deep breath - you've got this! 🌟",
        "🤗 I understand you're feeling nervous. Remember, this is just a conversation - be yourself and you'll do great! ✨",
        "💪 Feeling nervous shows you care! That's actually a good sign. Let's take this step by step together. 😊",
        "🌸 It's okay to feel nervous - everyone does! Just remember, we're here to get to know you better. Relax and be yourself! 💫",
        "🧘‍♀️ Take a moment to breathe. You're doing great so far! There's no pressure - just be authentic. 🌈",
        "💝 Nervousness is totally understandable! Think of this as a friendly chat rather than an interview. You're in good hands! 🤝",
        "🌟 I can sense you're nervous, and that's perfectly fine! Remember, we want you to succeed. Let's go at your pace. 💙",
        "🤲 Feeling anxious is natural! Just focus on sharing your genuine experiences. There are no wrong answers here! ☀️"
    ]
    return random.choice(comforting_messages)

def get_greeting_response():
    """Return a random greeting response"""
    greetings = [
        "Hello! Nice to meet you! 👋",
        "Hi there! Great to see you! 😊", 
        "Hello! Welcome to TalentScout! 🤖",
        "Hi! Nice to meet you! 😊",
        "Hello! How are you doing today? 😊",
        "Hi there! Welcome! 🌟",
        "Hello! Glad you're here! 👋",
        "Hi! Hope you're having a great day! ☀️",
        "Namaste! Welcome to TalentScout! 🙏",
        "Greetings! Nice to meet you! ✨",
        "Hello there! Ready to get started? 🚀",
        "Hi! Wonderful to have you here! 💫"
    ]
    return random.choice(greetings)

# ---------------- TECH QUESTIONS ----------------
TECH_QUESTIONS = {
    "python": [
        "Explain Python decorators.",
        "What is the difference between list and tuple?",
        "How does garbage collection work in Python?",
        "What are Python generators and when would you use them?"
    ],
    "javascript": [
        "Explain closures in JavaScript.",
        "What is the difference between let, var, and const?",
        "How does async/await work?",
        "What is event bubbling?"
    ],
    "react": [
        "What are React hooks?",
        "Explain virtual DOM.",
        "Difference between state and props?",
        "What is JSX and how does it work?"
    ],
    "java": [
        "What is the difference between abstract class and interface?",
        "Explain Java memory management.",
        "What are Java streams?",
        "Difference between ArrayList and LinkedList?"
    ]
}

def generate_questions(stack):
    questions = []
    for tech in stack:
        tech = tech.lower().strip()
        if tech in TECH_QUESTIONS:
            available_questions = TECH_QUESTIONS[tech]
            num_to_select = min(2, len(available_questions))
            questions.extend(random.sample(available_questions, num_to_select))
    
    # Add general questions if not enough tech-specific ones
    if len(questions) < 4:
        general_questions = [
            "Describe your problem-solving approach.",
            "How do you handle debugging complex issues?",
            "What's your experience with version control?",
            "How do you stay updated with new technologies?"
        ]
        questions.extend(general_questions[:4-len(questions)])
    
    return questions[:4]

# ---------------- MAIN UI ----------------
# Title Section
st.markdown("""
<div style="text-align: center; margin-bottom: 3rem;">
    <h1 style="background: linear-gradient(135deg, #f8fafc, #cbd5e0); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-size: 3rem; font-weight: 800;">🤖 TalentScout Hiring Assistant</h1>
    <p style="color: #e2e8f0; font-size: 1.2rem;">AI-Powered Recruitment Screening</p>
</div>
""", unsafe_allow_html=True)

# Welcome Message
if not st.session_state.chat:
    st.markdown("""
    <div style="background: rgba(168, 85, 247, 0.15); padding: 2rem; border-radius: 16px; margin-bottom: 2rem; border: 1px solid rgba(168, 85, 247, 0.3); text-align: center;">
        <div style="font-size: 3rem; margin-bottom: 1rem;">🤖</div>
        <div style="font-size: 1.3rem; font-weight: 600; color: #f1f5f9; margin-bottom: 1rem;">Hello! 👋 Welcome to TalentScout - Your AI-Powered Hiring Assistant.</div>
        <div style="color: #cbd5e0; margin-bottom: 1.5rem; line-height: 1.6;">
            I'm here to help you with our recruitment process. I'll collect some basic information about you and then ask relevant technical questions based on your skills.
        </div>
        <div style="color: #3b82f6; font-weight: 500; font-size: 1.1rem;">
            Let's get started! Please enter your Full Name:
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

    # Check for greetings first
    if detect_greeting(user_input):
        greeting_response = get_greeting_response()
        
        # If it's just a greeting (not part of answering a question), respond with greeting
        if st.session_state.step == 0 and len(user_input.strip().split()) <= 3:
            st.session_state.chat.append(("user", user_input))
            st.session_state.chat.append(("assistant", f"{greeting_response}\n\nI'm here to help you with our recruitment process. Let's get started!\n\nPlease enter your Full Name:"))
            st.rerun()

    # Simple sentiment analysis
    sentiment = analyze_sentiment(user_input)
    
    st.session_state.chat.append(("user", user_input))

    # ---------------- SCREENING FLOW ----------------
    if st.session_state.step == 0:
        st.session_state.data["name"] = user_input
        reply = f"Nice to meet you, {user_input}! 😊\n\nPlease provide your email address:"
        st.session_state.step += 1

    elif st.session_state.step == 1:
        st.session_state.data["email"] = user_input
        reply = "Great! What's your phone number?"
        st.session_state.step += 1

    elif st.session_state.step == 2:
        st.session_state.data["phone"] = user_input
        reply = "How many years of professional experience do you have?"
        st.session_state.step += 1

    elif st.session_state.step == 3:
        st.session_state.data["experience"] = user_input
        reply = "What position are you applying for?"
        st.session_state.step += 1

    elif st.session_state.step == 4:
        st.session_state.data["position"] = user_input
        reply = "What's your current location?"
        st.session_state.step += 1

    elif st.session_state.step == 5:
        st.session_state.data["location"] = user_input
        reply = "Please list your technical skills/stack (comma separated):"
        st.session_state.step += 1

    elif st.session_state.step == 6:
        stack = [s.strip() for s in user_input.split(",")]
        st.session_state.data["tech_stack"] = stack
        
        # Generate questions
        st.session_state.tech_questions = generate_questions(stack)
        st.session_state.current_question_index = 0
        st.session_state.question_answers = []
        
        # Ask first question
        first_question = st.session_state.tech_questions[0]
        reply = f"Perfect! Based on your skills, I'll now ask you some technical questions one by one.\n\n**Question 1 of 4:**\n{first_question}\n\nPlease share your answer:"
        st.session_state.step += 1

    elif st.session_state.step == 7:
        # Handle technical questions
        current_q_index = st.session_state.current_question_index
        current_question = st.session_state.tech_questions[current_q_index]
        
        # Store answer
        st.session_state.question_answers.append({
            "question": current_question,
            "answer": user_input
        })
        
        # Move to next question
        st.session_state.current_question_index += 1
        
        # Check if more questions
        if st.session_state.current_question_index < len(st.session_state.tech_questions):
            next_q_index = st.session_state.current_question_index
            next_question = st.session_state.tech_questions[next_q_index]
            
            encouragements = ["Great answer! 👍", "Excellent response! 🌟", "Well explained! 💯", "Nice insight! ✨"]
            encouragement = random.choice(encouragements)
            reply = f"{encouragement}\n\n**Question {next_q_index + 1} of 4:**\n{next_question}\n\nPlease share your answer:"
        else:
            # All questions completed
            reply = f"Excellent work! 🎉\n\nYou've successfully completed all 4 technical questions. Thank you for taking the time to share your knowledge and experience with us.\n\nOur HR team will review your responses along with your profile and get back to you soon. Feel free to ask me any questions about the company or role while you wait!"
            st.session_state.step += 1

    elif st.session_state.step >= 8:
        # Check if it's a greeting during completed state
        if detect_greeting(user_input) and len(user_input.strip().split()) <= 3:
            greeting_response = get_greeting_response()
            reply = f"{greeting_response} ✅ Your screening is complete! Feel free to ask me any questions about the company or role while you wait for our response."
        else:
            reply = "✅ Your screening is complete! Feel free to ask me any questions about the company or role while you wait for our response."
    
    # Add sentiment-based modifications
    if sentiment == "nervous":
        comforting_msg = get_comforting_response()
        reply = f"{comforting_msg}\n\n{reply}"
    elif sentiment == "excited":
        excited_msg = get_excited_response()
        reply = f"{excited_msg}\n\n{reply}"
    elif sentiment == "negative":
        reply = "😊 Don't worry. " + reply
    elif sentiment == "positive":
        reply = "🚀 Awesome! " + reply

    # Personalize if we have user data
    if st.session_state.data.get("name"):
        reply = f"{st.session_state.data['name']}, {reply}"

    st.session_state.chat.append(("assistant", reply))
    st.rerun()

# ---------------- SIDEBAR ----------------
with st.sidebar:
    # Header
    st.markdown("""
    <div style="text-align: center; padding: 1rem; background: linear-gradient(135deg, #3b82f6, #a855f7); border-radius: 12px; margin-bottom: 1.5rem;">
        <h2 style="color: white; margin: 0; font-size: 1.5rem;">🤖 TalentScout</h2>
        <p style="color: rgba(255,255,255,0.9); margin: 0; font-size: 0.9rem;">AI Hiring Assistant</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Progress Section
    if st.session_state.data or st.session_state.step > 0:
        st.markdown("### 📋 Application Progress")
        
        total_steps = 8
        progress = min(st.session_state.step / total_steps, 1.0)
        progress_percentage = int(progress * 100)
        
        st.progress(progress)
        st.markdown(f"**{progress_percentage}% Complete**")
        st.markdown(f"Step {st.session_state.step} of {total_steps}")
        
        st.markdown("---")
    
    # Candidate Information
    if st.session_state.data:
        st.markdown("### 👤 Candidate Profile")
        
        for key, value in st.session_state.data.items():
            if key == "tech_stack":
                st.markdown(f"**💻 {key.replace('_', ' ').title()}:** {', '.join(value)}")
            else:
                st.markdown(f"**{key.replace('_', ' ').title()}:** {value}")
        
        st.markdown("---")
    
    # Technical Questions Progress
    if st.session_state.step == 7 and st.session_state.tech_questions:
        st.markdown("### ❓ Technical Questions")
        
        for i, question in enumerate(st.session_state.tech_questions):
            if i < st.session_state.current_question_index:
                st.markdown(f"✅ **Q{i+1}:** {question[:40]}...")
            elif i == st.session_state.current_question_index:
                st.markdown(f"🔄 **Q{i+1}:** {question[:40]}...")
            else:
                st.markdown(f"⏳ **Q{i+1}:** {question[:40]}...")
        
        st.markdown("---")
    
    # Application Status
    st.markdown("### 📊 Application Status")
    
    if st.session_state.step >= 8:
        st.success("✅ Application Complete!")
    elif st.session_state.step == 7:
        st.info("❓ Technical Questions")
    elif st.session_state.step > 0:
        st.warning("🔄 In Progress")
    else:
        st.info("🚀 Ready to Start")
    
    st.markdown("---")
    
    # Restart button
    if st.button("🔄 Restart", use_container_width=True):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()