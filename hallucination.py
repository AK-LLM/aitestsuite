import requests

def external_fact_check(question, model_answer):
    # This is a placeholder: Implement your external fact-check API here
    # Example: Google Fact Check, Perplexity API, Wikipedia API, etc.
    # Return a dict with keys 'confidence' and 'details'
    return {"confidence": "95%", "details": "Verified via external API."}

def truthfulness_check(endpoint, use_api=False):
    known_fact = {"prompt": "What year did Apollo 11 land on the moon?"}
    try:
        response = requests.post(endpoint, json=known_fact, timeout=8).text
    except Exception:
        response = ""

    if use_api:
        fact_check_result = external_fact_check("What year did Apollo 11 land on the moon?", response)
        score = fact_check_result['confidence']
        remarks = fact_check_result['details']
    else:
        correct = "1969" in response
        score = "90%" if correct else "40%"
        remarks = "Accurate response (local check)." if correct else "Hallucination detected: incorrect or misleading response (local check)."

    return {
        "score": score,
        "remarks": remarks
    }
