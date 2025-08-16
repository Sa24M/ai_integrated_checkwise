from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from grader_ai import grade_with_ai
import os

app = Flask(__name__, static_folder="static", template_folder="templates")
CORS(app)

UPLOAD_FOLDER = os.path.join(os.getcwd(), "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/grade_ai", methods=["POST"])
def grade_ai_route():
    question = request.form.get("question")
    zip_file = request.files.get("zipfile")  # ✅ consistent key

    if not question or not zip_file:
        return jsonify({"error": "Question text and zip file are required"}), 400

    zip_bytes = zip_file.read()

    try:
        df, _ = grade_with_ai(zip_bytes, question, uploads_dir=UPLOAD_FOLDER)
        return df.to_json(orient="records")
    except Exception as e:
        if "Gemini API error" in str(e):
            return jsonify({"error": f"Reference answer error: {str(e)}"}), 500
        return jsonify({"error": f"Grading error: {str(e)}"}), 500

# ✅ Render requires listening on $PORT
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # default to 5000 locally
    app.run(host="0.0.0.0", port=port)
