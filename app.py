from flask import Flask, jsonify, request

app = Flask(__name__)

# Base Routes
@app.route('/')
def home():
    return "Welcome to my updated API portfolio!"

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

# --- STEP 8: NEW ENDPOINT 1 (Custom Information) ---
@app.route('/hobbies')
def get_hobbies():
    return jsonify({
        "favorite_hobbies": ["Gaming", "Coding", "Basketball"],
        "tech_stack": ["Python", "Flask", "Git"],
        "status": "Currently learning web service deployment!"
    })

# --- STEP 8: NEW ENDPOINT 2 (Accepts input from URL like ?mood=motivated) ---
@app.route('/quote')
def get_quote():
    mood = request.args.get('mood', 'happy').lower()
    quotes = {
        "happy": "Keep smiling, coding is fun!",
        "motivated": "Code is like humor. When you have to explain it, it’s bad.",
        "tired": "Take a rest! Even servers need rebooting sometimes."
    }
    quote_text = quotes.get(mood, "Stay positive and keep learning!")
    return jsonify({
        "requested_mood": mood,
        "quote": quote_text
    })

if __name__ == '__main__':
    app.run(debug=True)
