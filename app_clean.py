import streamlit as st
from textblob import TextBlob
from langdetect import detect
import random
import time

# ---------------- CSS LOADING ----------------
def load_css():
    """Load external CSS file or fallback to inline styles"""
    try:
        with open('styles.css') as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    except FileNotFoundError:
        # Fallback inline CSS
        st.markdown("""
        <style>
        /* Import Google Fonts */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
        
        /* Global Styles */
        .stApp {
            background: linear-gradient(135deg, rgba(15, 23, 42, 0.95) 0%, rgba(30, 41, 59, 0.9) 50%, rgba(51, 65, 85, 0.85) 100%);
            font-family: 'Inter', sans-serif;
            min-height: 100vh;
        }
        
        /* Hide Streamlit branding */
        #MainMenu { visibility: hidden; }
        footer { visibility: hidden; }
        header { visibility: hidden; }
        
        /* Sidebar */
        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, rgba(15,23,42,0.98), rgba(30,41,59,0.95));
            backdrop-filter: blur(15px);
        }
        
        [data-testid="stSidebar"] * {
            color: #f1f5f9 !important;
        }
        
        /* Chat messages */
        .stChatMessage {
            padding: 1.5rem;
            border-radius: 16px;
            margin-bottom: 1rem;
            backdrop-filter: blur(6px);
        }
        
        .stChatMessage[data-testid="user-message"] {
            background: rgba(59, 130, 246, 0.25);
        }
        
        .stChatMessage[data-testid="assistant-message"] {
            background: rgba(168, 85, 247, 0.25);
        }
        
        /* Buttons */
        .stButton > button {
            background: linear-gradient(135deg, #3b82f6, #7c3aed);
            color: white;
            border-radius: 12px;
            border: none;
            transition: all 0.3s ease;
        }
        
        .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 24px rgba(59,130,246,0.4);
        }
        </style>
        """, unsafe_allow_html=True)

# ---------------- CONFIG ----------------
st.set_page_config(page_title="TalentScout Hiring Assistant", layout="centered")

# Load CSS styles
load_css()

EXIT_KEYWORDS = ["exit", "quit", "bye", "stop", "end"]

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
if "sentiment_history" not in st.session_state:
    st.session_state.sentiment_history = []

# ---------------- SENTIMENT ANALYSIS ----------------
def analyze_sentiment(text):
    """
    Enhanced sentiment analysis that returns a dictionary with detailed information
    """
    try:
        blob = TextBlob(text)
        polarity = blob.sentiment.polarity
        subjectivity = blob.sentiment.subjectivity
        
        # Determine sentiment category
        if polarity > 0.3:
            sentiment = "very positive"
        elif polarity > 0.1:
            sentiment = "positive"
        elif polarity < -0.3:
            sentiment = "very negative"
        elif polarity < -0.1:
            sentiment = "negative"
        else:
            sentiment = "neutral"
            
        # Return detailed sentiment data
        return {
            "category": sentiment,
            "polarity": round(polarity, 2),
            "subjectivity": round(subjectivity, 2),
            "confidence": abs(polarity),
            "method": "textblob"
        }
    except Exception as e:
        # Fallback to simple keyword analysis
        return analyze_sentiment_fallback(text)

def analyze_sentiment_fallback(text):
    """
    Fallback sentiment analysis using keyword matching
    """
    text_lower = text.lower()
    
    # Positive keywords
    positive_words = ['happy', 'excited', 'great', 'excellent', 'amazing', 'wonderful', 'good', 'love', 'like']
    # Negative keywords  
    negative_words = ['sad', 'angry', 'frustrated', 'disappointed', 'terrible', 'awful', 'bad', 'hate', 'dislike']
    
    positive_count = sum(1 for word in positive_words if word in text_lower)
    negative_count = sum(1 for word in negative_words if word in text_lower)
    
    if positive_count > negative_count:
        sentiment = "positive"
        polarity = 0.3
    elif negative_count > positive_count:
        sentiment = "negative"
        polarity = -0.3
    else:
        sentiment = "neutral"
        polarity = 0.0
    
    return {
        "category": sentiment,
        "polarity": polarity,
        "subjectivity": 0.5,
        "confidence": abs(polarity),
        "method": "keyword_fallback"
    }

# ---------------- LANGUAGE ----------------
def detect_language(text):
    try:
        return detect(text)
    except:
        return "en"

def translate(text, target="en"):
    # Simple fallback translation - just return original text
    return text

# ---------------- TECH QUESTIONS ----------------
TECH_QUESTIONS = {
    "python": [
        "Explain Python decorators.",
        "What is the difference between list and tuple?",
        "How does garbage collection work in Python?",
        "What are Python generators and when would you use them?"
    ],
    "django": [
        "Explain Django ORM.",
        "What is middleware in Django?",
        "Difference between function-based and class-based views?",
        "How does Django handle database migrations?"
    ],
    "react": [
        "What are React hooks?",
        "Explain virtual DOM.",
        "Difference between state and props?",
        "What is JSX and how does it work?"
    ],
    "javascript": [
        "Explain closures in JavaScript.",
        "What is the difference between let, var, and const?",
        "How does async/await work?",
        "What is event bubbling?"
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
        tech = tech.lower()
        if tech in TECH_QUESTIONS:
            # Get 2 questions per technology
            available_questions = TECH_QUESTIONS[tech]
            num_to_select = min(2, len(available_questions))
            questions.extend(random.sample(available_questions, num_to_select))
    
    # Add general programming questions if not enough tech-specific ones
    if len(questions) < 4:
        general_questions = [
            "Describe your problem-solving approach.",
            "How do you handle debugging complex issues?",
            "What's your experience with version control?",
            "How do you stay updated with new technologies?"
        ]
        questions.extend(general_questions[:4-len(questions)])
    
    # Return exactly 4 questions
    return questions[:4]

# ---------------- PERSONALIZED RESPONSE ----------------
def personalize(msg):
    name = st.session_state.data.get("name", "")
    if name:
        msg = f"{name}, {msg}"
    return msg

# ---------------- MAIN UI ----------------
# Title Section
st.markdown("""
<div style="text-align: center; margin-bottom: 3rem;">
    <h1 style="background: linear-gradient(135deg, #f8fafc, #cbd5e0); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-size: 3rem; font-weight: 800;">🤖 TalentScout Hiring Assistant</h1>
    <p style="color: #e2e8f0; font-size: 1.2rem;">AI-Powered Recruitment Screening</p>
</div>
""", unsafe_allow_html=True)

# Welcome Message (only show if no chat history)
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

    # Analyze sentiment
    sentiment_data = analyze_sentiment(user_input)
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
        
        # Generate questions and store them
        st.session_state.tech_questions = generate_questions(stack)
        st.session_state.current_question_index = 0
        st.session_state.question_answers = []
        
        # Ask the first technical question
        first_question = st.session_state.tech_questions[0]
        reply = f"Perfect! Based on your skills, I'll now ask you some technical questions one by one.\n\n**Question 1 of 4:**\n{first_question}\n\nPlease share your answer:"
        st.session_state.step += 1

    elif st.session_state.step == 7:
        # Handle technical question answers
        current_q_index = st.session_state.current_question_index
        current_question = st.session_state.tech_questions[current_q_index]
        
        # Store the question-answer pair
        st.session_state.question_answers.append({
            "question": current_question,
            "answer": text
        })
        
        # Move to next question
        st.session_state.current_question_index += 1
        
        # Check if we have more questions
        if st.session_state.current_question_index < len(st.session_state.tech_questions):
            next_q_index = st.session_state.current_question_index
            next_question = st.session_state.tech_questions[next_q_index]
            
            # Provide encouraging feedback and ask next question
            encouragements = [
                "Great answer! 👍",
                "Excellent response! 🌟", 
                "Well explained! 💯",
                "Nice insight! ✨"
            ]
            
            encouragement = random.choice(encouragements)
            reply = f"{encouragement}\n\n**Question {next_q_index + 1} of 4:**\n{next_question}\n\nPlease share your answer:"
        else:
            # All questions completed
            reply = f"Excellent work! 🎉\n\nYou've successfully completed all 4 technical questions. Thank you for taking the time to share your knowledge and experience with us.\n\nOur HR team will review your responses along with your profile and get back to you soon. Feel free to ask me any questions about the company or role while you wait!"
            st.session_state.step += 1

    elif st.session_state.step >= 8:
        reply = "✅ Your screening is complete! Feel free to ask me any questions about the company or role while you wait for our response."
    
    # Add sentiment-based modifications
    if sentiment_data.get("category") == "negative":
        reply = "😊 Don't worry. " + reply
    elif sentiment_data.get("category") == "positive":
        reply = "🚀 Awesome! " + reply

    # Personalize if we have user data
    if st.session_state.data:
        reply = personalize(reply)

    # Store sentiment data safely
    try:
        if "sentiment_history" not in st.session_state:
            st.session_state.sentiment_history = []
        
        if sentiment_data:
            st.session_state.sentiment_history.append({
                "message": user_input,
                "sentiment": sentiment_data,
                "timestamp": time.time()
            })
    except Exception as e:
        # If there's any error, just initialize and continue
        st.session_state.sentiment_history = []

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
    
    # Application Progress Section
    if st.session_state.data or st.session_state.step > 0:
        st.markdown("### 📋 Application Progress")
        
        # Progress indicator
        total_steps = 8
        progress = min(st.session_state.step / total_steps, 1.0)
        progress_percentage = int(progress * 100)
        
        st.progress(progress)
        st.markdown(f"**{progress_percentage}% Complete** - Step {st.session_state.step} of {total_steps}")
        
        st.markdown("---")
    
    # Candidate Information Section
    if st.session_state.data:
        st.markdown("### 👤 Candidate Profile")
        
        for key, value in st.session_state.data.items():
            if key == "tech_stack":
                st.markdown(f"**💻 {key.replace('_', ' ').title()}:** {', '.join(value)}")
            else:
                st.markdown(f"**{key.replace('_', ' ').title()}:** {value}")
        
        st.markdown("---")
    
    # Sentiment Analysis Section
    if hasattr(st.session_state, 'sentiment_history') and st.session_state.sentiment_history:
        st.markdown("### 😊 Sentiment Analysis")
        
        # Get the latest sentiment
        latest_sentiment = st.session_state.sentiment_history[-1]
        sentiment_data = latest_sentiment["sentiment"]
        
        st.markdown(f"**Current Mood:** {sentiment_data['category'].title()}")
        st.markdown(f"**Confidence:** {sentiment_data['confidence']:.2f}")
        
        st.markdown("---")
    
    # Restart button
    if st.button("🔄 Restart", use_container_width=True):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()