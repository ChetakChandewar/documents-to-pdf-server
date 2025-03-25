from flask import Flask, request, send_file
import subprocess
import os

app = Flask(__name__)

UPLOAD_FOLDER = "/app/uploads"
OUTPUT_FOLDER = "/app/output"

# Create directories if not exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

@app.route("/convert", methods=["POST"])
def convert_doc_to_pdf():
    if "file" not in request.files:
        return {"error": "No file uploaded"}, 400

    file = request.files["file"]
    file_extension = file.filename.split('.')[-1].lower()

    if file_extension not in ["doc", "docx"]:
        return {"error": "Invalid file type. Only .doc and .docx allowed."}, 400

    input_path = os.path.join(UPLOAD_FOLDER, file.filename)
    output_path = os.path.join(OUTPUT_FOLDER, file.filename.rsplit(".", 1)[0] + ".pdf")

    file.save(input_path)

    try:
        # Convert DOC/DOCX to PDF using LibreOffice in headless mode
        subprocess.run([
            "libreoffice", "--headless", "--convert-to", "pdf", input_path, "--outdir", OUTPUT_FOLDER
        ], check=True)

        return send_file(output_path, as_attachment=True)
    except Exception as e:
        return {"error": str(e)}, 500
    finally:
        os.remove(input_path)
        if os.path.exists(output_path):
            os.remove(output_path)

# Run Flask server on port 8080
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
