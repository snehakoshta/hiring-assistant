import streamlit as st
from textblob import TextBlob
from langdetect import detect
# from googletrans import Translator  # Removed - not available
import random

# ---------------- CONFIG ----------------
st.set_page_config(page_title="TalentScout Hiring Assistant", layout="centered")

EXIT_KEYWORDS = ["exit", "quit", "bye", "stop", "end"]

# ---------------- SESSION STATE ----------------
if "step" not in st.session_state:
    st.session_state.step = 0
    st.session_state.data = {}
    st.session_state.chat = []

# ---------------- SENTIMENT ----------------
def analyze_sentiment(text):
    try:
        polarity = TextBlob(text).sentiment.polarity
        if polarity > 0.2:
            return "positive"
        elif polarity < -0.2:
            return "negative"
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
        "How does garbage collection work in Python?"
    ],
    "django": [
        "Explain Django ORM.",
        "What is middleware in Django?",
        "Difference between function-based and class-based views?"
    ],
    "react": [
        "What are React hooks?",
        "Explain virtual DOM.",
        "Difference between state and props?"
    ],
    "node": [
        "What is event-driven architecture?",
        "Explain middleware in Express.js.",
        "What is non-blocking I/O?"
    ],
    "sql": [
        "Difference between INNER JOIN and LEFT JOIN?",
        "What is normalization?",
        "Explain indexing."
    ]
}

def generate_questions(stack):
    questions = []
    for tech in stack:
        tech = tech.lower()
        if tech in TECH_QUESTIONS:
            questions.extend(random.sample(TECH_QUESTIONS[tech], 2))
    return questions[:5]

# ---------------- PERSONALIZED RESPONSE ----------------
def personalize(msg):
    name = st.session_state.data.get("name", "")
    exp = st.session_state.data.get("experience", "")
    stack = st.session_state.data.get("tech_stack", [])

    if name:
        msg = f"{name}, {msg}"
    if exp and exp.isdigit() and int(exp) < 2:
        msg += " 🌱 As an early-career professional, focus on fundamentals."
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

# ---------------- CHAT UI ----------------
st.title("🤖 TalentScout Hiring Assistant")
st.caption("AI-powered assistant for jobs, careers, and general questions")

# Add info about capabilities
st.info("💡 **I can help with:** Job applications, career advice, technical questions, interview prep, and general conversations!")

for role, message in st.session_state.chat:
    with st.chat_message(role):
        st.write(message)

user_input = st.chat_input("Ask me anything...")

if user_input:
    if any(word in user_input.lower() for word in EXIT_KEYWORDS):
        st.session_state.chat.append(("assistant", "🙏 Thank you for your time! Our HR team will contact you soon."))
        st.stop()

    sentiment = analyze_sentiment(user_input)
    lang = detect_language(user_input)
    text = translate(user_input, "en")

    st.session_state.chat.append(("user", user_input))

    # Check if user wants to start job screening
    if any(word in user_input.lower() for word in ["start screening", "apply", "job application", "screening"]):
        st.session_state.step = 1
        reply = "Great! Let's start the job screening process. 🚀\n\nWhat is your full name?"
    
    # ---------------- JOB SCREENING FLOW ----------------
    elif st.session_state.step == 1:
        st.session_state.data["name"] = text
        reply = "Nice to meet you! Please provide your email address."
        st.session_state.step += 1

    elif st.session_state.step == 2:
        st.session_state.data["email"] = text
        reply = "Your phone number?"
        st.session_state.step += 1

    elif st.session_state.step == 3:
        st.session_state.data["phone"] = text
        reply = "How many years of experience do you have?"
        st.session_state.step += 1

    elif st.session_state.step == 4:
        st.session_state.data["experience"] = text
        reply = "What position are you applying for?"
        st.session_state.step += 1

    elif st.session_state.step == 5:
        st.session_state.data["position"] = text
        reply = "Your current location?"
        st.session_state.step += 1

    elif st.session_state.step == 6:
        st.session_state.data["location"] = text
        reply = "Please list your tech stack (comma separated)."
        st.session_state.step += 1

    elif st.session_state.step == 7:
        stack = [s.strip() for s in text.split(",")]
        st.session_state.data["tech_stack"] = stack
        questions = generate_questions(stack)

        reply = "Great! Here are some technical questions:\n\n"
        for q in questions:
            reply += f"• {q}\n"
        reply += "\nThank you for completing the screening! 🎉"
        st.session_state.step += 1

    elif st.session_state.step >= 8:
        reply = "✅ Screening complete. We will get back to you shortly.\n\nFeel free to ask me any other questions!"
    
    # ---------------- GENERAL AI RESPONSES ----------------
    else:
        # Use AI response for general questions
        reply = get_ai_response(user_input, str(st.session_state.data))
        
        # Add screening suggestion if not in screening mode
        if st.session_state.step == 0:
            reply += "\n\n💼 **Want to apply for a job?** Just say 'start screening' to begin!"

    # Add sentiment-based modifications
    if sentiment == "negative":
        reply = "😊 Don't worry. " + reply
    elif sentiment == "positive":
        reply = "🚀 Awesome! " + reply

    # Personalize if we have user data
    if st.session_state.data:
        reply = personalize(reply)

    st.session_state.chat.append(("assistant", reply))
    st.rerun()

# Show current data in sidebar if available
if st.session_state.data:
    with st.sidebar:
        st.header("📋 Your Information")
        for key, value in st.session_state.data.items():
            st.write(f"**{key.title()}:** {value}")
        
        if st.button("🔄 Start Over"):
            st.session_state.step = 0
            st.session_state.data = {}
            st.session_state.chat = []
            st.rerun()