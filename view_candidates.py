import sqlite3

conn = sqlite3.connect("candidates.db")

cursor = conn.cursor()

cursor.execute("SELECT * FROM candidates")

rows = cursor.fetchall()

print("\nCANDIDATES IN DATABASE\n")

for row in rows:
    print("=" * 50)
    print("ID:", row[0])
    print("Name:", row[1])
    print("Email:", row[2])
    print("Phone:", row[3])
    print("LinkedIn:", row[4])
    print("Filename:", row[5])
    print("Skills:", row[6])
    print("Experience:", row[7])
    print("Job Title:", row[8])
    print("Location:", row[9])

conn.close()