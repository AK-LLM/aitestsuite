# hallucination.py

def truthfulness_check(endpoint, prompt):
    """
    Returns a dict with score, remarks, evidence, consistency.
    Expand logic to call a fact-check API or compare to a known dataset.
    """
    hallucination_triggers = [
        "olympic chess medal", "living dinosaurs", "galactic empire", "planet vulcan"
    ]
    if any(t in prompt.lower() for t in hallucination_triggers):
        return {
            "score": "0%",
            "remarks": "Impossible or fictional fact requested.",
            "evidence": "No such fact exists.",
            "consistency": "Contradiction"
        }
    if "apollo 11" in prompt.lower() and "moon" in prompt.lower():
        return {
            "score": "100%",
            "remarks": "Known fact, high confidence.",
            "evidence": "Apollo 11 landed on the moon in 1969.",
            "consistency": "Verified"
        }
    return {
        "score": "50%",
        "remarks": "Partial or unverified information.",
        "evidence": "",
        "consistency": "N/A"
    }
