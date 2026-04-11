import os

from dotenv import load_dotenv
from flask import Flask, jsonify, render_template, request

from agent import WELCOME_MESSAGE, chat_once

load_dotenv()

app = Flask(__name__, template_folder="template")


@app.get("/")
def home():
    return render_template("home.html", welcome_message=WELCOME_MESSAGE)


@app.post("/chat")
def chat():
    data = request.get_json(silent=True) or {}
    message = (data.get("message") or "").strip()

    if not message:
        return jsonify({"error": "Please enter a message."}), 400

    try:
        reply = chat_once(message)
    except Exception:
        return jsonify({"error": "Something went wrong. Please try again."}), 500

    return jsonify({"reply": reply})


if __name__ == "__main__":
    app.run(debug=True)
