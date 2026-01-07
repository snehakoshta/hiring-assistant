#!/usr/bin/env python3
"""
Fallback responses for when AI quota is exceeded
"""

def get_fallback_response(user_message, context=""):
    """
    Provide intelligent fallback responses without using AI
    """
    user_lower = user_message.lower().strip()
    
    # Greeting responses
    greetings = ["hello", "hi", "hey", "good morning", "good afternoon", "good evening", "namaste"]
    if any(greeting in user_lower for greeting in greetings):
        return "Hello! 👋 Welcome to TalentScout - Your AI-Powered Hiring Assistant. I'm here to help you with job applications and career opportunities.\n\n**Type 'start screening' to begin your application process!**"
    
    # Excitement/Positive responses
    positive_words = ["excited", "happy", "great", "awesome", "wonderful", "amazing", "fantastic"]
    if any(word in user_lower for word in positive_words):
        return "That's wonderful to hear! 🎉 Your enthusiasm is exactly what employers love to see. Let me help you channel that excitement into your job search.\n\n**Type 'start screening' to begin your application!**"
    
    # Nervous/Anxious responses
    nervous_words = ["nervous", "worried", "scared", "anxious", "concerned", "afraid"]
    if any(word in user_lower for word in nervous_words):
        return "It's completely normal to feel that way about job applications! 💪 Take a deep breath - I'm here to guide you through the process step by step.\n\n**Type 'start screening' to begin at your own pace.**"
    
    # Questions
    if "?" in user_message:
        if "job" in user_lower or "career" in user_lower:
            return "I'd love to help with your career questions! 🤔 I can assist you with job applications, resume tips, and interview preparation through our structured process.\n\n**Type 'start screening' to get personalized career guidance!**"
        elif "company" in user_lower or "talentscout" in user_lower:
            return "TalentScout is a modern recruitment platform that helps connect talented individuals with great opportunities! 🚀\n\n**Type 'start screening' to start your application process!**"
        else:
            return "I'd be happy to help answer that! 🤔 I specialize in job applications, career guidance, and interview preparation.\n\n**Type 'start screening' to get personalized assistance!**"
    
    # Start/Begin keywords
    start_words = ["start", "begin", "apply", "application", "screening"]
    if any(word in user_lower for word in start_words):
        return "Perfect! Let's get started with your job application. I'll collect some basic information and then ask relevant technical questions based on your skills.\n\n**Ready to begin? Type 'start screening'!**"
    
    # Technical/Skills related
    tech_words = ["python", "javascript", "java", "react", "node", "sql", "programming", "coding", "developer", "engineer"]
    if any(word in user_lower for word in tech_words):
        return "Great! I can see you have technical skills. 💻 Our screening process will include relevant technical questions based on your expertise.\n\n**Type 'start screening' to showcase your technical abilities!**"
    
    # Experience related
    exp_words = ["experience", "years", "worked", "job", "position", "role"]
    if any(word in user_lower for word in exp_words):
        return "Experience is valuable! 📈 Whether you're a beginner or seasoned professional, I'll help tailor the screening process to your background.\n\n**Type 'start screening' to share your experience!**"
    
    # Default response
    return "Welcome to TalentScout! 🚀 I'm here to help you with job applications and career opportunities.\n\n**What I can do:**\n• Collect your job application information\n• Ask relevant technical questions based on your skills\n• Provide career guidance\n• Help with interview preparation\n\n**Type 'start screening' to begin your application!**"

# Test the fallback system
if __name__ == "__main__":
    test_messages = [
        "Hello!",
        "I am very excited today",
        "I'm nervous about interviews",
        "What kind of jobs do you have?",
        "I know Python and JavaScript",
        "I have 5 years of experience",
        "start screening",
        "random message"
    ]
    
    print("🧪 Testing Fallback Response System")
    print("=" * 50)
    
    for msg in test_messages:
        response = get_fallback_response(msg)
        print(f"\nInput: '{msg}'")
        print(f"Response: {response[:100]}...")
        print("-" * 30)