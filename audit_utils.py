import json
from datetime import datetime

def log_audit_entry(endpoint, results):
    entry = {
        "timestamp": datetime.now().isoformat(),
        "endpoint": endpoint,
        "results_count": len(results),
        "results": results
    }
    try:
        with open("audit_log.json", "r") as f:
            audit_log = json.load(f)
    except Exception:
        audit_log = []
    audit_log.append(entry)
    with open("audit_log.json", "w") as f:
        json.dump(audit_log, f, indent=2)
