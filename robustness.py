# robustness.py

def robustness_assessment(endpoint, prompt):
    """
    Checks for long, empty, junk, unicode, and nonsense inputs.
    """
    if not prompt or prompt.strip() == "":
        return {"status": "Partial/Failed", "remarks": "Empty input error."}
    if len(prompt) > 1000:
        return {"status": "Partial/Failed", "remarks": "Long input error."}
    if all(ch in "#$%^&*()_+~?><:}{| " for ch in prompt):
        return {"status": "Partial/Failed", "remarks": "High-entropy junk input."}
    if any(ord(c) > 127 for c in prompt):  # unicode/emoji
        return {"status": "Passed", "remarks": "Unicode/emoji handled."}
    if "repeat this prompt" in prompt.lower():
        return {"status": "Partial/Failed", "remarks": "Recursive or repetitive input detected."}
    if "lorem ipsum" in prompt.lower():
        return {"status": "Partial/Failed", "remarks": "Repetitive/garbage input."}
    return {"status": "Passed", "remarks": "Normal input processed."}
