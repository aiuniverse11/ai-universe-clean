from flask import Flask, request, jsonify
from flask_cors import CORS
from groq import Groq
import os

app = Flask(__name__)
CORS(app)

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

@app.route("/")
def home():
    return jsonify({
        "status": "online",
        "message": "AI Universe Backend is running!"
    })

@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.json
        message = data.get("message", "")

        completion = client.chat.completions.create(
            model="llama3-70b-8192",
            messages=[
                {
                    "role": "user",
                    "content": message
                }
            ]
        )

        reply = completion.choices[0].message.content

        return jsonify({
            "reply": reply
        })

    except Exception as e:
        return jsonify({
            "reply": f"Error: {str(e)}"
        })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)