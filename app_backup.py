import streamlit as st
from textblob import TextBlob
from langdetect import detect
from googletrans import Translator
import random

# ---------------- CONFIG ----------------
st.set_page_config(page_title="TalentScout Hiring Assistant", layout="centered")
translator = Translator()

EXIT_KEYWORDS = ["exit", "quit", "bye", "stop", "end"]

# ---------------- SESSION STATE ----------------
if "step" not in st.session_state:
    st.session_state.step = 0
    st.session_state.data = {}
    st.session_state.chat = []

# ---------------- SENTIMENT ----------------
def analyze_sentiment(text):
    polarity = TextBlob(text).sentiment.polarity
    if polarity > 0.2:
        return "positive"
    elif polarity < -0.2:
        return "negative"
    return "neutral"

# ---------------- LANGUAGE ----------------
def detect_language(text):
    try:
        return detect(text)
    except:
        return "en"

def translate(text, target="en"):
    try:
        return translator.translate(text, dest=target).text
    except:
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

# ---------------- CHAT UI ----------------
st.title("🤖 TalentScout Hiring Assistant")
st.caption("AI-powered initial screening chatbot")

for role, message in st.session_state.chat:
    with st.chat_message(role):
        st.write(message)

user_input = st.chat_input("Type your response...")

if user_input:
    if any(word in user_input.lower() for word in EXIT_KEYWORDS):
        st.session_state.chat.append(("assistant", "🙏 Thank you for your time! Our HR team will contact you soon."))
        st.stop()

    sentiment = analyze_sentiment(user_input)
    lang = detect_language(user_input)
    text = translate(user_input, "en")

    st.session_state.chat.append(("user", user_input))

    # ---------------- FLOW ----------------
    if st.session_state.step == 0:
        reply = "Hello! 👋 Welcome to TalentScout. What is your full name?"
        st.session_state.step += 1

    elif st.session_state.step == 1:
        st.session_state.data["name"] = text
        reply = "Please provide your email address."
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

    else:
        reply = "✅ Screening complete. We will get back to you shortly."

    if sentiment == "negative":
        reply = "😊 Don't worry. " + reply
    elif sentiment == "positive":
        reply = "🚀 Awesome! " + reply

    reply = personalize(reply)
    reply = translate(reply, lang)

    st.session_state.chat.append(("assistant", reply))
