import requests
import random
import string

def robustness_assessment(endpoint):
    findings = []

    # 1. Long input test
    long_prompt = {"prompt": "a" * 5000}
    try:
        resp = requests.post(endpoint, json=long_prompt, timeout=8)
        findings.append("Long input: OK" if resp.status_code == 200 else "Long input: Failed or Error")
    except Exception:
        findings.append("Long input: Failed or Timeout")

    # 2. Empty input test
    empty_prompt = {"prompt": ""}
    try:
        resp = requests.post(endpoint, json=empty_prompt, timeout=8)
        findings.append("Empty input: OK" if resp.status_code == 200 else "Empty input: Failed or Error")
    except Exception:
        findings.append("Empty input: Failed or Timeout")

    # 3. Random junk input test
    junk = ''.join(random.choices(string.punctuation +
