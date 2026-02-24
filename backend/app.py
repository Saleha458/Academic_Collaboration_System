from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import random

app = Flask(__name__)
CORS(app)

# In-memory users (Reset on restart)
users = {"admin": "admin123"}

try:
    df = pd.read_csv("backend/studentInfo.csv")
    all_ids = df["id_student"].astype(str).unique().tolist()
except:
    all_ids = [str(i) for i in range(1001, 1050)]

@app.route("/register", methods=["POST"])
def register():
    data = request.json
    u, p = data.get("username"), data.get("password")
    if u in users: return jsonify({"msg": "User exists"}), 409
    users[u] = p
    return jsonify({"msg": "Success"}), 201

@app.route("/login", methods=["POST"])
def login():
    data = request.json
    if users.get(data.get("username")) == data.get("password"):
        return jsonify({"msg": "Success"}), 200
    return jsonify({"msg": "Fail"}), 401

@app.route("/student-ids")
def get_ids():
    return jsonify(all_ids)

@app.route("/ai-analytics")
def ai_analytics():
    status = random.choice(["SAFE", "AT RISK"])
    percent = random.randint(65, 98)
    return jsonify({
        "status": f"{status} ({percent}%)",
        "strength": random.choice(["VLE Engagement", "Quiz Consistency", "Forum Activity"]),
        "weakness": random.choice(["Late Submissions", "Low Interaction", "Exam Anxiety"]),
        "advice": random.choice(["Join group sessions", "Review Module 3", "Practice mock tests"])
    })

@app.route("/group-study")
def group_study():
    peers = [{"id": random.choice(all_ids), "score": random.randint(70, 99)} for _ in range(3)]
    return jsonify(peers)

@app.route("/performance-graph")
def performance():
    return jsonify({
        "labels": ["Week 1", "Week 2", "Week 3", "Week 4"],
        "scores": [random.randint(50, 95) for _ in range(4)]
    })

if __name__ == "__main__":
    app.run(debug=True, port=5000)