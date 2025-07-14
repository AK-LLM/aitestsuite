import json
import os

def save_session(findings, file="session.json"):
    with open(file, "w") as f:
        json.dump(findings, f)

def load_session(file="session.json"):
    if not os.path.exists(file):
        return {"error": "No previous session found."}
    with open(file) as f:
        return json.load(f)
