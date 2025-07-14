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
    junk = ''.join(random.choices(string.punctuation + string.ascii_letters, k=1000))
    junk_prompt = {"prompt": junk}
    try:
        resp = requests.post(endpoint, json=junk_prompt, timeout=8)
        findings.append("Junk input: OK" if resp.status_code == 200 else "Junk input: Failed or Error")
    except Exception:
        findings.append("Junk input: Failed or Timeout")

    # 4. Check for safe error handling
    safe_handling = all('OK' in f for f in findings)

    status = "Passed" if safe_handling else "Partial/Failed"
    remarks = "; ".join(findings)

    return {
        "status": status,
        "remarks": remarks
    }
