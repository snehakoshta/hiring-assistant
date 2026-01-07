# Streamlit.io Deployment Guide

## Prerequisites
1. GitHub account
2. Google API Key for Gemini AI
3. Streamlit Community Cloud account (free)

## Step-by-Step Deployment

### 1. Push Code to GitHub
```bash
git init
git add .
git commit -m "Initial commit - TalentScout Hiring Assistant"
git branch -M main
git remote add origin https://github.com/yourusername/your-repo-name.git
git push -u origin main
```

### 2. Get Google API Key
1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create a new API key
3. Copy the API key (you'll need it for deployment)

### 3. Deploy on Streamlit Community Cloud
1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Sign in with GitHub
3. Click "New app"
4. Select your repository
5. Set main file path: `app.py`
6. Click "Advanced settings"
7. Add secrets:
   ```
   GOOGLE_API_KEY = "your_actual_api_key_here"
   ```
8. Click "Deploy"

### 4. App Configuration
- **Main file**: `app.py`
- **Python version**: 3.9+ (automatically detected)
- **Dependencies**: Automatically installed from `requirements.txt`

### 5. Environment Variables (Secrets)
In Streamlit Cloud dashboard, add these secrets:
```toml
GOOGLE_API_KEY = "your_google_api_key_here"
```

## Features Included
- ✅ AI-powered hiring assistant
- ✅ Multi-language support (Hindi/English)
- ✅ Sentiment analysis
- ✅ Technical interview questions
- ✅ Professional UI with glassmorphism design
- ✅ Responsive design for mobile/desktop

## Local Development
```bash
# Install dependencies
pip install -r requirements.txt

# Create .env file
echo "GOOGLE_API_KEY=your_api_key_here" > .env

# Run locally
streamlit run app.py
```

## Troubleshooting

### Common Issues:
1. **API Key Error**: Make sure GOOGLE_API_KEY is set in Streamlit secrets
2. **Import Errors**: All dependencies are in requirements.txt
3. **Deployment Fails**: Check Python version compatibility

### Support:
- Streamlit Community: [discuss.streamlit.io](https://discuss.streamlit.io)
- Documentation: [docs.streamlit.io](https://docs.streamlit.io)

## App URL
After deployment, your app will be available at:
`https://your-app-name.streamlit.app`