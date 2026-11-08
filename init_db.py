import sqlite3

conn = sqlite3.connect('students.db')
cursor = conn.cursor()

# Drop table to apply the updated schema cleanly
cursor.execute('DROP TABLE IF EXISTS students')

# Create students table with 'source' column
cursor.execute('''
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id TEXT NOT NULL,
    name TEXT NOT NULL,
    program TEXT NOT NULL,
    year INTEGER NOT NULL,
    section TEXT NOT NULL,
    source TEXT DEFAULT 'Local'
)
''')

# Insert sample records (6 values per tuple matching 6 columns)
cursor.executemany('''
INSERT INTO students (student_id, name, program, year, section, source)
VALUES (?, ?, ?, ?, ?, ?)
''', [
    ('2026-0001', 'Juan Dela Cruz', 'BSIT', 3, 'A', 'Local'),
    ('2026-0002', 'Maria Santos', 'BSCS', 2, 'B', 'Local'),
    ('24-00104', 'Pedro Reyes', 'BSIT', 3, 'B', 'Local')
])

conn.commit()
conn.close()
print("Database initialized successfully.")