from flask import Flask, render_template, request
import sqlite3
import os
import re
from pypdf import PdfReader
from docx import Document
import google.generativeai as genai
from database import save_candidate

app = Flask(__name__)

genai.configure(api_key="YOUR_GEMINI_API_KEY")

UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


@app.route("/")
def home():

    conn = sqlite3.connect("candidates.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS candidates (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        email TEXT,
        phone TEXT,
        linkedin TEXT,
        filename TEXT,
        skills TEXT,
        experience TEXT,
        job_title TEXT,
        location TEXT
    )
    """)

    cursor.execute("""
    SELECT *
    FROM candidates
    ORDER BY id DESC
    """)

    candidates = cursor.fetchall()

    conn.commit()
    conn.close()

    return render_template(
        "index.html",
        candidates=candidates
    )


@app.route("/upload", methods=["POST"])
def upload():

    files = request.files.getlist("resumes")

    if not files or files[0].filename == "":
        return "No file selected!"

    for file in files:
        print("Processing File:", file.filename)

        file_path = os.path.join(
            app.config["UPLOAD_FOLDER"],
            file.filename
        )

        file.save(file_path)

        text = ""

        if file.filename.endswith(".pdf"):

            reader = PdfReader(file_path)

            for page in reader.pages:
                text += page.extract_text() or ""

        elif file.filename.endswith(".docx"):

            print("DOCX DETECTED")

            doc = Document(file_path)

            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"

        else:
            continue


        lines = text.split("\n")

        name = ""

        for line in lines:

            if line.strip():

                name = line.strip()

                break

        print("Name:", name)

        emails = re.findall(
            r'[\w\.-]+@[\w\.-]+\.\w+',
            text
        )

        phones = re.findall(
            r'(?:\+91[\s-]?)?[6-9]\d{4}[\s-]?\d{5}',
            text
        )

        linkedin_matches = re.findall(
            r'https?://(?:www\.)?linkedin\.com/[^\s]+',
            text,
            re.IGNORECASE
        )

        linkedin = ""

        if linkedin_matches:
            linkedin = linkedin_matches[0]

        print("\nCONTACT DETAILS FOUND")
        print("Emails:", emails)
        print("Phones:", phones)
        email = emails[0] if emails else ""
        phone = phones[0] if phones else ""

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
            "LinkedIn",
            "[LINKEDIN]"
        )
        scrubbed_text = scrubbed_text.replace(
            "GitHub",
            "[GITHUB]"
        )

        print("\nSCRUBBED TEXT")
        print(scrubbed_text[:500])

        model = genai.GenerativeModel("gemini-2.5-flash")

        prompt = f"""
Analyze this resume.

Return ONLY in this exact format:

SKILLS:<comma separated skills>
EXPERIENCE:<years>
JOB_TITLE:<most recent job title>
LOCATION:<location>

Resume:

{scrubbed_text}
"""

    try:
        response = model.generate_content(prompt)

    except Exception as e:
        print("GEMINI ERROR:", e)
        return f"Gemini Error: {e}"

    print("\nAI ANALYSIS")
    print(response.text)

    skills = ""
    experience = ""
    job_title = ""
    location = ""

    for line in response.text.split("\n"):

        if line.startswith("SKILLS:"):
            skills = line.replace(
                "SKILLS:",
                ""
            ).strip()

        elif line.startswith("EXPERIENCE:"):
            experience = line.replace(
                "EXPERIENCE:",
                ""
            ).strip()

        elif line.startswith("JOB_TITLE:"):
            job_title = line.replace(
                "JOB_TITLE:",
                ""
            ).strip()

        elif line.startswith("LOCATION:"):
            location = line.replace(
                "LOCATION:",
                ""
            ).strip()

    save_candidate(
        name,
        email,
        phone,
        linkedin,
        file.filename,
        skills,
        experience,
        job_title,
        location
    )

    print("Saved structured data to database!")

        

    print("\n" + "=" * 50)
    print(f"FILE: {file.filename}")
    print("=" * 50)
    print(text[:1000])
    print("=" * 50)

    return f"{len(files)} file(s) uploaded, saved, and processed successfully!"


@app.route("/search")
def search():

    skill = request.args.get("skill", "")
    location = request.args.get("location", "")
    min_experience = request.args.get("experience", "0")
    print("MIN EXPERIENCE =",min_experience)

    conn = sqlite3.connect("candidates.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM candidates
        WHERE skills LIKE ?
        AND location LIKE ?
    """, (
        f"%{skill}%",
        f"%{location}%"
    ))

    results = cursor.fetchall()

    filtered_results = []

    for row in results:
        try:
            candidate_experience = float(row[7])

            if candidate_experience >= float(min_experience):
                filtered_results.append(row)

        except:
            pass

    conn.close()

    output = """
    <html>
    <body style="font-family: Arial; margin: 40px;">
    <h1>Search Results</h1>
    """

    for row in filtered_results:

        output += f"""
        <div style="
            border:1px solid #ddd;
            padding:20px;
            margin-bottom:20px;
            border-radius:10px;
        ">

        <h2>{row[1]}</h2>

        <p><b>File:</b> {row[5]}</p>

        <p><b>Skills:</b><br>{row[6]}</p>

        <p><b>Experience:</b> {row[7]} years</p>

        <p><b>Location:</b> {row[9]}</p>

        </div>
        """

    if len(filtered_results) == 0:
        output += """
        <h2>No candidates found</h2>
        """

    output += """
    </body>
    </html>
    """

    return output

@app.route("/profile/<int:id>")
def profile(id):

    conn = sqlite3.connect("candidates.db")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM candidates WHERE id = ?",
        (id,)
    )

    candidate = cursor.fetchone()

    conn.close()

    if not candidate:
        return "Candidate not found"

    return f"""
    <html>
    <body style="font-family: Arial; margin:40px;">

    <h1>{candidate[1]}</h1>

    <p><b>Email:</b> {candidate[2]}</p>

    <p><b>Phone:</b> {candidate[3]}</p>

    <p><b>LinkedIn:</b> {candidate[4]}</p>

    <p><b>File:</b> {candidate[5]}</p>

    <p><b>Skills:</b> {candidate[6]}</p>

    <p><b>Experience:</b> {candidate[7]}</p>

    <p><b>Job Title:</b> {candidate[8]}</p>

    <p><b>Location:</b> {candidate[9]}</p>

    <br>

    <a href="/">Back</a>

    </body>
    </html>
    """
if __name__ == "__main__":
    app.run(debug=True)