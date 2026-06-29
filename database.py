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
    CREATE TABLE IF NOT EXISTS retry_jobs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        filename TEXT,
        status TEXT,
        retry_count INTEGER DEFAULT 0
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

def save_retry_job(filename):

    conn = sqlite3.connect("candidates.db")

    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS retry_jobs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        filename TEXT,
        status TEXT,
        retry_count INTEGER DEFAULT 0
    )
    """)

    cursor.execute("""
    INSERT INTO retry_jobs (
        filename,
        status,
        retry_count
    )
    VALUES (?, ?, ?)
    """, (
        filename,
        "Pending",
        0
    ))

    conn.commit()
    conn.close()


def get_pending_retry_jobs():

    conn = sqlite3.connect("candidates.db")

    cursor = conn.cursor()

    cursor.execute("""
    SELECT *
    FROM retry_jobs
    WHERE status = 'Pending'
    """)

    jobs = cursor.fetchall()

    conn.close()

    return jobs


def mark_retry_job_completed(job_id):

    conn = sqlite3.connect("candidates.db")

    cursor = conn.cursor()

    cursor.execute("""
    UPDATE retry_jobs
    SET status = 'Completed'
    WHERE id = ?
    """, (job_id,))

    conn.commit()
    conn.close()

def candidate_exists(filename):

    conn = sqlite3.connect("candidates.db")

    cursor = conn.cursor()

    cursor.execute("""
    SELECT COUNT(*)
    FROM candidates
    WHERE filename = ?
    """, (filename,))

    exists = cursor.fetchone()[0] > 0

    conn.close()

    return exists
