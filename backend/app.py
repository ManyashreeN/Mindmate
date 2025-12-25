"""
MindMate Backend - Flask API for AI Chat Support
Integrates with Google Gemini API for empathetic student wellbeing support
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
#from google import genai
import os
from datetime import datetime
import re
from dotenv import load_dotenv

# Load environment variables from .env file
#load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), ".env"))



# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for frontend requests

# Configure Gemini API
#GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
#print("GEMINI_API_KEY loaded:", bool(GEMINI_API_KEY))
#if not GEMINI_API_KEY:
   # print("WARNING: GEMINI_API_KEY not set. Gemini responses will not work.")

#client = genai.Client(api_key=GEMINI_API_KEY)
# System prompt that defines MindMate's behavior
SYSTEM_PROMPT = """You are MindMate, a compassionate AI friend supporting college students during stressful times. Your role is to listen, understand, and provide emotional support - NOT medical or therapeutic advice.

Your behavior:
1. **Listen First**: Acknowledge their feelings without judgment
2. **Respond Gently**: Be warm, empathetic, and human-like
3. **Ask Follow-ups**: Ask gentle questions to help them express themselves
4. **Stay Within Bounds**: Never provide diagnosis, medical advice, or therapy
5. **Be Supportive**: Validate their struggles, especially around academics and placements
6. **Suggest Help When Needed**: If they express severe distress, suggest reaching out to a trusted adult or professional

Tone: Friendly, like a caring senior or friend - not robotic or clinical.

Examples of good responses:
- "That sounds really stressful. Tell me, what part is bothering you the most?"
- "It's okay to feel overwhelmed sometimes. Many students go through this."
- "I hear you. Have you talked to anyone about this?"

Topics to be supportive about:
- Placement anxiety and interview stress
- Academic pressure and exam fear
- Imposter syndrome and self-doubt
- Social anxiety and loneliness
- Career confusion and future uncertainty
- Work-life balance and burnout

Distress indicators to watch for:
- Mentions of self-harm or suicide
- Extreme hopelessness or despair
- Severe anxiety or panic attacks
- Substance abuse mentions
- Abuse or trauma disclosure

When distress is detected: Acknowledge their pain, suggest professional help, and provide this message:
"I'm concerned about what you're going through. Please reach out to a trusted adult, school counselor, or a mental health professional. Your wellbeing matters. 💙"

Keep responses concise (2-3 sentences) unless more detail is needed. Be genuine."""

# List of distress keywords to detect severe emotional states
DISTRESS_KEYWORDS = [
    "suicide", "self-harm", "kill myself", "end it all", "no point",
    "hopeless", "worthless", "can't take it", "nobody cares", "alone forever",
    "scared", "panic", "terrified", "panic attack", "anxiety attack",
    "abusive", "abuse", "assault", "harassed", "bullied",
    "drug", "drugs", "alcohol", "drinking", "high", "drunk",
    "depressed", "depression", "suicidal", "die"
]


def detect_distress(message):
    """
    Check if the message contains indicators of severe distress
    Returns True if distress is detected
    """
    message_lower = message.lower()
    for keyword in DISTRESS_KEYWORDS:
        if keyword in message_lower:
            return True
    return False


def generate_safety_warning():
    """Generate a crisis support message"""
    return {
        "warning": True,
        "message": "I'm concerned about what you're sharing. Please reach out to a trusted adult, school counselor, or a mental health professional. Your wellbeing truly matters. 💙",
        "resources": [
            "Talk to your college counseling center",
            "National Suicide Prevention Lifeline: 988 (US)",
            "Crisis Text Line: Text HOME to 741741",
            "International Association for Suicide Prevention: https://www.iasp.info/resources/Crisis_Centres/"
        ]
    }

def call_gemini_api(user_message):
    try:
        import google.generativeai as genai

        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            return "Gemini API key is not configured."

        genai.configure(api_key=api_key)

        model = genai.GenerativeModel("gemini-pro")

        full_message = (
            f"{SYSTEM_PROMPT}\n\n"
            f"User says: {user_message}\n\n"
            f"Respond as MindMate:"
        )

        response = model.generate_content(full_message)
        return response.text.strip()

    except Exception as e:
        print("Gemini error:", e)
        return "I'm having trouble responding right now. Please try again later 💙"

@app.route("/")
def root():
    return "MindMate backend running", 200


@app.route("/health", methods=["GET"])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "service": "MindMate Backend",
        "timestamp": datetime.now().isoformat()
    }), 200


@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()

    if not data or "message" not in data:
        return jsonify({
            "reply": "Please enter a message so I can help you 💙",
            "warning": False
        }), 400

    user_message = data.get("message", "").strip()

    if not user_message:
        return jsonify({
            "reply": "I didn’t catch that. Could you try typing it again?",
            "warning": False
        }), 400

    distress_detected = detect_distress(user_message)
    ai_response = call_gemini_api(user_message)

    response = {
        "reply": ai_response,
        "warning": distress_detected
    }

    if distress_detected:
        safety_info = generate_safety_warning()
        response["safetyMessage"] = safety_info["message"]
        response["resources"] = safety_info["resources"]

    return jsonify(response), 200



@app.route("/chat-history", methods=["GET"])
def get_chat_history():
    """
    Get chat history for a user (placeholder for Firestore integration)
    Future: Store and retrieve from Firestore
    """
    return jsonify({
        "message": "Chat history feature coming soon with Firestore integration",
        "status": "placeholder"
    }), 200


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({
        "error": "Endpoint not found",
        "status": 404
    }), 404


@app.errorhandler(500)
def server_error(error):
    """Handle 500 errors"""
    return jsonify({
        "error": "Internal server error",
        "status": 500
    }), 500


if __name__ == "__main__":
    # Development server
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
