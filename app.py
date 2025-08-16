from flask import Flask, request, redirect, url_for
import os
import zipfile

app = Flask(__name__)

# Temporary upload folder (Render allows writing to /tmp)
UPLOAD_FOLDER = "/tmp/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/", methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        if "file" not in request.files:
            return "No file part in request", 400

        file = request.files["file"]
        if file.filename == "":
            return "No file selected", 400

        # Save uploaded file directly to disk
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(file_path)

        # Extract ZIP one file at a time (memory-efficient)
        extract_folder = os.path.join(UPLOAD_FOLDER, file.filename + "_extracted")
        os.makedirs(extract_folder, exist_ok=True)

        try:
            with zipfile.ZipFile(file_path, "r") as zip_ref:
                for member in zip_ref.infolist():
                    zip_ref.extract(member, extract_folder)
        except zipfile.BadZipFile:
            return "Uploaded file is not a valid ZIP", 400

        return f"Uploaded and extracted to {extract_folder}"

    # Simple upload form
    return '''
    <!doctype html>
    <title>Upload ZIP</title>
    <h1>Upload a ZIP file</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Render sets $PORT
    app.run(host="0.0.0.0", port=port)
