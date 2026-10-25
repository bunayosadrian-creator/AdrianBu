import sqlite3
import json
import urllib.request
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
    return jsonify({"message": f"Hello, {name}!"})

@app.route('/students')
def get_students():
    conn = get_db_connection()
    students = conn.execute('SELECT * FROM students').fetchall()
    conn.close()
    return jsonify([dict(student) for student in students])

@app.route('/students/<int:id>')
def get_student_by_id(id):
    conn = get_db_connection()
    student = conn.execute('SELECT * FROM students WHERE id = ?', (id,)).fetchone()
    conn.close()
    if student is None:
        return jsonify({"error": "Student not found"}), 404
    return jsonify(dict(student))

@app.route('/students/year/<int:year>')
def get_students_by_year(year):
    conn = get_db_connection()
    students = conn.execute('SELECT * FROM students WHERE year = ?', (year,)).fetchall()
    conn.close()
    return jsonify([dict(student) for student in students])

# ==========================================
# REST API Endpoints (/api/students)
# ==========================================

# READ ALL: Endpoint for local app and external clients (GET)
@app.route('/api/students', methods=['GET'])
def api_students():
    conn = get_db_connection()
    rows = conn.execute('SELECT * FROM students').fetchall()
    conn.close()
    return jsonify([dict(row) for row in rows])

# CREATE: Add a new student (POST)
@app.route('/api/students', methods=['POST'])
def add_student():
    data = request.get_json()
    conn = get_db_connection()
    cursor = conn.execute(
        """INSERT INTO students (student_id, name, program, year, section)
        VALUES (?, ?, ?, ?, ?)""",
        (data['student_id'], data['name'], data['program'], data['year'], data['section'])
    )
    conn.commit()
    new_id = cursor.lastrowid
    conn.close()
    return jsonify({"message": "Student added", "id": new_id}), 201

# READ ONE: Retrieve single student by DB ID (GET)
@app.route('/api/students/<int:id>', methods=['GET'])
def api_get_student(id):
    conn = get_db_connection()
    student = conn.execute('SELECT * FROM students WHERE id = ?', (id,)).fetchone()
    conn.close()
    if student is None:
        return jsonify({"error": "Student not found"}), 404
    return jsonify(dict(student))

# UPDATE: Update existing student record (PUT)
@app.route('/api/students/<int:id>', methods=['PUT'])
def update_student(id):
    data = request.get_json()
    conn = get_db_connection()
    conn.execute(
        """UPDATE students SET student_id=?, name=?, program=?, year=?, section=?
        WHERE id=?""",
        (data['student_id'], data['name'], data['program'], data['year'], data['section'], id)
    )
    conn.commit()
    conn.close()
    return jsonify({"message": "Student updated"})

# DELETE: Remove student by DB ID (DELETE)
@app.route('/api/students/<int:id>', methods=['DELETE'])
def delete_student(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM students WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return jsonify({"message": "Student deleted"})

# --- Classmate Proxy Endpoint (Bypasses CORS if browser direct fetch is blocked) ---
@app.route('/api/classmate-proxy')
def classmate_proxy():
    target_url = request.args.get('url')
    if not target_url:
        return jsonify({"error": "URL query parameter is required"}), 400
    try:
        req = urllib.request.Request(target_url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode('utf-8'))
            return jsonify(data)
    except Exception as e:
        return jsonify({"error": f"Failed to fetch classmate data: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True)