from flask import Flask, render_template, request
import os
import re
from pypdf import PdfReader
import google.generativeai as genai
from database import save_candidate

app = Flask(__name__)
genai.configure(api_key="YOUR_GEMINI_API_KEY")

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
                scrubbed_text = scrubbed_text.replace(
                    "LinkedIn"
                    "[LINKEDIN]"
                )
                scrubbed_text = scrubbed_text.replace(
                    "GitHub"
                    "[GITHUB]"
                )

            print("\nSCRUBBED TEXT")
            print(scrubbed_text[:500])
            
            model = genai.GenerativeModel("gemini-2.5-flash")
            prompt = f"""
            Analyze this resume 
            Return ONLY in this exact format:

            SKILLS:<comma separated skills>
            EXPERIENCE:<years>
            JOB_TITLE:<most recent job title>
            LOCATION:<location>

            Resume:

            {scrubbed_text}
            """
            response = model.generate_content(prompt)

            print("\nAI ANALYSIS")
            print(response.text)

            skills = ""
            experience = ""
            job_title = ""
            location = ""

            for line in response.text.split("\n"):
                if line.startswith("SKILLS:"):
                    skills = line.replace("SKILls:", "").strip()
                elif line.startswith("EXPERIENCE:"):
                    experience = line.replace("EXPERIENCE:", "").strip()
                elif line.startswith("JOB_TITLE:"):
                    job_title = line.replace("JOB_TITLE:", "").strip()
                elif line.startswith("LOCATION:"):
                    location = line.replace("LOCATION:", "").strip()

            save_candidate(
                file.filename,
                skills,
                experience,
                job_title,
                location
            )

            print("Saved structured data to database")


            print("\n" + "=" * 50)
            print(f"FILE: {file.filename}")
            print("=" * 50)
            print(text[:1000])
            print("=" * 50)

    return f"{len(files)} file(s) uploaded, saved, and processed successfully!"


if __name__ == "__main__":
    app.run(debug=True)