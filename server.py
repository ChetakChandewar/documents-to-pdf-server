from flask import Flask, request, send_file, jsonify
import subprocess
import os

app = Flask(__name__)

# Define upload and output folders
UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "output"

# Create directories if they don’t exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

@app.route("/", methods=["GET"])
def home():
    return "Server is running!", 200  # Health check endpoint

@app.route("/convert", methods=["POST"])
def convert_doc_to_pdf():
    """Convert a DOCX file to PDF"""
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    input_path = os.path.join(UPLOAD_FOLDER, file.filename)
    output_filename = file.filename.rsplit(".", 1)[0] + ".pdf"
    output_path = os.path.join(OUTPUT_FOLDER, output_filename)

    file.save(input_path)

    try:
        # Convert using LibreOffice
        subprocess.run(["libreoffice", "--headless", "--convert-to", "pdf", "--outdir", OUTPUT_FOLDER, input_path], check=True)
        return send_file(output_path, as_attachment=True)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/files", methods=["GET"])
def list_files():
    """List all converted PDF files"""
    files = os.listdir(OUTPUT_FOLDER)
    return jsonify({"files": files}), 200

@app.route("/download/<filename>", methods=["GET"])
def download_file(filename):
    """Download a specific converted file"""
    file_path = os.path.join(OUTPUT_FOLDER, filename)
    if not os.path.exists(file_path):
        return jsonify({"error": "File not found"}), 404
    return send_file(file_path, as_attachment=True)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
