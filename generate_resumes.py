from docx import Document
from reportlab.pdfgen import canvas
import os

OUTPUT_FOLDER = "generated_resumes"

os.makedirs(OUTPUT_FOLDER, exist_ok=True)

candidates = [
    {
        "name": "Arjun Menon",
        "email": "arjun.menon@gmail.com",
        "phone": "+91 9876543211",
        "linkedin": "https://linkedin.com/in/arjunmenon",
        "role": "Junior Software Engineer",
        "location": "Kochi",
        "experience": "1 Year",
        "skills": "Python, SQL, Flask, Git",
        "education": "B.Tech Computer Science",
        "type": "docx"
    },
    {
        "name": "Priya Nair",
        "email": "priya.nair@gmail.com",
        "phone": "+91 9876543212",
        "linkedin": "https://linkedin.com/in/priyanair",
        "role": "UI/UX Designer",
        "location": "Bangalore",
        "experience": "3 Years",
        "skills": "Figma, Adobe XD, User Research, Wireframing",
        "education": "B.Des Design",
        "type": "pdf"
    },
    {
        "name": "Rahul Sharma",
        "email": "rahul.sharma@gmail.com",
        "phone": "+91 9876543213",
        "linkedin": "https://linkedin.com/in/rahulsharma",
        "role": "Project Manager",
        "location": "Pune",
        "experience": "8 Years",
        "skills": "Agile, Scrum, Jira, Risk Management",
        "education": "MBA Project Management",
        "type": "pdf"
    },
    {
        "name": "Sneha Reddy",
        "email": "sneha.reddy@gmail.com",
        "phone": "+91 9876543214",
        "linkedin": "https://linkedin.com/in/snehareddy",
        "role": "Product Manager",
        "location": "Hyderabad",
        "experience": "6 Years",
        "skills": "Product Strategy, Analytics, Roadmaps, SQL",
        "education": "MBA",
        "type": "docx"
    },
    {
        "name": "Vikram Patel",
        "email": "vikram.patel@gmail.com",
        "phone": "+91 9876543215",
        "linkedin": "https://linkedin.com/in/vikrampatel",
        "role": "Backend Developer",
        "location": "Mumbai",
        "experience": "5 Years",
        "skills": "Java, Spring Boot, PostgreSQL, Docker",
        "education": "B.Tech IT",
        "type": "docx"
    },
    {
        "name": "Meera Krishnan",
        "email": "meera.krishnan@gmail.com",
        "phone": "+91 9876543216",
        "linkedin": "https://linkedin.com/in/meerakrishnan",
        "role": "Graphic Designer",
        "location": "Trivandrum",
        "experience": "4 Years",
        "skills": "Photoshop, Illustrator, Branding, Canva",
        "education": "B.Des",
        "type": "pdf"
    },
    {
        "name": "Ankit Verma",
        "email": "ankit.verma@gmail.com",
        "phone": "+91 9876543217",
        "linkedin": "https://linkedin.com/in/ankitverma",
        "role": "Sales Executive",
        "location": "Delhi",
        "experience": "2 Years",
        "skills": "CRM, Lead Generation, Negotiation",
        "education": "BBA",
        "type": "docx"
    },
    {
        "name": "Neha Joseph",
        "email": "neha.joseph@gmail.com",
        "phone": "+91 9876543218",
        "linkedin": "https://linkedin.com/in/nehajoseph",
        "role": "Operations Manager",
        "location": "Chennai",
        "experience": "7 Years",
        "skills": "Supply Chain, Process Optimization, ERP",
        "education": "MBA Operations",
        "type": "docx"
    },
    {
        "name": "Aditya Rao",
        "email": "aditya.rao@gmail.com",
        "phone": "+91 9876543219",
        "linkedin": "https://linkedin.com/in/adityarao",
        "role": "Full Stack Developer",
        "location": "Bangalore",
        "experience": "4 Years",
        "skills": "React, Node.js, MongoDB, AWS",
        "education": "B.Tech CSE",
        "type": "docx"
    },
    {
        "name": "Kavya Das",
        "email": "kavya.das@gmail.com",
        "phone": "+91 9876543220",
        "linkedin": "https://linkedin.com/in/kavyadas",
        "role": "QA Automation Engineer",
        "location": "Hyderabad",
        "experience": "3 Years",
        "skills": "Selenium, Python, Test Automation",
        "education": "B.Tech",
        "type": "pdf"
    },
    {
        "name": "Rohan Iyer",
        "email": "rohan.iyer@gmail.com",
        "phone": "+91 9876543221",
        "linkedin": "https://linkedin.com/in/rohaniyer",
        "role": "DevOps Engineer",
        "location": "Bangalore",
        "experience": "6 Years",
        "skills": "AWS, Docker, Kubernetes, Linux",
        "education": "B.Tech",
        "type": "docx"
    },
    {
        "name": "Aisha Khan",
        "email": "aisha.khan@gmail.com",
        "phone": "+91 9876543222",
        "linkedin": "https://linkedin.com/in/aishakhan",
        "role": "UI Designer",
        "location": "Kochi",
        "experience": "1 Year",
        "skills": "Figma, Wireframing, Prototyping",
        "education": "B.Des",
        "type": "docx"
    },
    {
        "name": "Sanjay Nair",
        "email": "sanjay.nair@gmail.com",
        "phone": "+91 9876543223",
        "linkedin": "https://linkedin.com/in/sanjaynair",
        "role": "Data Engineer",
        "location": "Pune",
        "experience": "5 Years",
        "skills": "Python, SQL, Spark, AWS",
        "education": "B.Tech",
        "type": "pdf"
    },
    {
        "name": "Divya Menon",
        "email": "divya.menon@gmail.com",
        "phone": "+91 9876543224",
        "linkedin": "https://linkedin.com/in/divyamenon",
        "role": "Business Analyst",
        "location": "Chennai",
        "experience": "4 Years",
        "skills": "SQL, Power BI, Excel, Requirements Gathering",
        "education": "MBA",
        "type": "docx"
    },
    {
        "name": "Harish Kumar",
        "email": "harish.kumar@gmail.com",
        "phone": "+91 9876543225",
        "linkedin": "https://linkedin.com/in/harishkumar",
        "role": "Senior Software Engineer",
        "location": "Mumbai",
        "experience": "10 Years",
        "skills": "Python, Django, PostgreSQL, AWS",
        "education": "B.Tech",
        "type": "pdf"
    }
]

def create_docx(candidate):
    doc = Document()

    doc.add_heading(candidate["name"], level=1)
    doc.add_paragraph(f"Email: {candidate['email']}")
    doc.add_paragraph(f"Phone: {candidate['phone']}")
    doc.add_paragraph(f"LinkedIn: {candidate['linkedin']}")
    doc.add_paragraph(f"Role: {candidate['role']}")
    doc.add_paragraph(f"Location: {candidate['location']}")
    doc.add_paragraph(f"Experience: {candidate['experience']}")
    doc.add_paragraph(f"Skills: {candidate['skills']}")
    doc.add_paragraph(f"Education: {candidate['education']}")

    filename = os.path.join(
        OUTPUT_FOLDER,
        candidate["name"].replace(" ", "_") + ".docx"
    )

    doc.save(filename)

def create_pdf(candidate):
    filename = os.path.join(
        OUTPUT_FOLDER,
        candidate["name"].replace(" ", "_") + ".pdf"
    )

    c = canvas.Canvas(filename)

    y = 800

    lines = [
        candidate["name"],
        f"Email: {candidate['email']}",
        f"Phone: {candidate['phone']}",
        f"LinkedIn: {candidate['linkedin']}",
        f"Role: {candidate['role']}",
        f"Location: {candidate['location']}",
        f"Experience: {candidate['experience']}",
        f"Skills: {candidate['skills']}",
        f"Education: {candidate['education']}"
    ]

    for line in lines:
        c.drawString(50, y, line)
        y -= 20

    c.save()

for candidate in candidates:
    if candidate["type"] == "docx":
        create_docx(candidate)
    else:
        create_pdf(candidate)

print("Resumes generated successfully!")