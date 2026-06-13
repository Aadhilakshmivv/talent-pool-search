from flask import Flask, render_template, request
import os
import re
from pypdf import PdfReader

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload():
    files = request.files.getlist("resumes")

    if not files or files[0].filename == "":
        return "No file selected!"

    for file in files:
        file_path = os.path.join(
            app.config["UPLOAD_FOLDER"],
            file.filename
        )

        file.save(file_path)

        if file.filename.endswith(".pdf"):
            reader = PdfReader(file_path)

            text = ""

            for page in reader.pages:
                text += page.extract_text() or ""

            # Extract email
            emails = re.findall(
                r'[\w\.-]+@[\w\.-]+\.\w+',
                text
            )

            # Extract phone
            phones = re.findall(
                r'(?:\+91[\s-]?)?[6-9]\d{4}[\s-]?\d{5}',
                text
            )

            print("\nCONTACT DETAILS FOUND")
            print("Emails:", emails)
            print("Phones:", phones)

            # Create scrubbed copy
            scrubbed_text = text

            for email in emails:
                scrubbed_text = scrubbed_text.replace(
                    email,
                    "[EMAIL]"
                )

            for phone in phones:
                scrubbed_text = scrubbed_text.replace(
                    phone,
                    "[PHONE]"
                )

            print("\nSCRUBBED TEXT")
            print(scrubbed_text[:500])

            print("\n" + "=" * 50)
            print(f"FILE: {file.filename}")
            print("=" * 50)
            print(text[:1000])
            print("=" * 50)

    return f"{len(files)} file(s) uploaded, saved, and processed successfully!"


if __name__ == "__main__":
    app.run(debug=True)