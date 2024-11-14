from typing import Dict
import json
from datetime import datetime

def generate_structured_report(
    initial_analysis: Dict,
    final_result: Dict | None = None,
    output_file: str | None = None
) -> str:
    """Generate a structured report combining all analysis results."""

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    report = {
        "timestamp": timestamp,
        "recruitment_process": {
            "initial_analysis": {
                "profile_match": initial_analysis.get("profile_analysis"),
                "proposed_interview_plan": initial_analysis.get("interview_plan"),
                "status": initial_analysis.get("status")
            }
        }
    }

    if final_result:
        report["recruitment_process"]["final_evaluation"] = {
            "interview_results": final_result.get("profile_analysis"),
            "final_recommendation": final_result.get("final_recommendation"),
            "status": final_result.get("status")
        }

    if output_file:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        return output_file

    return json.dumps(report, indent=2, ensure_ascii=False)
