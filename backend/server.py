# ============================================================
# AI Universe - Flask Backend Server
# ============================================================
# Installation Commands:
# pip install flask flask-cors groq
# ============================================================

# ------------------------------------------------------------
# IMPORTS
# ------------------------------------------------------------
from dotenv import load_dotenv
load_dotenv()
from flask import Flask, request, jsonify
from flask_cors import CORS
from groq import Groq
import os

# ------------------------------------------------------------
# FLASK SETUP
# ------------------------------------------------------------
app = Flask(__name__)

# Enable CORS for all routes and origins
# This allows your frontend (VS Code Live Server) to communicate with this backend
CORS(app)

# ------------------------------------------------------------
# GROQ CLIENT SETUP
# ------------------------------------------------------------
# Replace 'YOUR_GROQ_API_KEY' with your actual Groq API key
# You can get one from: https://console.groq.com
import os

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Initialize Groq client
client = Groq(api_key=GROQ_API_KEY)

# ------------------------------------------------------------
# SYSTEM PROMPT
# ------------------------------------------------------------
SYSTEM_PROMPT = """
You are AI Universe, an advanced AI assistant created to give direct, intelligent, accurate, and human-like answers.

Rules:
- Always answer clearly and confidently.
- Never say "based on available trends" or "I recommend cross-referencing".
- Give practical and useful answers.
- Speak naturally like ChatGPT.
- Help with coding, business, education, AI, editing, and technology.
- Keep responses modern, smart, and professional.
"""

# ------------------------------------------------------------
# AI CHAT ROUTE
# ------------------------------------------------------------
@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()
        user_message = data.get("message")

        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": user_message
                }
            ],
            model="llama-3.3-70b-versatile"
        )

        ai_reply = chat_completion.choices[0].message.content

        return jsonify({
            "reply": ai_reply
        })

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500
# ------------------------------------------------------------
# HEALTH CHECK ROUTE
# ------------------------------------------------------------
@app.route("/", methods=["GET"])
def home():
    """Health check endpoint"""
    return jsonify({
        "status": "online",
        "message": "AI Universe Backend is running!",
        "endpoints": {
            "chat": "POST /chat"
        }
    }), 200


# ------------------------------------------------------------
# SERVER START
# ------------------------------------------------------------

if __name__ == "__main__":
    print("=" * 50)
    print("AI Universe Backend Server")
    print("=" * 50)
    print("Server running...")
    print("=" * 50)

    port = int(os.environ.get("PORT", 5000))

    app.run(
        host="0.0.0.0",
        port=port,
        debug=True
    )