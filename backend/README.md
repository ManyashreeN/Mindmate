# MindMate Backend - Setup & Deployment Guide

## 📋 Overview

This Flask backend serves the MindMate AI chat feature using Google Gemini API. It provides:
- **POST /chat** - Main endpoint for receiving messages and returning AI responses
- **Distress Detection** - Identifies crisis keywords and triggers safety warnings
- **Empathetic AI** - Uses Gemini with a specialized system prompt for student support

---

## 🚀 Quick Start (Local Development)

### 1. Prerequisites
- Python 3.8+
- Google Gemini API Key (free) from https://makersuite.google.com/app/apikey
- pip (Python package manager)

### 2. Setup

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Linux/Mac:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file with your API key
cp .env.example .env
# Edit .env and add your GEMINI_API_KEY
```

### 3. Run Locally

```bash
python app.py
```

Backend runs on `http://localhost:8080`

---

## 🔧 Configuration

### Environment Variables (.env)

```
GEMINI_API_KEY=your_api_key_here
FLASK_ENV=development
FLASK_DEBUG=True
```

### Key Settings

| Setting | Purpose | Value |
|---------|---------|-------|
| GEMINI_API_KEY | Google Gemini API authentication | Your API key |
| FLASK_DEBUG | Enable debug mode | True (dev), False (prod) |
| FLASK_ENV | Environment | development/production |

---

## 📡 API Endpoints

### POST /chat

**Request:**
```json
{
  "message": "I'm feeling stressed about placements",
  "userId": "user_123" // optional, for analytics
}
```

**Response (Normal):**
```json
{
  "reply": "That sounds really stressful. Tell me, what part is bothering you the most?",
  "warning": false,
  "timestamp": "2025-12-23T10:30:00",
  "userId": "user_123"
}
```

**Response (Distress Detected):**
```json
{
  "reply": "I'm really concerned about what you're sharing...",
  "warning": true,
  "safetyMessage": "I'm concerned about what you're going through. Please reach out to...",
  "resources": [
    "Talk to your college counseling center",
    "National Suicide Prevention Lifeline: 988 (US)",
    "Crisis Text Line: Text HOME to 741741",
    "..."
  ],
  "timestamp": "2025-12-23T10:30:00",
  "userId": "user_123"
}
```

### GET /health

Health check endpoint. Returns status of backend.

---

## 🧠 AI Behavior & System Prompt

The backend uses a carefully designed system prompt that:

1. **Instructs Gemini** to act like a caring friend, not a therapist
2. **Defines boundaries** - no medical/therapy advice
3. **Lists distress keywords** - for detecting crisis situations
4. **Provides examples** - of good empathetic responses
5. **Sets tone** - friendly, human-like, supportive

Located in: `app.py` → `SYSTEM_PROMPT` variable

---

## ⚠️ Distress Detection

### How It Works

1. **Keyword Matching**: Message scanned for crisis keywords
   - Examples: "suicide", "self-harm", "hopeless", "abuse", etc.
2. **Automatic Trigger**: If detected → `warning = true`
3. **Safety Response**: Additional crisis resources provided
4. **AI Still Responds**: Gemini generates empathetic response too

### Distress Keywords (in app.py)

```python
DISTRESS_KEYWORDS = [
    "suicide", "self-harm", "kill myself", "end it all",
    "hopeless", "worthless", "can't take it",
    "panic attack", "anxiety attack",
    "abusive", "abuse", "assault",
    "drug", "drugs", "alcohol",
    # ... more in code
]
```

**Note:** Simple keyword matching is a placeholder. Future versions can use ML models for better detection.

---

## 🔐 Security & Privacy

### Privacy Features

✅ **No Personal Data Collection**
- Users are anonymous by default
- UserIds are randomly generated and stored locally in browser
- Messages not stored (placeholder implementation)

✅ **No Medical Advice**
- System prompt explicitly forbids diagnosis/therapy advice
- Safety disclaimer on frontend

✅ **CORS Enabled**
- Frontend can safely communicate with backend

### Security Measures

- Input validation (message length limits)
- HTML escaping on frontend
- Error handling without exposing system details
- API key kept in environment variables (not in code)

---

## 🌐 Frontend Integration

### Chat Interface (chat.html)

The frontend:
1. Gets user input from text field
2. Sends to `POST /chat` endpoint
3. Displays AI response with typing animation
4. Shows warning box if `warning: true`
5. Stores userId in localStorage for session continuity

### CORS Configuration

Backend has CORS enabled:
```python
CORS(app)  # Allows frontend requests
```

Adjust if deploying to production with specific domain.

---

## 📦 Deployment Options

### Option 1: Google Cloud Run (Recommended)

```bash
# Install Google Cloud CLI
# Authenticate
gcloud auth login

# Deploy
gcloud run deploy mindmate-backend \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars GEMINI_API_KEY=$YOUR_API_KEY
```

**Update frontend API_URL to your Cloud Run URL**

### Option 2: Heroku

```bash
# Create Procfile
echo "web: gunicorn app:app" > Procfile

# Deploy
heroku login
heroku create mindmate-backend
git push heroku main
heroku config:set GEMINI_API_KEY=$YOUR_API_KEY
```

### Option 3: Docker

```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8000", "app:app"]
```

---

## 🧪 Testing Endpoints

### Using curl

```bash
# Test health
curl http://localhost:8080/health

# Test chat
curl -X POST http://localhost:8080/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "I am stressed about placements", "userId": "test_user"}'

# Test distress detection
curl -X POST http://localhost:8080/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "I want to end it all", "userId": "test_user"}'
```

---

## 🐛 Troubleshooting

### Issue: "GEMINI_API_KEY not set"
**Solution:** Create `.env` file and add your Gemini API key

### Issue: CORS errors in browser
**Solution:** Ensure `CORS(app)` is in app.py and frontend uses correct API_URL

### Issue: Gemini API calls fail
**Solution:** 
- Check API key is valid
- Ensure API is enabled in Google Cloud Console
- Check rate limits (free tier has limits)

### Issue: Messages timing out
**Solution:** Gemini API responses can take 3-10 seconds. Check backend logs.

---

## 📝 Next Steps for Production

- [ ] Integrate Firebase Firestore for storing chat logs (anonymously)
- [ ] Improve distress detection with ML model
- [ ] Add rate limiting to prevent abuse
- [ ] Set up logging and monitoring
- [ ] Add conversation context (multi-turn chat memory)
- [ ] Cache popular responses for faster delivery
- [ ] Admin dashboard for reviewing safety incidents
- [ ] A/B testing for different system prompts

---

## 📚 Related Files

- `app.py` - Main Flask application
- `requirements.txt` - Python dependencies
- `.env.example` - Environment variables template
- `../frontend/chat.html` - Frontend chat interface
- `../frontend/index.html` - Main dashboard

---

## 👥 Team Contributions

**Member 2 (Backend):**
- ✅ Created Flask backend with /chat endpoint
- ✅ Integrated Google Gemini API
- ✅ Designed system prompt for empathetic AI behavior
- ✅ Implemented distress detection logic
- ✅ Added safety warnings & crisis resources
- ✅ Created API documentation

---

## 📞 Support

For issues or questions:
1. Check `.env` configuration
2. Review error logs in terminal
3. Test endpoints with curl first
4. Check Google Gemini API status

---

**Last Updated:** December 23, 2025  
**Status:** ✅ Ready for local testing and deployment
