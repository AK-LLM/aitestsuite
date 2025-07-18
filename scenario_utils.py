import json

def load_scenarios_from_json(file):
    """Loads a list of scenarios from a user-uploaded JSON file or string."""
    if hasattr(file, "read"):
        data = file.read()
        scenarios = json.loads(data)
    else:
        scenarios = json.loads(file)
    return scenarios

def flatten_scenario_for_report(scenario, results):
    """
    Flattens a scenario+results for reporting (PDF/CSV/etc).
    """
    context_trace = " / ".join(
        f"{t['role']}: {t['content']}" for t in scenario.get("turns", [])
    )
    return {
        "scenario_id": scenario.get("scenario_id", ""),
        "description": scenario.get("description", ""),
        "tags": ", ".join(scenario.get("tags", [])),
        "expected_behavior": scenario.get("expected_behavior", ""),
        "context_trace": context_trace,
        "result": results.get("result", "-"),
        "risk_level": results.get("risk_level", "-"),
        "risk_description": results.get("risk_description", "-"),
        "evidence": results.get("evidence", "-"),
        "recommendations": results.get("recommendations", "-"),
        "root_cause": results.get("root_cause", "-"),
    }
