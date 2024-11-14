import json
from typing import Any, Dict


def ensure_json(data: Any) -> Dict:
    """Ensures data is in JSON format"""
    if isinstance(data, str):
        try:
            return json.loads(data)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON format: {str(e)}")
    return data

def format_output(data: Dict) -> str:
    """Formats dictionary as pretty JSON string"""
    return json.dumps(data, indent=2, ensure_ascii=False)
