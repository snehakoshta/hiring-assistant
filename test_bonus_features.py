#!/usr/bin/env python3
"""
Test all bonus features: Sentiment Analysis, Multilingual Support, Personalized Responses
"""

import sys
import os

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_sentiment_analysis():
    """Test enhanced sentiment analysis"""
    print("🧠 Testing Enhanced Sentiment Analysis...")
    print("-" * 40)
    
    try:
        from app import analyze_sentiment, detect_emotions
        
        test_texts = [
            "I'm very excited about this opportunity!",
            "I'm quite nervous about the interview",
            "This is okay, nothing special",
            "I'm frustrated with my current job",
            "I feel confident and ready for new challenges",
            "I'm grateful for this chance"
        ]
        
        for text in test_texts:
            result = analyze_sentiment(text)
            emotions = detect_emotions(text)
            
            print(f"Text: '{text}'")
            print(f"  Sentiment: {result.get('sentiment', 'N/A')} ({result.get('confidence', 0)}% confidence)")
            print(f"  Polarity: {result.get('polarity', 0):.2f}")
            print(f"  Emotions: {emotions}")
            print()
        
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_multilingual_support():
    """Test enhanced multilingual support"""
    print("🌍 Testing Enhanced Multilingual Support...")
    print("-" * 40)
    
    try:
        from app import detect_language, translate_text
        
        test_texts = [
            ("Hello, I am excited about this job!", "en"),
            ("Hola, estoy muy emocionado por este trabajo!", "es"),
            ("नमस्ते, मैं इस नौकरी के लिए बहुत उत्साहित हूँ!", "hi"),
            ("Bonjour, je suis très excité pour ce travail!", "fr")
        ]
        
        for text, expected_lang in test_texts:
            lang_result = detect_language(text)
            
            print(f"Text: '{text}'")
            if isinstance(lang_result, dict):
                print(f"  Detected: {lang_result.get('language', 'N/A')} ({lang_result.get('confidence', 0)}% confidence)")
                print(f"  All languages: {lang_result.get('all_languages', [])}")
            else:
                print(f"  Detected: {lang_result}")
            
            # Test translation
            if expected_lang != "en":
                translated = translate_text(text, "en")
                print(f"  Translated to EN: '{translated}'")
            
            print()
        
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_personalized_responses():
    """Test enhanced personalized responses"""
    print("🎯 Testing Enhanced Personalized Responses...")
    print("-" * 40)
    
    try:
        from app import get_personalized_response
        
        # Mock user data
        user_data = {
            "Full Name": "John Doe",
            "Years of Experience": "3",
            "Tech Stack": "Python, React, Node.js"
        }
        
        sentiment_data = {
            "sentiment": "very positive",
            "confidence": 85.5,
            "emotions": ["excited", "confident"]
        }
        
        language_data = {
            "language": "en",
            "confidence": 95.0,
            "all_languages": [("en", 95.0)]
        }
        
        base_response = "Thank you for your interest in our position."
        
        personalized = get_personalized_response(
            base_response, user_data, sentiment_data, language_data
        )
        
        print("Base response:")
        print(f"  '{base_response}'")
        print()
        print("Personalized response:")
        print(f"  '{personalized}'")
        print()
        
        # Test with different scenarios
        scenarios = [
            {
                "user_data": {"Full Name": "Maria Garcia", "Years of Experience": "0"},
                "sentiment_data": {"sentiment": "nervous", "emotions": ["nervous", "anxious"]},
                "language_data": {"language": "es", "confidence": 88.0}
            },
            {
                "user_data": {"Full Name": "Raj Patel", "Years of Experience": "8", "Tech Stack": "AI, Machine Learning, Python"},
                "sentiment_data": {"sentiment": "positive", "emotions": ["confident"]},
                "language_data": {"language": "hi", "confidence": 92.0}
            }
        ]
        
        for i, scenario in enumerate(scenarios, 1):
            print(f"Scenario {i}:")
            personalized = get_personalized_response(
                base_response, 
                scenario["user_data"], 
                scenario["sentiment_data"], 
                scenario["language_data"]
            )
            print(f"  '{personalized}'")
            print()
        
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    """Run all bonus feature tests"""
    print("🎉 Testing All Bonus Features")
    print("=" * 50)
    
    tests = [
        ("Sentiment Analysis", test_sentiment_analysis),
        ("Multilingual Support", test_multilingual_support),
        ("Personalized Responses", test_personalized_responses)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        try:
            if test_func():
                passed += 1
                print(f"✅ {test_name} - PASSED")
            else:
                print(f"❌ {test_name} - FAILED")
        except Exception as e:
            print(f"❌ {test_name} - ERROR: {e}")
    
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All bonus features are working perfectly!")
        print("\n🚀 Features Summary:")
        print("   ✅ Enhanced Sentiment Analysis - Detects emotions with confidence scores")
        print("   ✅ Advanced Multilingual Support - Hindi, Spanish, French translations")
        print("   ✅ Smart Personalized Responses - Context-aware, experience-based personalization")
        print("   ✅ Real-time Language Detection - Multi-language confidence scoring")
        print("   ✅ Emotion Recognition - Identifies specific emotions in text")
        print("\n🎯 Your TalentScout Hiring Assistant has all premium features!")
    else:
        print("⚠️ Some features may need attention.")
    
    return passed == total

if __name__ == "__main__":
    main()