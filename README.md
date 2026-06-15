# Talent Pool Search

## Overview

Talent Pool Search is an AI-powered resume screening and candidate search application built using Flask and SQLite.

The application allows recruiters to upload multiple resumes, extract candidate information, remove personal information before AI analysis, and search candidates based on skills, experience, and location.

## Features

### Resume Upload
- Upload multiple PDF and DOCX resumes
- Store uploaded resumes locally

### Resume Parsing
- Extract text from PDF resumes
- Extract text from DOCX resumes

### Contact Information Extraction
- Extract candidate name
- Extract email address using regular expressions
- Extract phone number using regular expressions
- Extract LinkedIn information using regular expressions

### PII Scrubbing
Before sending resume content to the AI model:
- Email addresses are replaced with [EMAIL]
- Phone numbers are replaced with [PHONE]
- LinkedIn URLs are replaced with [LINKEDIN]
- GitHub URLs are replaced with [GITHUB]

### AI-Powered Analysis
The application extracts:
- Skills
- Total Years of Experience
- Most Recent Job Title
- Location

### Candidate Database
All extracted information is stored in a SQLite database.

### Candidate Search
Recruiters can search candidates using:
- Skills
- Location
- Minimum Experience

### Candidate Profile
View:
- Candidate Name
- Email
- Phone Number
- LinkedIn Information
- Skills
- Experience
- Job Title
- Location
- Original Resume

## Technology Stack

### Frontend
- HTML
- CSS

### Backend
- Python
- Flask

### Database
- SQLite

### AI Model
- Groq API
- Llama 3.3 70B Versatile

### Libraries Used
- pypdf
- python-docx
- sqlite3
- Flask
- Groq

## Project Workflow

1. Recruiter uploads one or more resumes.
2. Resume text is extracted locally.
3. Contact details are extracted using regex.
4. Personal information is scrubbed.
5. Scrubbed resume text is sent to the AI model.
6. AI extracts skills, experience, job title, and location.
7. Candidate data is stored in SQLite.
8. Recruiters search and view candidate profiles.

## Installation

### Clone Repository

git clone <repository-url>

### Create Virtual Environment

python -m venv venv

### Activate Virtual Environment

Windows:

venv\Scripts\activate

### Install Dependencies

pip install -r requirements.txt

### Configure API Key

Create a .env file and add:

GROQ_API_KEY=your_api_key_here

### Run Application

python app.py

### Open Browser

http://127.0.0.1:5000