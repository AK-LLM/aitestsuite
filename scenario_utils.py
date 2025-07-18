import json

def load_scenarios_from_json(file_or_path):
    """
    Loads scenarios from a JSON file.
    Supports file-like object (Streamlit upload) or a path string.
    """
    # If it's a Streamlit uploaded file (file-like, has read)
    if hasattr(file_or_path, "read"):
        return json.load(file_or_path)
    # If it's a path (str)
    elif isinstance(file_or_path, str):
        with open(file_or_path, "r", encoding="utf-8") as f:
            return json.load(f)
    else:
        raise ValueError("Unsupported input for loading JSON scenarios.")

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
