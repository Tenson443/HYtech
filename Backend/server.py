from flask import Flask, request, jsonify
import pandas as pd
from datetime import datetime
import os
from Ai import ask_ollama

app = Flask(__name__)

DB_FILE = "messages_db.csv"

# Added "role" to the columns!
if os.path.exists(DB_FILE):
    df = pd.read_csv(DB_FILE)
    print(f"Loaded existing database with {len(df)} messages.")
else:
    columns = ["timestamp", "role", "student", "message", "subject"]
    df = pd.DataFrame(columns=columns)
    print("Created new empty database.")


@app.route("/send_message", methods=["POST"])
def send_message():
    global df
    data = request.json

    # We now look for a 'role'. If they don't provide one, we assume it's a student.
    role = data.get("role", "student")
    student = data.get("student", "Unknown")
    message = data.get("message", "")

    # If it's a teacher, we DO NOT ask Ollama. We just label it "Teacher Reply"
    if role == "teacher":
        classification = "Teacher Reply"
    else:
        # If it's a student, we classify their math question
        classification = ask_ollama(message)

    new_row = {
        "timestamp": datetime.now().strftime("%H:%M:%S"),
        "role": role,
        "student": student,
        "message": message,
        "subject": classification
    }

    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    df.to_csv(DB_FILE, index=False)

    return jsonify({"status": "ok", "classification": classification})


@app.route("/get_messages", methods=["GET"])
def get_messages():
    if df.empty:
        return jsonify([])

    messages = df.copy()
    return jsonify(messages.to_dict(orient="records"))


@app.route("/get_stats", methods=["GET"])
def get_stats():
    if df.empty:
        return jsonify([])

    # Filter out non-math questions AND Teacher Replies
    filtered = df[(df["subject"] != "Other") & (df["subject"] != "Teacher Reply")]

    if filtered.empty:
        return jsonify([])

    stats = filtered.groupby("subject").size().reset_index(name="count")
    return jsonify(stats.to_dict(orient="records"))


if __name__ == "__main__":
    print("Starting Chat & Classification Server on port 5000...")
    app.run(host='0.0.0.0', port=5000, debug=True)