import os
import zipfile
import tempfile
import pandas as pd
from sentence_transformers import SentenceTransformer, util
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Set Gemini API key
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise Exception("Gemini API key not set in .env file")
genai.configure(api_key=api_key)

def generate_reference_answer(question_text):
    """Generate reference answer using Google Gemini 1.5 Flash"""
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(
            f"Write a concise, high-quality answer for the question:\n{question_text}"
        )
        return response.text.strip()
    except Exception as e:
        raise Exception(f"Gemini API error generating reference answer: {str(e)}")

def generate_feedback(student_answer, reference_answer):
    """Generate improvement suggestions using Google Gemini 1.5 Flash"""
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        prompt = (
            f"Compare the student answer with the reference answer and suggest improvements.\n\n"
            f"Reference Answer: {reference_answer}\nStudent Answer: {student_answer}"
        )
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"No suggestions available. Error: {str(e)}"

def grade_with_ai(zip_bytes, question_text, max_marks=10.0, uploads_dir=None):
    """Grades student answers in a zip file using AI-generated reference answer"""
    if uploads_dir is None:
        uploads_dir = tempfile.mkdtemp()
    else:
        os.makedirs(uploads_dir, exist_ok=True)

    temp_zip_path = os.path.join(uploads_dir, "uploaded.zip")
    with open(temp_zip_path, "wb") as f:
        f.write(zip_bytes)

    with zipfile.ZipFile(temp_zip_path, "r") as zip_ref:
        zip_ref.extractall(uploads_dir)

    answers_dir = None
    for root, dirs, _ in os.walk(uploads_dir):
        if "answers" in dirs:
            answers_dir = os.path.join(root, "answers")
            break
    if not answers_dir:
        raise FileNotFoundError("'answers' folder not found in uploaded zip")

    reference_text = generate_reference_answer(question_text)

    model = SentenceTransformer("all-MiniLM-L6-v2")
    reference_embedding = model.encode(reference_text, convert_to_tensor=True)

    rows = []
    for file in sorted(os.listdir(answers_dir)):
        file_path = os.path.join(answers_dir, file)
        if not os.path.isfile(file_path):
            continue

        with open(file_path, "r", encoding="utf-8") as f:
            answer_text = f.read().strip()

        try:
            answer_embedding = model.encode(answer_text, convert_to_tensor=True)
            similarity_score = util.pytorch_cos_sim(
                reference_embedding, answer_embedding
            ).item()
            marks = round(similarity_score * max_marks, 2)
        except Exception as e:
            marks = 0.0
            print(f"Error computing similarity for {file}: {str(e)}")

        suggestion = generate_feedback(answer_text, reference_text)

        rows.append({
            "answer_file": file,
            "marks": marks,
            "suggestions": suggestion
        })

    df = pd.DataFrame(rows)
    return df, uploads_dir
