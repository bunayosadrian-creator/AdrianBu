from flask import Flask, jsonify, request, render_template

app = Flask(__name__)

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

# Custom endpoint for Additional Task
@app.route('/course')
def get_course():
    return jsonify({
        "course_code": "IT301",
        "course_title": "Web Systems and Technologies",
        "units": 3,
        "status": "Enrolled"
    })

if __name__ == '__main__':
    app.run(debug=True)