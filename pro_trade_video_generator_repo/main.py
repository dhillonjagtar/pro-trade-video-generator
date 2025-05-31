from flask import Flask, request, jsonify, send_file
from engine import generate_trade_video
import os

app = Flask(__name__)

@app.route("/generate", methods=["POST"])
def generate():
    user_prompt = request.json.get("prompt")
    output_path = generate_trade_video(user_prompt)
    return send_file(output_path, mimetype="video/mp4")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
