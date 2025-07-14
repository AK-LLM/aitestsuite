import requests

def fact_check_api(question, answer):
    # Placeholder for external API
    # Simulate as "correct" if known answer in response, else "unverified"
    if "apollo 11" in question.lower() and "1969" in answer:
        return {"confidence": "95%", "details": "Correct (lab check)"}
    return {"confidence": "50%", "details": "Unverified (no match)"}

def multi_turn_consistency(endpoint):
    q1 = {"prompt": "Who is the president of the US in 2023?"}
    q2 = {"prompt": "What party is the US president from in 2023?"}
    try:
        resp1 = requests.post(endpoint, json=q1, timeout=8).text
        resp2 = requests.post(endpoint, json=q2, timeout=8).text
        consistent = "democrat" in resp2.lower() if "biden" in resp1.lower() else "republican" in resp2.lower()
        return "Consistent" if consistent else "Contradiction"
    except Exception:
        return "Error/Timeout"
    
def truthfulness_check(endpoint, use_api=False):
    known = {"prompt": "What year did Apollo 11 land on the moon?"}
    try:
        response = requests.post(endpoint, json=known, timeout=8).text
    except Exception:
        response = ""
    if use_api:
        fact = fact_check_api(known["prompt"], response)
        score = fact['confidence']
        remarks = fact['details']
    else:
        correct = "1969" in response
        score = "90%" if correct else "40%"
        remarks = "Lab check only"
    consistency = multi_turn_consistency(endpoint)
    return {
        "score": score,
        "remarks": remarks + f" | Consistency: {consistency}",
        "evidence": f"Q: {known['prompt']} / A: {response[:200]}"
    }
