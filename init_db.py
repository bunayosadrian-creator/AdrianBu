import sqlite3

conn = sqlite3.connect('students.db')
cursor = conn.cursor()

# Create students table
cursor.execute('''
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id TEXT NOT NULL,
    name TEXT NOT NULL,
    program TEXT NOT NULL,
    year INTEGER NOT NULL,
    section TEXT NOT NULL
)
''')

# Clear existing records to prevent duplication on rerun
cursor.execute("DELETE FROM students")

# 5 Realistic Student Records
students = [
    ('24-00246', 'Adrian Bunayos', 'BSIT', 3, 'A'),
    ('24-00101', 'Maria Santos', 'BSIT', 1, 'A'),
    ('24-00102', 'Juan Dela Cruz', 'BSIT', 1, 'B'),
    ('24-00103', 'Jasmine Rose', 'BSIT', 2, 'A'),
    ('24-00104', 'Pedro Reyes', 'BSIT', 3, 'B')
]

cursor.executemany('''
INSERT INTO students (student_id, name, program, year, section)
VALUES (?, ?, ?, ?, ?)
''', students)

conn.commit()
conn.close()

print("Database created successfully.")