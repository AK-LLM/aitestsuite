def call_mcp_service(prompt):
    # Placeholder for real MCP call, return simulated context validation
    return "Context validated (MCP API)."

def local_context_validation(prompt):
    # Local (offline) context check for fallback
    return "Context check bypassed (local mode)."

def mcp_context_test(endpoint, use_mcp=True):
    test_prompt = "Summarize GDPR principles."
    if use_mcp:
        details = call_mcp_service(test_prompt)
        return {"context_result": "MCP Context Checked", "details": details}
    else:
        details = local_context_validation(test_prompt)
        return {"context_result": "Skipped (MCP disabled).", "details": details}
