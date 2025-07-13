import requests

def robustness_assessment(endpoint):
    long_prompt = {"prompt": "a" * 5000}  # excessively long input
    try:
        response = requests.post(endpoint, json=long_prompt, timeout=5)
        stable = response.status_code == 200
    except requests.exceptions.RequestException:
        stable = False

    return {
        "status": "Passed" if stable else "Failed",
        "remarks": "Handled large inputs well." if stable else "Failed or timed out under large input."
    }
