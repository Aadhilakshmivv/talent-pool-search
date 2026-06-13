import google.generativeai as genai

genai.configure(api_key="YOUR_GEMINI_API_KEY")

model = genai.GenerativeModel("gemini-2.5-flash")

resume_text = """
Fathima Nasrin

Email: [EMAIL]
Phone: [PHONE]

Skills:
Python, Flask, SQL, React

Worked as Software Developer at ABC Technologies
from 2022 to 2025.

Location: Thrissur, Kerala
"""

prompt = f"""
Analyze this resume and return:

1. Skills
2. Total years of experience
3. Most recent job title
4. Location

Resume:

{resume_text}
"""

response = model.generate_content(prompt)

print(response.text)