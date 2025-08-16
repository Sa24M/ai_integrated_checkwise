# CheckWise AI Grading System

[![Python](https://img.shields.io/badge/python-3.11+-blue)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/flask-2.3-green)](https://flask.palletsprojects.com/)
[![License](https://img.shields.io/badge/license-MIT-orange)](LICENSE)

CheckWise is an AI-powered grading system that automatically evaluates student answers using advanced language models and semantic similarity. It generates reference answers, grades student submissions, and provides improvement suggestions.

---

## 🚀 Features

* Upload a ZIP file of student answers (as text files)
* Enter the question to be graded
* AI generates a reference answer using **Google Gemini**
* Each student answer is graded using **semantic similarity** (Sentence Transformers)
* AI provides personalized suggestions for improvement
* Download grading results as a **CSV report**
* Modern, **responsive web UI**

---

## 📂 Project Structure

```
.
├── app.py                  # Flask web server
├── grader_ai.py            # AI grading logic (Gemini, embeddings, feedback)
├── requirements.txt        # Python dependencies
├── Procfile                # For deployment (Render, Heroku)
├── start.sh                # Startup script for deployment
├── static/
│   ├── script.js           # Frontend logic (AJAX, CSV download)
│   └── style.css           # Custom styles
├── templates/
│   └── index.html          # Main web page (form & results)
└── uploads/                # Temporary folder for uploaded files (created at runtime)
```

---

## ⚡ Quick Start

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/checkwise-ai.git
cd checkwise-ai
```

### 2. Install dependencies

Use a virtual environment (recommended):

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Set up environment variables

Create a `.env` file in the project root:

```env
GEMINI_API_KEY=your-gemini-api-key-here
```

### 4. Run the app locally

```bash
python app.py
```

Open in your browser: [http://127.0.0.1:5000](http://127.0.0.1:5000)

---

## 🛠 Usage

1. Open the web app in your browser
2. Enter the question to be graded
3. Upload a ZIP file containing an `answers/` folder with student answer `.txt` files
4. Click **Grade Answers**
5. View marks and suggestions in the results table
6. Download the CSV report if needed

---

## ☁️ Deployment

* Ready for deployment on **Render**, **Heroku**, or similar platforms
* Uses `Procfile` and `start.sh` for production WSGI serving with **Gunicorn**

---

## 🧰 Technologies Used

* [Flask](https://flask.palletsprojects.com/) – backend
* [Sentence Transformers](https://www.sbert.net/) – semantic similarity
* [Google Gemini](https://ai.google.dev/) – reference answer & feedback
* [Bootstrap 5](https://getbootstrap.com/) – frontend
* [Pandas](https://pandas.pydata.org/) – data handling



**Note:** This project requires access to the Google Gemini API and may incur costs depending on usage.
