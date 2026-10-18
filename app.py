import sqlite3
from flask import Flask, jsonify, request, render_template

app = Flask(__name__)

# Database connection helper function
def get_db_connection():
    conn = sqlite3.connect('students.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/student')
def get_student():
    return jsonify({
        "student_id": "24-00246",
        "name": "Adrian Bunayos",
        "program": "BSIT",
        "year": 3,
        "section": "A"
    })

@app.route('/hello')
def say_hello():
    name = request.args.get('name', 'Student')
    return jsonify({
        "message": f"Hello, {name}!"
    })

# Step 5: Endpoint to retrieve ALL students from SQLite database
@app.route('/students')
def get_students():
    conn = get_db_connection()
    students = conn.execute('SELECT * FROM students').fetchall()
    conn.close()
    return jsonify([dict(student) for student in students])

# Step 7: Endpoint to retrieve ONE student by Database ID
@app.route('/students/<int:id>')
def get_student_by_id(id):
    conn = get_db_connection()
    student = conn.execute(
        'SELECT * FROM students WHERE id = ?', (id,)
    ).fetchone()
    conn.close()
    if student is None:
        return jsonify({"error": "Student not found"}), 404
    return jsonify(dict(student))

# Additional Task: Database API Endpoint to filter students by Year Level
@app.route('/students/year/<int:year>')
def get_students_by_year(year):
    conn = get_db_connection()
    students = conn.execute(
        'SELECT * FROM students WHERE year = ?', (year,)
    ).fetchall()
    conn.close()
    return jsonify([dict(student) for student in students])

if __name__ == '__main__':
    app.run(debug=True)