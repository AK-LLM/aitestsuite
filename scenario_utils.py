import json

def load_scenarios_from_json(file_or_path):
    """
    Loads scenarios from a JSON file.
    Bulletproof against empty files, wrong format, missing keys.
    Returns: (list_of_valid_scenarios, list_of_errors)
    """
    errors = []
    # Read file contents
    try:
        if hasattr(file_or_path, "read"):
            data = file_or_path.read()
            if isinstance(data, bytes):
                data = data.decode("utf-8")
        elif isinstance(file_or_path, str):
            with open(file_or_path, "r", encoding="utf-8") as f:
                data = f.read()
        else:
            errors.append("Unsupported file type")
            return [], errors

        if not data.strip():
            errors.append("File is empty")
            return [], errors

        obj = json.loads(data)
    except Exception as e:
        errors.append(f"JSON decode error: {e}")
        return [], errors

    # Validate structure
    if not isinstance(obj, list):
        errors.append("Top-level JSON should be a list of scenarios")
        return [], errors

    valid_scenarios = []
    for idx, scenario in enumerate(obj):
        if not isinstance(scenario, dict):
            errors.append(f"Scenario {idx+1} is not a JSON object")
            continue
        if "scenario_id" not in scenario or "turns" not in scenario:
            errors.append(f"Scenario {idx+1} missing 'scenario_id' or 'turns'")
            continue
        if not isinstance(scenario["turns"], list) or not scenario["turns"]:
            errors.append(f"Scenario {idx+1} has invalid or empty 'turns'")
            continue
        valid_scenarios.append(scenario)

    if not valid_scenarios:
        errors.append("No valid scenarios found in file")

    return valid_scenarios, errors

def flatten_scenario_for_report(scenario, result):
    """Flattens scenario and result for reporting/output."""
    d = {
        "scenario_id": scenario.get("scenario_id"),
        "description": scenario.get("description", ""),
        "category": scenario.get("category", ""),
        "tags": ", ".join(scenario.get("tags", [])),
        "result": result.get("result", "-"),
        "risk_level": result.get("risk_level", "-"),
        "risk_description": result.get("risk_description", "-"),
        "evidence": result.get("evidence", "-"),
        "recommendations": result.get("recommendations", "-"),
        "root_cause": result.get("root_cause", "-")
    }
    return d
