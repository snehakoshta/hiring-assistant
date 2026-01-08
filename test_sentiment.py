#!/usr/bin/env python3
"""
Test sentiment analysis with specific input
"""

from textblob import TextBlob

def test_sentiment(text):
    """Test sentiment analysis for given text"""
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity
    subjectivity = blob.sentiment.subjectivity
    
    print(f'Input: "{text}"')
    print(f'Sentiment Polarity: {polarity:.3f}')
    print(f'Sentiment Subjectivity: {subjectivity:.3f}')
    print()
    print('Interpretation:')
    if polarity > 0.1:
        print('✅ POSITIVE sentiment detected')
        sentiment_type = "positive"
    elif polarity < -0.1:
        print('❌ NEGATIVE sentiment detected')
        sentiment_type = "negative"
    else:
        print('😐 NEUTRAL sentiment detected')
        sentiment_type = "neutral"
        
    print(f'Confidence: {abs(polarity):.1%}')
    
    return {
        'text': text,
        'polarity': polarity,
        'subjectivity': subjectivity,
        'sentiment': sentiment_type,
        'confidence': abs(polarity)
    }

if __name__ == "__main__":
    # Test the specific input
    test_input = "I am very excited about this opportunity!"
    result = test_sentiment(test_input)
    
    print("\n" + "="*50)
    print("Expected behavior according to requirements:")
    print("- System should detect positive sentiment")
    print("- System should respond with encouraging language")
    print("- System should store sentiment with candidate data")