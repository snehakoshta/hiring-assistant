import streamlit as st
import os

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
        pass
    
    # Fallback to environment variable (for local development)
    if not api_key:
        api_key = os.getenv("GOOGLE_API_KEY")
        if api_key:
            print("✅ API key loaded from environment variable")
    
    # Last resort: read directly from .env file (for local development)
    if not api_key:
        try:
            with open('.env', 'r', encoding='utf-8') as f:
                content = f.read().strip()
                if 'GOOGLE_API_KEY=' in content:
                    # Extract API key directly from file
                    api_key = content.split('GOOGLE_API_KEY=')[1].split('\n')[0].strip()
                    print("✅ API key loaded from .env file")
        except Exception as e:
            print(f"⚠️ Could not read .env file: {e}")
    
    if not api_key:
        st.error("❌ GOOGLE_API_KEY not found. Please configure it in Streamlit Cloud secrets or .env file.")
        AI_AVAILABLE = False
        ADVANCED_FEATURES = False
    else:
        print(f"✅ API Key found: {api_key[:10]}...")
        # Configure Google GenAI client
        genai_client = genai.Client(api_key=api_key)
        
        # Test API connection (but don't fail if quota exceeded)
        try:
            test_response = genai_client.models.generate_content(
                model='gemini-flash-latest',  # Use the working model
                contents="Test"
            )
            print("✅ API connection test successful!")
            AI_AVAILABLE = True
            ADVANCED_FEATURES = True
        except Exception as e:
            error_str = str(e).lower()
            if "quota" in error_str or "429" in str(e):
                print("⚠️ API quota exceeded - app will use fallback responses")
            elif "overloaded" in error_str or "503" in str(e):
                print("⚠️ API temporarily overloaded - app will retry with fallbacks")
            else:
                print(f"⚠️ API connection test failed: {e}")
            
            # Still set AI_AVAILABLE to True to allow fallback handling
            AI_AVAILABLE = True
            ADVANCED_FEATURES = True
        
except ImportError as e:
    AI_AVAILABLE = False
    ADVANCED_FEATURES = False
    st.warning(f"⚠️ Required libraries not installed. Install with: pip install google-genai python-dotenv textblob langdetect\nError: {e}")
except Exception as e:
    AI_AVAILABLE = False
    ADVANCED_FEATURES = False
    st.error(f"❌ Error initializing AI client: {e}")

# Configuration
st.set_page_config(
    page_title="TalentScout Hiring Assistant",
    page_icon="🤖",
    layout="centered"
)

# Data collection fields
FIELDS = [
    "Full Name",
    "Email Address", 
    "Phone Number",
    "Years of Experience",
    "Desired Position(s)",
    "Current Location",
    "Tech Stack"
]

# Technical interview questions per technology
TECH_QUESTIONS = {
    'python': [
        "What are the key differences between Python 2 and Python 3?",
        "Explain Python's GIL (Global Interpreter Lock) and its impact.",
        "How do you handle memory management in Python?",
        "What are Python decorators and how do you use them?"
    ],
    'javascript': [
        "What is the difference between var, let, and const in JavaScript?",
        "Explain JavaScript closures with an example.",
        "How does asynchronous programming work in JavaScript?",
        "What are JavaScript promises and async/await?"
    ],
    'react': [
        "What are React hooks and why are they useful?",
        "Explain the difference between state and props in React.",
        "How do you handle state management in large React applications?",
        "What is the virtual DOM and how does it work?"
    ],
    'java': [
        "What are the main principles of Object-Oriented Programming in Java?",
        "Explain the difference between abstract classes and interfaces.",
        "How does garbage collection work in Java?",
        "What are Java generics and why are they important?"
    ],
    'sql': [
        "What is the difference between INNER JOIN and LEFT JOIN?",
        "How do you optimize slow SQL queries?",
        "Explain database normalization and its benefits.",
        "What are SQL indexes and when should you use them?"
    ],
    'node.js': [
        "What is Node.js and how does it work?",
        "Explain the event loop in Node.js.",
        "What are callbacks, promises, and async/await in Node.js?",
        "How do you handle file operations in Node.js?"
    ]
}

# Advanced Features Functions
def detect_emotions(text):
    """Detect specific emotions in text"""
    emotions = []
    text_lower = text.lower()
    
    # Emotion keywords mapping
    emotion_keywords = {
        "excited": ["excited", "thrilled", "enthusiastic", "eager", "pumped", "amazing", "fantastic"],
        "nervous": ["nervous", "anxious", "worried", "scared", "concerned", "afraid", "stressed"],
        "confident": ["confident", "sure", "ready", "prepared", "capable", "skilled"],
        "frustrated": ["frustrated", "annoyed", "upset", "disappointed", "angry"],
        "hopeful": ["hopeful", "optimistic", "positive", "looking forward", "expecting"],
        "grateful": ["grateful", "thankful", "appreciate", "blessed", "lucky"]
    }
    
    for emotion, keywords in emotion_keywords.items():
        if any(keyword in text_lower for keyword in keywords):
            emotions.append(emotion)
    
    return emotions

def analyze_sentiment(text):
    """Enhanced sentiment analysis of user response"""
    if not ADVANCED_FEATURES:
        return {"polarity": 0, "subjectivity": 0, "sentiment": "neutral", "confidence": 0}
    
    try:
        blob = TextBlob(text)
        polarity = blob.sentiment.polarity
        subjectivity = blob.sentiment.subjectivity
        
        # Enhanced sentiment classification
        if polarity > 0.3:
            sentiment = "very positive"
            confidence = min(polarity * 100, 95)
        elif polarity > 0.1:
            sentiment = "positive"
            confidence = polarity * 80
        elif polarity < -0.3:
            sentiment = "very negative"
            confidence = min(abs(polarity) * 100, 95)
        elif polarity < -0.1:
            sentiment = "negative"
            confidence = abs(polarity) * 80
        else:
            sentiment = "neutral"
            confidence = 50
            
        # Detect specific emotions
        emotions = detect_emotions(text)
        
        return {
            "polarity": polarity,
            "subjectivity": subjectivity,
            "sentiment": sentiment,
            "confidence": round(confidence, 1),
            "emotions": emotions
        }
    except:
        return {"polarity": 0, "subjectivity": 0, "sentiment": "neutral", "confidence": 0, "emotions": []}

def detect_language(text):
    """Enhanced language detection with confidence"""
    if not ADVANCED_FEATURES:
        return {"language": "en", "confidence": 100}
    
    try:
        from langdetect import detect, detect_langs
        
        # Get language with confidence
        detected_lang = detect(text)
        lang_probs = detect_langs(text)
        
        # Find confidence for detected language
        confidence = 0
        for lang_prob in lang_probs:
            if lang_prob.lang == detected_lang:
                confidence = round(lang_prob.prob * 100, 1)
                break
        
        return {
            "language": detected_lang,
            "confidence": confidence,
            "all_languages": [(lp.lang, round(lp.prob * 100, 1)) for lp in lang_probs[:3]]
        }
    except:
        return {"language": "en", "confidence": 100, "all_languages": [("en", 100)]}

def translate_text(text, target_lang="en"):
    """Enhanced translation with multiple language support"""
    if not ADVANCED_FEATURES:
        return text
    
    try:
        detected = detect_language(text)
        source_lang = detected["language"] if isinstance(detected, dict) else detected
        
        if source_lang == target_lang:
            return text
        
        # Enhanced translation dictionary
        translations = {
            'hi': {
                # Greetings
                'Hello': 'नमस्ते', 'Hi': 'हाय', 'Good morning': 'सुप्रभात',
                'Good evening': 'शुभ संध्या', 'Welcome': 'स्वागत है',
                
                # Common phrases
                'Thank you': 'धन्यवाद', 'Please': 'कृपया', 'Yes': 'हाँ', 'No': 'नहीं',
                'Good': 'अच्छा', 'Great': 'बहुत बढ़िया', 'Excellent': 'उत्कृष्ट',
                
                # Job-related terms
                'Job': 'नौकरी', 'Work': 'काम', 'Experience': 'अनुभव',
                'Skills': 'कौशल', 'Interview': 'साक्षात्कार', 'Application': 'आवेदन',
                'Resume': 'बायोडाटा', 'Career': 'करियर', 'Position': 'पद',
                
                # Emotions
                'Excited': 'उत्साहित', 'Nervous': 'घबराया हुआ', 'Happy': 'खुश',
                'Confident': 'आत्मविश्वासी', 'Ready': 'तैयार'
            },
            'es': {
                # Greetings
                'Hello': 'Hola', 'Hi': 'Hola', 'Good morning': 'Buenos días',
                'Good evening': 'Buenas tardes', 'Welcome': 'Bienvenido',
                
                # Common phrases
                'Thank you': 'Gracias', 'Please': 'Por favor', 'Yes': 'Sí', 'No': 'No',
                'Good': 'Bueno', 'Great': 'Excelente', 'Excellent': 'Excelente',
                
                # Job-related terms
                'Job': 'Trabajo', 'Work': 'Trabajo', 'Experience': 'Experiencia',
                'Skills': 'Habilidades', 'Interview': 'Entrevista', 'Application': 'Aplicación',
                'Resume': 'Currículum', 'Career': 'Carrera', 'Position': 'Posición'
            },
            'fr': {
                # Greetings
                'Hello': 'Bonjour', 'Hi': 'Salut', 'Good morning': 'Bonjour',
                'Good evening': 'Bonsoir', 'Welcome': 'Bienvenue',
                
                # Common phrases
                'Thank you': 'Merci', 'Please': 'S\'il vous plaît', 'Yes': 'Oui', 'No': 'Non',
                'Good': 'Bon', 'Great': 'Excellent', 'Excellent': 'Excellent',
                
                # Job-related terms
                'Job': 'Emploi', 'Work': 'Travail', 'Experience': 'Expérience',
                'Skills': 'Compétences', 'Interview': 'Entretien', 'Application': 'Candidature'
            }
        }
        
        if target_lang in translations:
            translated_text = text
            for english, translated in translations[target_lang].items():
                # Case-insensitive replacement
                import re
                pattern = re.compile(re.escape(english), re.IGNORECASE)
                translated_text = pattern.sub(translated, translated_text)
            return translated_text
        
        return text
    except Exception as e:
        return text

def get_personalized_response(base_response, user_data, sentiment_data, language_data):
    """Generate highly personalized response based on user data and context"""
    if not ADVANCED_FEATURES:
        return base_response
    
    try:
        personalized = base_response
        user_name = user_data.get("Full Name", "")
        
        # Name personalization
        if user_name and user_name.strip():
            first_name = user_name.split()[0]
            personalized = f"Hi {first_name}! {personalized}"
        
        # Sentiment-based personalization
        sentiment = sentiment_data.get("sentiment", "neutral")
        emotions = sentiment_data.get("emotions", [])
        
        if sentiment == "very positive" or "excited" in emotions:
            personalized = f"🎉 {personalized}"
        elif sentiment == "positive" or "confident" in emotions:
            personalized = f"😊 {personalized}"
        elif sentiment == "negative" or "nervous" in emotions:
            personalized = f"💪 Don't worry! {personalized}"
        elif "frustrated" in emotions:
            personalized = f"🤗 I understand your concerns. {personalized}"
        
        # Experience-based personalization
        experience = user_data.get("Years of Experience", "")
        if experience:
            try:
                years = float(str(experience).replace("years", "").replace("year", "").strip())
                if years == 0:
                    personalized += "\n\n💡 As a fresh graduate, focus on showcasing your projects and learning enthusiasm!"
                elif years < 2:
                    personalized += "\n\n🌱 Your early career experience is valuable - highlight your growth mindset!"
                elif years < 5:
                    personalized += "\n\n🚀 With your solid experience, you're in a great position for career advancement!"
                elif years >= 5:
                    personalized += "\n\n🏆 Your extensive experience makes you a strong candidate for senior roles!"
            except:
                pass
        
        # Tech stack personalization
        tech_stack = user_data.get("Tech Stack", "")
        if tech_stack:
            tech_lower = tech_stack.lower()
            if any(tech in tech_lower for tech in ["python", "javascript", "react", "node"]):
                personalized += "\n\n💻 Great tech stack! These are highly in-demand skills."
            elif any(tech in tech_lower for tech in ["java", "spring", "sql"]):
                personalized += "\n\n🏢 Excellent enterprise technology skills!"
            elif any(tech in tech_lower for tech in ["ai", "ml", "data", "analytics"]):
                personalized += "\n\n🤖 AI/Data skills are the future - you're ahead of the curve!"
        
        # Language-based personalization
        if isinstance(language_data, dict):
            detected_lang = language_data.get("language", "en")
            confidence = language_data.get("confidence", 100)
            
            if detected_lang == "hi" and confidence > 70:
                personalized += "\n\n🇮🇳 मैं हिंदी में भी बात कर सकता हूँ!"
            elif detected_lang == "es" and confidence > 70:
                personalized += "\n\n🇪🇸 ¡También puedo ayudarte en español!"
            elif detected_lang == "fr" and confidence > 70:
                personalized += "\n\n🇫🇷 Je peux aussi vous aider en français!"
        
        return personalized
        
    except Exception as e:
        return base_response

def get_ai_response(user_message, context=""):
    """Get AI response using Google GenAI API or fallback"""
    if not AI_AVAILABLE:
        return "I'm a hiring assistant! I can help you with job applications and career questions. However, AI features are not available right now. Please install Google GenAI library with: pip install google-genai python-dotenv"
    
    try:
        # Advanced Features: Language Detection and Translation
        detected_lang = "en"
        translated_message = user_message
        
        if ADVANCED_FEATURES:
            detected_lang = detect_language(user_message)
            if detected_lang != "en":
                translated_message = translate_text(user_message, "en")
        
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
        
        # Combine system prompt with user message for GenAI
        full_prompt = f"{system_prompt}\n\nUser Question: {translated_message}\n\nAssistant:"
        
        # Use quota-aware model selection (prioritize working models)
        models_to_try = [
            'gemini-flash-latest',   # This one is working!
            'gemini-2.0-flash-lite', # Lighter version
            'gemini-2.0-flash',      # Might have quota issues
            'gemini-2.5-flash'       # Backup
        ]
        
        response = None
        last_error = None
        
        for model_name in models_to_try:
            for attempt in range(3):  # Try each model 3 times
                try:
                    response = genai_client.models.generate_content(
                        model=model_name,
                        contents=full_prompt
                    )
                    # Success! Break out of both loops
                    break
                except Exception as e:
                    last_error = e
                    error_str = str(e).lower()
                    
                    if "overloaded" in error_str or "503" in error_str or "unavailable" in error_str:
                        # Model overloaded, wait and retry
                        import time
                        time.sleep(1 + attempt)  # Increasing delay
                        continue
                    else:
                        # Different error, try next model
                        break
            
            if response:
                break  # Success, exit model loop
        
        if not response:
            # All models failed, raise the last error
            raise last_error
        
        # Translate response back if needed
        response_text = response.text
        if ADVANCED_FEATURES and detected_lang != "en":
            response_text = translate_text(response.text, detected_lang)
        
        return response_text
    except Exception as e:
        error_msg = str(e)
        
        # Debug: Print error details (only in development)
        if os.getenv("STREAMLIT_SHARING") != "true":
            print(f"🐛 API Error: {error_msg}")
            print(f"🐛 Error Type: {type(e).__name__}")
        
        # Handle specific error types
        if "quota" in error_msg.lower() or "429" in error_msg or "resource_exhausted" in error_msg.lower():
            # Quota exceeded - use intelligent fallback system
            return get_fallback_response(user_message, context)
                
        elif "overloaded" in error_msg.lower() or "503" in error_msg or "unavailable" in error_msg.lower():
            # Model overloaded - use intelligent fallback system  
            return get_fallback_response(user_message, context)
        elif "quota" in error_msg.lower() or "billing" in error_msg.lower() or "429" in error_msg:
            return "I'm a hiring assistant! 🤖 We've reached our daily AI quota limit, but I can still help you with our structured job screening process!\n\n**What I can do right now:**\n• Collect your job application information\n• Ask relevant technical questions\n• Provide career guidance\n• Help with interview preparation\n\n**Type 'start screening' to begin!**"
        elif "401" in error_msg or "403" in error_msg or "invalid_api_key" in error_msg.lower():
            return "I'm a hiring assistant! The Google API key appears to be invalid. Please check your API key at https://console.cloud.google.com/apis/credentials and update the .env file."
        elif "404" in error_msg and "model" in error_msg.lower():
            return "I'm a hiring assistant! The AI model is temporarily unavailable. Please try again in a few moments."
        else:
            # Generic fallback with helpful response
            return f"I'm a hiring assistant! I can help you with job applications and career questions. Let me assist you with our structured screening process instead. Type 'start screening' to begin!"

def validate_input(field, user_input):
    """Validate user input based on field type"""
    user_input = user_input.strip()
    
    if not user_input:
        return {"valid": False, "message": "Input cannot be empty."}
    
    if field == "Email Address":
        import re
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, user_input):
            return {"valid": False, "message": "Please enter a valid email address (e.g., john@example.com)."}
    
    elif field == "Phone Number":
        # Allow various phone number formats
        import re
        phone_pattern = r'^[\+]?[1-9][\d\s\-\(\)]{7,15}$'
        if not re.match(phone_pattern, user_input.replace(" ", "").replace("-", "").replace("(", "").replace(")", "")):
            return {"valid": False, "message": "Please enter a valid phone number (e.g., +1-234-567-8900 or 1234567890)."}
    
    elif field == "Years of Experience":
        try:
            years = float(user_input.replace("years", "").replace("year", "").strip())
            if years < 0 or years > 50:
                return {"valid": False, "message": "Please enter a valid number of years (0-50)."}
        except ValueError:
            return {"valid": False, "message": "Please enter years of experience as a number (e.g., 3, 2.5, 0)."}
    
    elif field == "Tech Stack":
        if len(user_input) < 3:
            return {"valid": False, "message": "Please provide at least one technology (e.g., Python, React, Java)."}
    
    return {"valid": True, "message": ""}

def get_greeting():
    return (
        "Hello! 👋 Welcome to **TalentScout** - Your AI-Powered Hiring Assistant.\n\n"
        "I'm here to help you with our recruitment process. I'll collect some basic information about you and then ask relevant technical questions based on your skills.\n\n"
        "Let's get started! Please enter your **Full Name**:"
    )

def get_next_technical_question(state):
    """Get the next technical question based on current progress"""
    tech_stack = state.get("Tech Stack", "")
    if not tech_stack:
        return None
    
    # Get current technical interview progress
    current_tech = state.get("current_tech", 0)
    current_question = state.get("current_question", 0)
    
    # Parse tech stack
    techs = [t.strip().lower() for t in tech_stack.split(",")]
    
    # If we've finished all technologies
    if current_tech >= len(techs):
        return None
    
    tech = techs[current_tech]
    
    # Get questions for current technology
    if tech in TECH_QUESTIONS:
        questions = TECH_QUESTIONS[tech]
    else:
        # Generic questions for unknown technologies
        questions = [
            f"What are the core concepts of {tech.title()}?",
            f"Explain a real-world project where you used {tech.title()}.",
            f"What challenges have you faced while working with {tech.title()}?",
            f"How do you stay updated with {tech.title()} best practices?"
        ]
    
    # If we've finished questions for current tech, move to next
    if current_question >= len(questions) or current_question >= 4:  # Max 4 questions per tech
        state["current_tech"] = current_tech + 1
        state["current_question"] = 0
        return get_next_technical_question(state)
    
    # Return current question
    question = questions[current_question]
    state["current_question"] = current_question + 1
    
    return {
        "question": question,
        "tech": tech.title()
    }

def generate_technical_questions(tech_stack):
    if not tech_stack:
        return []
    
    techs = [t.strip().lower() for t in tech_stack.split(",")]
    questions = []
    
    # Enhanced question bank for different technologies
    question_templates = {
        'python': [
            "What are the key differences between Python 2 and Python 3?",
            "Explain Python's GIL (Global Interpreter Lock) and its impact on multithreading.",
            "How do you handle memory management in Python?",
            "What are Python decorators and how do you use them?",
            "Describe the difference between list, tuple, and set in Python."
        ],
        'javascript': [
            "What is the difference between var, let, and const in JavaScript?",
            "Explain JavaScript closures with an example.",
            "How does asynchronous programming work in JavaScript (callbacks, promises, async/await)?",
            "What is event bubbling and event capturing in JavaScript?",
            "Describe the concept of hoisting in JavaScript."
        ],
        'react': [
            "What are React hooks and why are they useful?",
            "Explain the difference between state and props in React.",
            "How do you handle state management in large React applications?",
            "What is the virtual DOM and how does it work?",
            "Describe the React component lifecycle methods."
        ],
        'java': [
            "What are the main principles of Object-Oriented Programming in Java?",
            "Explain the difference between abstract classes and interfaces in Java.",
            "How does garbage collection work in Java?",
            "What are Java generics and why are they important?",
            "Describe the difference between ArrayList and LinkedList."
        ],
        'sql': [
            "What is the difference between INNER JOIN and LEFT JOIN?",
            "How do you optimize slow SQL queries?",
            "Explain database normalization and its benefits.",
            "What are SQL indexes and when should you use them?",
            "Describe the ACID properties in database transactions."
        ],
        'django': [
            "What is Django ORM and how does it work?",
            "Explain Django's MVT (Model-View-Template) architecture.",
            "How do you handle database migrations in Django?",
            "What are Django middlewares and how do you create custom ones?",
            "Describe Django's authentication and authorization system."
        ],
        'node.js': [
            "What is the event loop in Node.js?",
            "How do you handle asynchronous operations in Node.js?",
            "What are the differences between require() and import in Node.js?",
            "Explain the concept of middleware in Express.js.",
            "How do you handle error handling in Node.js applications?"
        ],
        'mongodb': [
            "What are the advantages of MongoDB over relational databases?",
            "Explain the concept of collections and documents in MongoDB.",
            "How do you perform aggregation operations in MongoDB?",
            "What is indexing in MongoDB and why is it important?",
            "Describe the difference between embedded and referenced documents."
        ],
        'git': [
            "What is the difference between git merge and git rebase?",
            "How do you resolve merge conflicts in Git?",
            "Explain the Git workflow (staging, committing, pushing).",
            "What are Git branches and how do you manage them?",
            "How do you undo changes in Git (reset vs revert)?"
        ],
        'docker': [
            "What is containerization and how does Docker work?",
            "Explain the difference between Docker images and containers.",
            "How do you create a Dockerfile for a web application?",
            "What is Docker Compose and when do you use it?",
            "How do you manage data persistence in Docker containers?"
        ]
    }
    
    # Generic questions for any technology
    generic_questions = [
        "What are the core concepts and features of {tech}?",
        "Describe a real-world project where you used {tech} and the challenges you faced.",
        "What are the best practices you follow when working with {tech}?",
        "How do you stay updated with the latest developments in {tech}?",
        "What tools and libraries do you commonly use with {tech}?"
    ]
    
    for tech in techs:
        tech_clean = tech.strip().lower()
        if tech_clean in question_templates:
            # Use specific questions for known technologies (limit to 2 per tech)
            questions.extend(question_templates[tech_clean][:2])
        else:
            # Use generic questions for unknown technologies (limit to 1 per tech)
            for template in generic_questions[:1]:
                questions.append(template.format(tech=tech.strip()))
    
    # Return 3-5 questions maximum
    return questions[:5]

def store_candidate_data(state, field, value):
    state[field] = value

def get_bot_response(user_input, state):
    # Check for exit commands first (before any other logic)
    exit_commands = ['exit', 'quit', 'bye', 'stop', 'goodbye', 'end', 'धन्यवाद', 'बाई', 'समाप्त', 'खत्म']
    if user_input.lower().strip() in exit_commands:
        return (
            "आपके समय के लिए धन्यवाद! 🙏\n"
            "Thank you for your time!\n\n"
            "आपकी जानकारी record हो गई है। हमारी HR team आपके application को review करके जल्दी ही आपसे contact करेगी।\n"
            "Your information has been recorded. Our HR team will review your application and contact you soon.\n\n"
            "आपका दिन शुभ हो! 👋\n"
            "Have a great day!"
        )
    
    # Auto-start screening if this is the first interaction
    if "step" not in state and "screening_mode" not in state:
        state["screening_mode"] = True
        state["step"] = 0
        return get_greeting()
    
    # Check if user wants to start screening manually
    if user_input.lower() in ['start screening', 'start', 'begin screening', 'apply']:
        state["screening_mode"] = True
        state["step"] = 0
        return "Great! Let's start the screening process.\n\nPlease enter your **Full Name**:"
    
    # If in screening mode, handle the screening flow
    if state.get("screening_mode", False):
        step = state.get("step", 0)

        if step < len(FIELDS):
            field = FIELDS[step]
            
            # Advanced Features: Enhanced Sentiment & Language Analysis
            if ADVANCED_FEATURES and user_input.strip():
                sentiment_data = analyze_sentiment(user_input)
                language_data = detect_language(user_input)
                
                # Store enhanced data
                state[f"{field}_sentiment"] = sentiment_data
                state[f"{field}_language"] = language_data
                
                # Enhanced sentiment feedback with confidence
                if field == "Full Name":
                    if sentiment_data.get("sentiment") in ["positive", "very positive"]:
                        confidence = sentiment_data.get("confidence", 0)
                        st.success(f"😊 Great to meet you! Positive energy detected ({confidence}% confidence)")
                    elif "excited" in sentiment_data.get("emotions", []):
                        st.success("🎉 I can sense your excitement! That's wonderful!")
                        
                elif field == "Years of Experience":
                    if sentiment_data.get("sentiment") in ["negative", "very negative"]:
                        st.info("💪 Don't worry, every experience counts! Focus on your growth.")
                    elif "confident" in sentiment_data.get("emotions", []):
                        st.success("🚀 I can sense your confidence in your abilities!")
                        
                elif field == "Tech Stack":
                    if sentiment_data.get("sentiment") in ["positive", "very positive"]:
                        st.success("💻 Great enthusiasm for technology!")
                
                # Language detection feedback
                if isinstance(language_data, dict) and language_data.get("confidence", 0) > 80:
                    detected_lang = language_data.get("language", "en")
                    if detected_lang == "hi":
                        st.info("🇮🇳 Hindi detected! मैं हिंदी में भी मदद कर सकता हूँ।")
                    elif detected_lang == "es":
                        st.info("🇪🇸 Spanish detected! ¡También puedo ayudarte en español!")
                    elif detected_lang != "en":
                        st.info(f"🌍 Language detected: {detected_lang}")
            
            store_candidate_data(state, field, user_input)
            state["step"] += 1

            if state["step"] < len(FIELDS):
                next_field = FIELDS[state['step']]
                base_response = f"Thank you! Now please enter your **{next_field}**:"
                
                # Enhanced personalized response
                if ADVANCED_FEATURES:
                    user_data = {k: v for k, v in state.items() if not k.startswith(('step', 'screening_mode', 'technical_interview'))}
                    sentiment_data = state.get(f"{field}_sentiment", {"sentiment": "neutral", "emotions": []})
                    language_data = state.get(f"{field}_language", {"language": "en", "confidence": 100})
                    
                    personalized_response = get_personalized_response(
                        base_response, user_data, sentiment_data, language_data
                    )
                    return personalized_response
                
                return base_response
            else:
                # Screening completed - start technical interview
                state["screening_mode"] = False
                state["technical_interview"] = True
                tech_stack = state.get("Tech Stack", "")
                user_name = state.get("Full Name", "")
                
                if tech_stack:
                    state["current_tech"] = 0
                    state["current_question"] = 0
                    
                    # Get first technical question
                    first_q = get_next_technical_question(state)
                    if first_q:
                        base_message = (
                            f"Perfect! 🎉 Basic information collected successfully!\n\n"
                            f"Now let's proceed with some technical questions based on your tech stack: **{tech_stack}**\n\n"
                            f"**{first_q['tech']} Question:**\n\n{first_q['question']}"
                        )
                        
                        # Add personalization
                        if ADVANCED_FEATURES and user_name:
                            sentiment_data = {"sentiment": "positive"}  # Completion is positive
                            detected_lang = state.get("Tech Stack_language", "en")
                            
                            personalized_message = get_personalized_response(
                                base_message, user_name, sentiment_data, detected_lang
                            )
                            return personalized_message
                        
                        return base_message
                    else:
                        return (
                            "Thank you for completing the screening! 🎉\n\n"
                            "Our team will review your application and contact you soon.\n\n"
                            "Feel free to ask me any other questions!"
                        )
                else:
                    return (
                        "Thank you for completing the screening! 🎉\n\n"
                        "Our team will review your application and contact you soon.\n\n"
                        "Feel free to ask me any other questions!\n\n"
                        "💡 *Type 'exit' or 'bye' when you want to end the conversation.*"
                    )
    
    # Handle technical interview mode
    if state.get("technical_interview", False):
        # Store the answer
        current_tech = state.get("current_tech", 0)
        current_question = state.get("current_question", 0) - 1  # -1 because we incremented it
        
        if current_question >= 0:
            answer_key = f"tech_answer_{current_tech}_{current_question}"
            state[answer_key] = user_input
        
        # Get next question
        next_q = get_next_technical_question(state)
        
        if next_q:
            return f"Thank you for your answer! 👍\n\n**{next_q['tech']} Question:**\n\n{next_q['question']}"
        else:
            # Technical interview completed
            state["technical_interview"] = False
            return (
                "Excellent! 🎉 Technical interview completed successfully!\n\n"
               
                "**Next Steps:**\n"
                "• Our technical team will review your answers\n"
                "• HR team will contact you within 2-3 business days\n"
                "• You may receive a follow-up technical interview invitation\n\n"
                "Thank you for your time and interest in TalentScout! 🚀\n\n"
                "Feel free to ask me any other questions about careers, jobs, or technology!"
            )
    
    # Fallback mechanism for unclear inputs during screening
    if state.get("screening_mode", False):
        return (
            "I didn't quite understand that. Could you please provide a clear answer to the current question?\n\n"
            "If you want to exit the conversation, type 'exit'."
        )
    
    # If not in screening mode, use AI to respond to general questions
    else:
        # Get AI response for general questions
        candidate_context = ""
        if len(state) > 1:  # If we have candidate data
            candidate_context = f"Candidate info: {', '.join([f'{k}: {v}' for k, v in state.items() if k not in ['step', 'screening_mode', 'technical_questions_mode', 'technical_questions', 'current_question', 'technical_answers']])}"
        
        ai_response = get_ai_response(user_input, candidate_context)
        return ai_response

# Custom CSS for enhanced styling
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Global Styles with Background Image */
    .stApp {
        background: 
            linear-gradient(135deg, rgba(15, 23, 42, 0.95) 0%, rgba(30, 41, 59, 0.9) 50%, rgba(51, 65, 85, 0.85) 100%),
            url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><defs><pattern id="grid" width="10" height="10" patternUnits="userSpaceOnUse"><path d="M 10 0 L 0 0 0 10" fill="none" stroke="%23334155" stroke-width="0.5" opacity="0.2"/></pattern></defs><rect width="100" height="100" fill="url(%23grid)"/></svg>'),
            radial-gradient(circle at 20% 80%, rgba(59, 130, 246, 0.15) 0%, transparent 50%),
            radial-gradient(circle at 80% 20%, rgba(168, 85, 247, 0.15) 0%, transparent 50%);
        background-attachment: fixed;
        background-size: cover, 50px 50px, 800px 800px, 600px 600px;
        font-family: 'Inter', sans-serif;
        min-height: 100vh;
    }
    
    /* Main container with glass effect */
    .main > div {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(15px);
        border-radius: 20px;
        padding: 2.5rem;
        margin: 1rem;
        box-shadow: 
            0 8px 32px rgba(0, 0, 0, 0.3),
            0 4px 16px rgba(0, 0, 0, 0.2),
            inset 0 1px 0 rgba(255, 255, 255, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.1);
        position: relative;
    }
    
    /* Professional header styling */
    .main-title {
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
    }
    
    .main-title::after {
        content: '';
        position: absolute;
        bottom: -10px;
        left: 50%;
        transform: translateX(-50%);
        width: 80px;
        height: 3px;
        background: linear-gradient(90deg, #3b82f6, #a855f7);
        border-radius: 2px;
    }
    
    .subtitle {
        text-align: center;
        color: #e2e8f0;
        font-size: 1.2rem;
        margin-bottom: 3rem;
        font-weight: 500;
        opacity: 0.9;
    }
    
    /* Enhanced chat message styling */
    .stChatMessage {
        padding: 1.8rem;
        border-radius: 16px;
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.08);
        border: 1px solid rgba(255, 255, 255, 0.3);
        backdrop-filter: blur(5px);
        position: relative;
        overflow: hidden;
    }
    
    .stChatMessage::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.5), transparent);
    }
    
    /* Ensure all chat message text is white */
    .stChatMessage p, 
    .stChatMessage div, 
    .stChatMessage span,
    .stChatMessage strong,
    .stChatMessage em {
        color: #ffffff !important;
    }
    
    /* Fix text visibility in main content */
    .main .element-container p,
    .main .element-container div,
    .main .element-container span,
    .main .element-container h1,
    .main .element-container h2,
    .main .element-container h3 {
        color: #ffffff !important;
    }
    
    /* User message with same background as assistant */
    .stChatMessage[data-testid="user-message"] {
        background: rgba(59, 130, 246, 0.2) !important;
        backdrop-filter: blur(10px);
        color: #ffffff !important;
        margin-left: 3rem;
        border: 1px solid rgba(59, 130, 246, 0.3);
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.2);
    }
    
    /* Assistant message with same background */
    .stChatMessage[data-testid="assistant-message"] {
        background: rgba(168, 85, 247, 0.2) !important;
        backdrop-filter: blur(10px);
        color: #ffffff !important;
        margin-right: 3rem;
        border: 1px solid rgba(168, 85, 247, 0.3);
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.2);
    }
    
    /* Professional chat input */
    .stChatInputContainer {
        padding-top: 1.5rem;
        background: transparent;
    }
    
    .stChatInput > div {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(15px);
        border-radius: 16px;
        border: 2px solid rgba(255, 255, 255, 0.2);
        box-shadow: 
            0 4px 16px rgba(0, 0, 0, 0.2),
            inset 0 1px 0 rgba(255, 255, 255, 0.1);
        transition: all 0.3s ease;
    }
    
    .stChatInput > div:focus-within {
        border-color: #3b82f6;
        box-shadow: 
            0 0 0 4px rgba(59, 130, 246, 0.25),
            0 6px 20px rgba(59, 130, 246, 0.3);
        transform: translateY(-2px);
    }
    
    /* Chat input text styling */
    .stChatInput input {
        color: #f1f5f9 !important;
        background: transparent !important;
    }
    
    .stChatInput input::placeholder {
        color: rgba(241, 245, 249, 0.6) !important;
    }
    
    /* Enhanced sidebar styling */
    .css-1d391kg {
        background: linear-gradient(180deg, rgba(45, 55, 72, 0.95) 0%, rgba(26, 32, 44, 0.95) 100%);
        backdrop-filter: blur(10px);
    }
    
    .sidebar-content {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(10px);
        padding: 2rem;
        border-radius: 16px;
        margin: 1rem;
        box-shadow: 
            0 8px 32px rgba(0, 0, 0, 0.15),
            inset 0 1px 0 rgba(255, 255, 255, 0.8);
        border: 1px solid rgba(255, 255, 255, 0.3);
    }
    
    .candidate-info {
        background: rgba(30, 41, 59, 0.9) !important;
        backdrop-filter: blur(5px);
        padding: 1.2rem;
        border-radius: 12px;
        margin: 0.8rem 0;
        border-left: 4px solid #4299e1;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
        transition: transform 0.2s ease;
        color: #ffffff !important;
    }
    
    .candidate-info strong {
        color: #60a5fa !important;
    }
    
    .candidate-info:hover {
        transform: translateX(4px);
    }
    
    /* Enhanced progress indicator */
    .progress-container {
        background: rgba(30, 41, 59, 0.9) !important;
        backdrop-filter: blur(5px);
        padding: 1.5rem;
        border-radius: 12px;
        margin-bottom: 1.5rem;
        text-align: center;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.08);
        border: 1px solid rgba(59, 130, 246, 0.3);
        color: #ffffff !important;
    }
    
    .progress-container strong {
        color: #60a5fa !important;
    }
    
    .progress-bar {
        background: linear-gradient(90deg, #4299e1 0%, #48bb78 50%, #3182ce 100%);
        height: 10px;
        border-radius: 6px;
        margin: 0.8rem 0;
        transition: width 0.5s ease;
        box-shadow: 0 2px 8px rgba(66, 153, 225, 0.3);
    }
    
    /* Professional button styling */
    .stButton > button {
        background: linear-gradient(135deg, #4299e1 0%, #3182ce 100%);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.8rem 2.5rem;
        font-weight: 600;
        font-size: 1rem;
        box-shadow: 
            0 4px 16px rgba(66, 153, 225, 0.3),
            inset 0 1px 0 rgba(255, 255, 255, 0.2);
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .stButton > button::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
        transition: left 0.5s ease;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #3182ce 0%, #2c5282 100%);
        transform: translateY(-3px);
        box-shadow: 
            0 8px 24px rgba(66, 153, 225, 0.4),
            inset 0 1px 0 rgba(255, 255, 255, 0.3);
    }
    
    .stButton > button:hover::before {
        left: 100%;
    }
    
    /* Smooth animations */
    @keyframes fadeInUp {
        from { 
            opacity: 0; 
            transform: translateY(30px);
        }
        to { 
            opacity: 1; 
            transform: translateY(0);
        }
    }
    
    @keyframes slideInRight {
        from {
            opacity: 0;
            transform: translateX(30px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    .fade-in-up {
        animation: fadeInUp 0.8s ease-out;
    }
    
    .slide-in-right {
        animation: slideInRight 0.6s ease-out;
    }
    
    /* Responsive design enhancements */
    @media (max-width: 768px) {
        .main-title {
            font-size: 2.2rem;
        }
        .main > div {
            margin: 0.5rem;
            padding: 1.5rem;
        }
        .stChatMessage[data-testid="user-message"] {
            margin-left: 1rem;
        }
        .stChatMessage[data-testid="assistant-message"] {
            margin-right: 1rem;
        }
    }
    
    /* Loading animation */
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.5; }
    }
    
    .loading {
        animation: pulse 2s infinite;
    }
</style>
""", unsafe_allow_html=True)

# Main App Header
st.markdown('<h1 class="main-title fade-in-up">🤖 TalentScout Hiring Assistant</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle slide-in-right">AI-Powered Recruitment Screening</p>', unsafe_allow_html=True)

# Initialize session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "state" not in st.session_state:
    st.session_state.state = {}

# Enhanced sidebar with features showcase
with st.sidebar:
    st.markdown('<div class="sidebar-content">', unsafe_allow_html=True)
    
    # Features showcase
    st.markdown("### 🚀 Advanced Features")
    
    if ADVANCED_FEATURES:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    padding: 1rem; border-radius: 10px; margin-bottom: 1rem; color: white;">
            <h4 style="margin: 0; color: white;">✨ AI-Powered Features Active</h4>
            <ul style="margin: 0.5rem 0; padding-left: 1.2rem;">
                <li>🧠 <strong>Sentiment Analysis</strong><br>
                    <small>Detects emotions & adapts responses</small></li>
                <li>🌍 <strong>Multilingual Support</strong><br>
                    <small>Hindi, Spanish, French & more</small></li>
                <li>🎯 <strong>Personalized Responses</strong><br>
                    <small>Tailored based on your profile</small></li>
                <li>🤖 <strong>Google Gemini AI</strong><br>
                    <small>Smart conversational responses</small></li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="background: #f39c12; padding: 1rem; border-radius: 10px; margin-bottom: 1rem; color: white;">
            <h4 style="margin: 0; color: white;">⚠️ Basic Mode</h4>
            <p style="margin: 0.5rem 0; font-size: 0.9rem;">
                Advanced features unavailable. Install required packages for full functionality.
            </p>
        </div>
        """, unsafe_allow_html=True)

# Show candidate info sidebar if data exists
if st.session_state.state and len(st.session_state.state) > 1:  # More than just 'step'
    with st.sidebar:
        st.markdown("### 📋 Candidate Information")
        
        # Progress indicator
        current_step = st.session_state.state.get('step', 0)
        progress = min(current_step / len(FIELDS), 1.0) * 100
        
        st.markdown(f"""
        <div class="progress-container">
            <strong>Progress: {current_step}/{len(FIELDS)} fields completed</strong>
            <div style="background: #e0e0e0; border-radius: 4px; height: 8px; margin: 0.5rem 0;">
                <div class="progress-bar" style="width: {progress}%;"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Display collected information
        for field in FIELDS:
            if field in st.session_state.state:
                st.markdown(f"""
                <div class="candidate-info">
                    <strong>{field}:</strong><br>
                    {st.session_state.state[field]}
                </div>
                """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Add reset button
        if st.button("🔄 Start Over"):
            st.session_state.chat_history = []
            st.session_state.state = {}
            st.rerun()

# Display chat history
for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Chat input
user_input = st.chat_input("Type your response...")

if user_input:
    # Add user message to history
    st.session_state.chat_history.append({"role": "user", "content": user_input})
    
    # Get bot response
    response = get_bot_response(user_input, st.session_state.state)
    
    # Add bot response to history
    st.session_state.chat_history.append({"role": "assistant", "content": response})
    
    # Rerun to update the display
    st.rerun()

# Show initial greeting if no chat history
if not st.session_state.chat_history:
    with st.chat_message("assistant"):
        initial_message = get_bot_response("", st.session_state.state)
        st.markdown(initial_message)
        st.session_state.chat_history.append({"role": "assistant", "content": initial_message})

# Footer removed as requested
