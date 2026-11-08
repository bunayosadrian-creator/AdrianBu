import sqlite3
import requests
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('students.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    return render_template('index.html')

# --- LOCAL DB API ENDPOINTS ---

@app.route('/api/students', methods=['GET'])
def api_students():
    conn = get_db_connection()
    rows = conn.execute('SELECT * FROM students').fetchall()
    conn.close()
    return jsonify([dict(row) for row in rows])

@app.route('/api/students/<int:id>', methods=['GET'])
def api_get_student(id):
    conn = get_db_connection()
    student = conn.execute('SELECT * FROM students WHERE id = ?', (id,)).fetchone()
    conn.close()
    if student is None:
        return jsonify({"error": "Student not found"}), 404
    return jsonify(dict(student))

# Step 8: Allow partner/external system to POST to your endpoint with source tracking
@app.route('/api/students', methods=['POST'])
def add_student():
    data = request.get_json()
    source = data.get('source', 'External API')
    conn = get_db_connection()
    cursor = conn.execute(
        """INSERT INTO students
        (student_id, name, program, year, section, source)
        VALUES (?, ?, ?, ?, ?, ?)""",
        (data['student_id'], data['name'], data['program'],
         data['year'], data['section'], source)
    )
    conn.commit()
    new_id = cursor.lastrowid
    conn.close()
    return jsonify({"message": "Student added", "id": new_id}), 201

@app.route('/api/students/<int:id>', methods=['PUT'])
def update_student(id):
    data = request.get_json()
    conn = get_db_connection()
    conn.execute(
        """UPDATE students SET student_id=?, name=?, program=?,
        year=?, section=? WHERE id=?""",
        (data['student_id'], data['name'], data['program'],
         data['year'], data['section'], id)
    )
    conn.commit()
    conn.close()
    return jsonify({"message": "Student updated"})

@app.route('/api/students/<int:id>', methods=['DELETE'])
def delete_student(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM students WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return jsonify({"message": "Student deleted"})

# --- LAB 9 SYSTEM-TO-SYSTEM INTEGRATION ENDPOINTS ---

# Step 3: Retrieve partner records through Flask backend
@app.route('/partner-records', methods=['GET'])
def partner_records():
    partner_url = request.args.get('url')
    if not partner_url:
        return jsonify({"error": "Partner API URL parameter is required"}), 400
    try:
        response = requests.get(partner_url, timeout=15)
        response.raise_for_status()
        return jsonify(response.json())
    except requests.RequestException as e:
        return jsonify({"error": f"Unable to retrieve partner data: {str(e)}"}), 502

# Step 5: Import selected partner record into local DB
@app.route('/import-student', methods=['POST'])
def import_student():
    data = request.get_json()
    conn = get_db_connection()
    conn.execute(
        """INSERT INTO students
        (student_id, name, program, year, section, source)
        VALUES (?, ?, ?, ?, ?, ?)""",
        (data['student_id'], data['name'], data['program'],
         data['year'], data['section'], 'Classmate API')
    )
    conn.commit()
    conn.close()
    return jsonify({"message": "Remote record saved"}), 201

# Step 9: Endpoint to send a practice record to partner API
@app.route('/send-to-partner', methods=['POST'])
def send_to_partner():
    payload = request.get_json()
    partner_url = payload.get('partner_url')
    record = payload.get('record', {
        "student_id": "EXT-001",
        "name": "Sample Exchange Record",
        "program": "BSIT",
        "year": 1,
        "section": "A",
        "source": "Partner API"
    })
    
    if not partner_url:
        return jsonify({"error": "Partner API URL required"}), 400
        
    try:
        response = requests.post(partner_url, json=record, timeout=15)
        return jsonify({
            "status_code": response.status_code,
            "response": response.text
        }), response.status_code
    except requests.RequestException as e:
        return jsonify({"error": f"Failed to send record to partner: {str(e)}"}), 502

if __name__ == '__main__':
    app.run(debug=True)