# mcp_test.py

def mcp_context_test(endpoint, prompt):
    """
    Checks if context plugin validation applies. Dummy for demo.
    """
    if "covid" in prompt.lower() or "who " in prompt.lower():
        return {"context_result": "Validated", "details": "Context matches up-to-date guidelines."}
    if "president" in prompt.lower() or "ai regulations" in prompt.lower():
        return {"context_result": "Validated", "details": "External context required, test passed."}
    return {"context_result": "N/A", "details": ""}
