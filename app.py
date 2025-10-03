from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
import openai

app = Flask(__name__)
CORS(app)

openai.api_key = "YOUR_OPENAI_API_KEY"
DB_NAME = "mentor_student.db"

# Initialize DB
def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    # Users table
    c.execute("""
        CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT,
            role TEXT
        )
    """)
    # Doubts table
    c.execute("""
        CREATE TABLE IF NOT EXISTS doubts(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_name TEXT,
            doubt TEXT,
            answer TEXT
        )
    """)
    # Insert sample users
    c.execute("INSERT OR IGNORE INTO users(username,password,role) VALUES ('student1','123','1st')")
    c.execute("INSERT OR IGNORE INTO users(username,password,role) VALUES ('mentor1','123','2nd')")
    conn.commit()
    conn.close()

init_db()

# Login Route
@app.route("/login",methods=["POST"])
def login():
    data = request.get_json()
    user = data.get("username")
    password = data.get("password")
    role = data.get("role")
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username=? AND password=? AND role=?",(user,password,role))
    res = c.fetchone()
    conn.close()
    if res:
        return jsonify({"status":"success"})
    return jsonify({"status":"fail","message":"Invalid username/password/role"})

# Submit doubt
@app.route("/submit_doubt", methods=["POST"])
def submit_doubt():
    data = request.get_json()
    student_name = data.get("student_name")
    doubt = data.get("doubt")
    if not student_name or not doubt:
        return jsonify({"status": "error", "message": "Missing fields"})
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("INSERT INTO doubts (student_name,doubt) VALUES (?,?)",(student_name,doubt))
    conn.commit(); conn.close()
    return jsonify({"status":"success"})

# Get doubts
@app.route("/get_doubts", methods=["GET"])
def get_doubts():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT id, student_name, doubt, answer FROM doubts")
    rows = c.fetchall(); conn.close()
    doubts_list = [{"id":r[0],"student_name":r[1],"doubt":r[2],"answer":r[3]} for r in rows]
    return jsonify({"doubts":doubts_list})

# Save answer
@app.route("/save_answer",methods=["POST"])
def save_answer():
    data = request.get_json()
    doubt_id = data.get("id")
    answer = data.get("answer")
    if doubt_id is None or answer is None:
        return jsonify({"status":"error","message":"Missing fields"})
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("UPDATE doubts SET answer=? WHERE id=?",(answer,doubt_id))
    conn.commit(); conn.close()
    return jsonify({"status":"success"})

# Chatbot
@app.route("/chat",methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data.get("message","")
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role":"system","content":"You are a helpful mentor for students."},
                      {"role":"user","content":user_message}],
            max_tokens=150,
            temperature=0.7
        )
        reply=response['choices'][0]['message']['content']
        return jsonify({"reply":reply})
    except Exception as e:
        return jsonify({"reply":"Error: "+str(e)})

if __name__=="__main__":
    app.run(debug=True, port=5000)
