from typing import Dict

def get_prompt_variables(agent_type: str, data: Dict) -> Dict:
    """Helper function to prepare variables for prompt templates"""
    base_variables = {
        "query": data.get("query", ""),
        "context": data.get("context", ""),
        "data": data.get("data", {})
    }
    
    # Add any additional agent-specific variables
    if agent_type == "delivery":
        base_variables.update({
            "metrics": data.get("metrics", {}),
            "thresholds": data.get("thresholds", {})
        })
    elif agent_type == "courier":
        base_variables.update({
            "courier_data": data.get("courier_data", {}),
            "weight_data": data.get("weight_data", {})
        })
    
    return base_variables