from flask import Flask, render_template, request ,send_from_directory
import sqlite3
import os
import re
from pypdf import PdfReader
from docx import Document
from dotenv import load_dotenv
from groq import Groq
from database import save_candidate
from flask import redirect


app = Flask(__name__)

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

UPLOAD_FOLDER = "uploads"
import os
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


@app.route("/")
def home():

    message = request.args.get("message", "")

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
        candidates=candidates,
        message=message
    )


@app.route("/upload", methods=["POST"])
def upload():

    files = request.files.getlist("resumes")
    success_count = 0

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

                page_text = page.extract_text()

                print("PAGE TEXT =", page_text)

                text += page_text or ""

            print("PDF TEXT LENGTH =", len(text))

        elif file.filename.endswith(".docx"):

            print("DOCX DETECTED")

            doc = Document(file_path)

            # Normal paragraphs
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"

            # Tables
            for table in doc.tables:
                for row in table.rows:
                    for cell in row.cells:
                        text += cell.text + "\n"

            print("========== EXTRACTED TEXT ==========")
            print(text)
            print("===================================")

            print("TEXT LENGTH =", len(text))

        else:
            continue


        lines = text.split("\n")

        name = ""

        for line in lines:

            line = line.strip()

            if not line:
                continue

            if "@" in line:
                continue

            if "linkedin" in line.lower():
                continue

            if "github" in line.lower():
                continue

            if len(line) > 40:
                continue

            name = line
            break

        print("Name:", name)

        emails = re.findall(
            r'[\w\.-]+@[\w\.-]+\.\w+',
            text
        )

        phones = re.findall(
        r'(\+?\d[\d\s\-]{8,15}\d)',
        text
        )

        linkedin_matches = re.findall(
        r'(?:https?://)?(?:www\.)?linkedin\.com/[^\s]+',
        text,
        re.IGNORECASE
        )

        linkedin = ""

        if linkedin_matches:
            linkedin = linkedin_matches[0]

        else:
            linkedin_short = re.findall(
                r'linkedin/[A-Za-z0-9_-]+',
                text,
                re.IGNORECASE
            )

            if linkedin_short:
                linkedin = linkedin_short[0]


        github = ""

        github_matches = re.findall(
            r'github/[A-Za-z0-9_-]+',
            text,
            re.IGNORECASE
        )

        if github_matches:
            github = github_matches[0]

        print("\nCONTACT DETAILS FOUND")
        print("Emails:", emails)
        print("Phones:", phones)
        email = emails[0] if emails else ""
        phone = phones[0] if phones else ""

        scrubbed_text = text

        if linkedin:
            scrubbed_text = scrubbed_text.replace(
                linkedin,
                "[LINKEDIN]"
            )
        
        if github:
            scrubbed_text = scrubbed_text.replace(
                github,
                "[GITHUB]"
            )
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
        response = None

        skills = "Not Available"
        experience = "0"
        job_title = "Not Available"
        location = "Not Available"

        for attempt in range(3):

            try:

                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ]
                )

                break

            except Exception as e:

                print("GROQ ERROR:", e)

                break

    

        if response:
            print("\nAI ANALYSIS")
            ai_output = response.choices[0].message.content

            print(ai_output)

            skills = ""
            experience = ""
            job_title = ""
            location = ""

            for line in ai_output.split("\n"):

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
        print("JOB =", job_title)
        print("LOC =", location)
        print("EXP =", experience)
        print("SKILLS =", skills)

        print("RESPONSE IS NONE =", response is None)

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

        success_count += 1
    print("SUCCESS COUNT =", success_count)

    print("Saved structured data to database!")    

            

    print("\n" + "=" * 50)
    print(f"FILE: {file.filename}")
    print("=" * 50)
    print(text[:1000])
    print("=" * 50)

    if success_count == 1:
        return redirect("/?message=1 resume processed successfully")

    return redirect(f"/?message={success_count} resumes processed successfully")

@app.route("/search")
def search():

    skill = request.args.get("skill", "")
    location = request.args.get("location", "")

    min_experience = request.args.get("experience", "")

    if (
        skill.strip() == "" and
        location.strip() == "" and
        min_experience.strip() == ""
    ):
        return """
        <html>
        <body style="font-family: Arial; margin:40px;">
            <h2>Please enter at least one search criteria.</h2>

            <br>

            <a href="/">Back</a>

        </body>
        </html>
        """

    if min_experience == "":
        min_experience = "0"

    print("MIN EXPERIENCE =", min_experience)

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
    print("SEARCH SKILL =", skill)
    print("SEARCH LOCATION =", location)
    print("RESULTS =", results)
    filtered_results = []

    for row in results:
        try:
            candidate_experience = float(row[7])

            if candidate_experience >= float(min_experience):
                filtered_results.append(row)

        except Exception as e:
            print("ERROR =", e)

    conn.close()

    output = """
    <html>
    <head>
    <style>

    .profile-btn {
        display: inline-block;
        margin-top: 10px;
        padding: 8px 15px;
        background: #007bff;
        color: white;
        text-decoration: none;
        border-radius: 5px;
    }

    .profile-btn:hover {
        background: #0056b3;
    }

    </style>
    </head>

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

        <p><b>Skills:</b><br>{row[6]}</p>

        <p><b>Experience:</b> {row[7]} years</p>

        <p><b>Location:</b> {row[9]}</p>

        <a
            class="profile-btn"
            href="/profile/{row[0]}">
            View Profile
        </a>

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

    <p>
    <b>Email:</b>
    <a href="mailto:{candidate[2]}">
        {candidate[2]}
    </a>
    </p>

    <p>
    <b>Phone:</b>
    <a href="tel:{candidate[3]}">
        {candidate[3]}
    </a>
    </p>

    <p>
    <b>LinkedIn:</b>
    <a href="https://{candidate[4]}" target="_blank">
        {candidate[4]}
    </a>
    </p>

    <p><b>File:</b> {candidate[5]}</p>

    <p><b>Skills:</b> {candidate[6]}</p>

    <p><b>Experience:</b> {candidate[7]}</p>

    <p><b>Job Title:</b> {candidate[8]}</p>

    <p><b>Location:</b> {candidate[9]}</p>

    <br>

    <a
        href="/resume/{candidate[5]}"
        style="
            display:inline-block;
            padding:8px 15px;
            background:#28a745;
            color:white;
            text-decoration:none;
            border-radius:5px;
        ">
        View Resume
    </a>

<br><br>

    <a href="/">Back</a>

    </body>
    </html>
    """

@app.route("/resume/<path:filename>")
def view_resume(filename):

    return send_from_directory(
        app.config["UPLOAD_FOLDER"],
        filename,
        as_attachment=False
    )


if __name__ == "__main__":
    app.run(debug=True)