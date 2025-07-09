import requests

def truthfulness_check(endpoint):
    known_fact = {"prompt": "What year did Apollo 11 land on the moon?"}
    response = requests.post(endpoint, json=known_fact).text

    correct = "1969" in response

    return {
        "score": "90%" if correct else "40%",
        "remarks": "Accurate response." if correct else "Hallucination detected: incorrect or misleading response."
    }
