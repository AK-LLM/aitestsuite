import json

def save_session(findings, file="session.json"):
    with open(file, "w") as f:
        json.dump(findings, f)

def load_session(file="session.json"):
    with open(file) as f:
        return json.load(f)
