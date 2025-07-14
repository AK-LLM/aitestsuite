import requests
import random
import string
import time

def fuzz_test(endpoint):
    junk = ''.join(random.choices(string.punctuation + string.ascii_letters, k=1000))
    try:
        resp = requests.post(endpoint, json={"prompt": junk}, timeout=8)
        return "Junk input: OK" if resp.status_code == 200 else "Junk input: Failed/Error"
    except Exception:
        return "Junk input: Failed/Timeout"

def robustness_assessment(endpoint):
    findings = []
    # Long input test
    t0 = time.time()
    try:
        resp = requests.post(endpoint, json={"prompt": "a"*5000}, timeout=8)
        findings.append("Long input: OK" if resp.status_code == 200 else "Long input: Failed/Error")
    except Exception:
        findings.append("Long input: Failed/Timeout")
    t1 = time.time()
    latency = t1 - t0
    # Empty input
    try:
        resp = requests.post(endpoint, json={"prompt": ""}, timeout=8)
        findings.append("Empty input: OK" if resp.status_code == 200 else "Empty input: Failed/Error")
    except Exception:
        findings.append("Empty input: Failed/Timeout")
    # Fuzzing
    findings.append(fuzz_test(endpoint))
    # Latency
    findings.append(f"Latency (long input): {latency:.2f}s")
    status = "Passed" if all("OK" in f for f in findings) else "Partial/Failed"
    remarks = "; ".join(findings)
    return {"status": status, "remarks": remarks}
