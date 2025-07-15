# security.py

def security_assessment(endpoint, prompt):
    """
    Returns a dict with risk_level and summary (and evidence if desired).
    Replace logic with API calls or deeper checks as needed.
    """
    risky = "ignore" in prompt.lower() or "admin" in prompt.lower() or "secret" in prompt.lower()
    if risky:
        return {
            "risk_level": "High Risk",
            "summary": "Prompt injection or privileged escalation detected."
        }
    else:
        return {
            "risk_level": "Low Risk",
            "summary": "No injection risk detected."
        }
