# 🤖 TalentScout Hiring Assistant

An AI-powered recruitment screening chatbot built with Streamlit and Google GenAI that streamlines the initial candidate screening process through intelligent conversation and automated technical question generation.

## ✨ Features

### Core Functionality
- **Interactive Candidate Screening**: Conversational interface for collecting essential candidate information
- **AI-Powered Responses**: Intelligent responses using Google's Gemini AI model
- **Technical Question Generation**: Automatic generation of relevant technical questions based on candidate's tech stack
- **Real-time Data Collection**: Seamless collection and storage of candidate information

### Advanced Features
- **Sentiment Analysis**: Analyzes candidate responses to adapt conversation tone
- **Multi-language Support**: Detects and responds in candidate's preferred language
- **Personalized Responses**: Customizes responses based on candidate data and sentiment
- **Professional UI**: Modern glass-morphism design with smooth animations
- **Progress Tracking**: Visual progress indicators and candidate information sidebar

### Supported Technologies
The system includes pre-built technical questions for:
- Python, JavaScript, React, Java, SQL
- Django, Node.js, MongoDB, Git, Docker
- And generic questions for any other technologies

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- Google Cloud API key with Gemini API access

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd talentscout-hiring-assistant
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   Create a `.env` file in the project root:
   ```env
   GOOGLE_API_KEY=your_google_api_key_here
   ```

4. **Run the application**
   ```bash
   streamlit run app.py
   ```

5. **Access the application**
   Open your browser and navigate to `http://localhost:8501`

## 📋 Usage

### For Candidates
1. **Start Screening**: The chatbot automatically begins the screening process
2. **Provide Information**: Answer questions about your background and experience
3. **Technical Questions**: Receive personalized technical questions based on your tech stack
4. **Complete Process**: Review your responses and await HR contact

### For HR Teams
1. **Monitor Progress**: View candidate information in real-time via the sidebar
2. **Review Responses**: Access all collected data and technical question answers
3. **Export Data**: Candidate information is stored in session state for processing

## 🛠️ Configuration

### Environment Variables
```env
GOOGLE_API_KEY=your_google_genai_api_key
```

### Customization Options
- **Add New Technologies**: Extend `TECH_QUESTIONS` dictionary in `app.py`
- **Modify Fields**: Update `FIELDS` list to change collected information
- **Customize Styling**: Modify CSS in the `st.markdown` section
- **Language Support**: Extend translation dictionaries for additional languages

## 📁 Project Structure

```
talentscout-hiring-assistant/
├── app.py                          # Main Streamlit application
├── chatbot.py                      # Core chatbot logic
├── config.py                       # Configuration settings
├── data_handler.py                 # Data processing utilities
├── prompts.py                      # AI prompt templates
├── tech_questions.py               # Technical question database
├── utils.py                        # Utility functions
├── requirements.txt                # Python dependencies
├── .env                           # Environment variables
├── test_advanced_features.py       # Advanced features testing
├── test_import.py                 # Import testing
├── ADVANCED_FEATURES_SUMMARY.md    # Advanced features documentation
└── .kiro/                         # Kiro IDE configuration
    └── specs/
        └── hiring-assistant-chatbot/
            └── requirements.md     # Detailed requirements
```

## 🔧 Technical Details

### Dependencies
- **streamlit**: Web application framework
- **google-genai**: Google's Generative AI client
- **python-dotenv**: Environment variable management
- **textblob**: Natural language processing for sentiment analysis
- **langdetect**: Language detection for multilingual support

### Architecture
- **Frontend**: Streamlit web interface with custom CSS styling
- **Backend**: Python-based conversation logic with state management
- **AI Integration**: Google Gemini API for intelligent responses
- **Data Flow**: Session-based state management with real-time updates

## 🎨 UI Features

### Design Elements
- **Glass Morphism**: Modern translucent design with backdrop blur effects
- **Gradient Backgrounds**: Dynamic color gradients with geometric patterns
- **Smooth Animations**: CSS animations for enhanced user experience
- **Responsive Design**: Mobile-friendly interface with adaptive layouts

### Interactive Components
- **Progress Indicators**: Visual progress bars showing completion status
- **Sidebar Information**: Real-time display of collected candidate data
- **Chat Interface**: Professional chat UI with role-based message styling
- **Input Validation**: Real-time validation with helpful error messages

## 🧪 Testing

### Run Tests
```bash
# Test advanced features
python test_advanced_features.py

# Test imports and dependencies
python test_import.py
```

### Test Coverage
- Sentiment analysis functionality
- Language detection and translation
- Technical question generation
- Data validation and storage
- AI response generation

## 🔒 Security & Privacy

### Data Protection
- Session-based data storage (no persistent storage by default)
- Environment variable protection for API keys
- Input validation and sanitization
- Secure API communication with Google GenAI

### Best Practices
- API key stored in environment variables
- No sensitive data logged or exposed
- Graceful error handling for API failures
- Input validation for all user data

## 🚀 Deployment

### Local Development
```bash
streamlit run app.py
```

### Production Deployment
1. **Streamlit Cloud**: Deploy directly from GitHub repository
2. **Docker**: Containerize the application for cloud deployment
3. **Heroku**: Deploy using Heroku's Python buildpack
4. **AWS/GCP**: Deploy on cloud platforms with proper environment configuration

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

### Common Issues

**API Key Not Working**
- Verify your Google Cloud API key is correct
- Ensure Gemini API is enabled in your Google Cloud project
- Check API quotas and billing settings

**Dependencies Not Installing**
- Upgrade pip: `pip install --upgrade pip`
- Use virtual environment: `python -m venv venv`
- Install from requirements: `pip install -r requirements.txt`

**Streamlit Not Starting**
- Check Python version (3.8+ required)
- Verify Streamlit installation: `streamlit --version`
- Run with module flag: `python -m streamlit run app.py`

### Contact
For support and questions, please open an issue in the repository or contact the development team.

---

**TalentScout Hiring Assistant** - Revolutionizing recruitment through AI-powered conversation 🚀