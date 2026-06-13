import sqlite3

def save_candidate(
    name,
    email,
    phone,
    linkedin,
    filename,
    skills,
    experience,
    job_title,
    location
):

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
    INSERT INTO candidates (
        name,
        email,
        phone,
        linkedin,
        filename,
        skills,
        experience,
        job_title,
        location
    )
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        name,
        email,
        phone,
        linkedin,
        filename,
        skills,
        experience,
        job_title,
        location
    ))

    conn.commit()
    conn.close()