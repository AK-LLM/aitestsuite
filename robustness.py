import requests

def robustness_assessment(endpoint):
    long_prompt = {"prompt": "a" * 5000}
    try:
        response = requests.post(endpoint, json=long_prompt, timeout=8)
        stable = response.status_code == 200
    except Exception:
        stable = False

    return {
        "status": "Passed" if stable else "Failed",
        "remarks": "Handled large inputs well." if stable else "Failed or timed out under large input."
    }
