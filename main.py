import os
from typing import Dict
from workflow.graph import create_hr_workflow
from core.state import AgentState
import json
from datetime import datetime
from utils.report_generator import generate_structured_report


def process_candidate(
    job_description: str,
    cv_content: str,
    interview_feedback: str | None = None
) -> Dict:
    workflow = create_hr_workflow()
    
    initial_state = AgentState.create_initial(
        job_description=job_description,
        cv_content=cv_content,
        interview_feedback=interview_feedback
    )
    
    # Get the final state from the workflow
    final_state_dict = workflow.invoke(initial_state)
    
    # Convert the final state dict back to our AgentState class
    final_state = AgentState.from_dict(dict(final_state_dict))
    
    return {
        "profile_analysis": json.loads(final_state.profile_analysis) if final_state.profile_analysis else None,
        "interview_plan": json.loads(final_state.interview_plan) if final_state.interview_plan else None,
        "final_recommendation": json.loads(final_state.final_recommendation) if final_state.final_recommendation else None,
        "error": final_state.error,
        "status": final_state.current_step
    }

def save_results(results: Dict, filename: str):
    """Save results to a file in the outputs directory."""
    
    output_dir = "outputs"
    os.makedirs(output_dir, exist_ok=True)
    
    file_path = os.path.join(output_dir, filename)
    
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    return file_path
if __name__ == "__main__":
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    job_description = """
    Senior Software Engineer
    
    Responsabilités:
    - Développement d'applications Python complexes
    - Leadership technique d'équipe
    - Architecture de solutions cloud
    
    Requis:
    - 5+ ans d'expérience en Python
    - Expérience en AI/ML
    - Excellentes capacités de communication
    """
    
    cv_content = """
    Jean Dupont
    Ingénieur Logiciel Senior
    
    Expérience:
    - 6 ans de développement Python
    - Chef d'équipe technique (3 ans)
    - Projets ML/AI réussis
    
    Compétences:
    - Python, TensorFlow, AWS
    - Leadership d'équipe
    - Communication technique
    """
    
    # Initial analysis and interview planning
    result = process_candidate(
        job_description=job_description,
        cv_content=cv_content
    )
    initial_analysis_file = save_results(
        result,
        f"initial_analysis_{timestamp}.json"
    )
    print(f"Initial analysis saved to: {initial_analysis_file}")
    
    # Later, after interview. Mock feedback
    interview_feedback = """
    {
        "technical_performance": "Excellent",
        "communication_skills": "Très bon",
        "technical_questions_score": 9,
        "behavioral_score": 8,
        "overall_impression": "Candidat prometteur avec une excellente maîtrise technique"
    }
    """
    
    final_result = process_candidate(
        job_description=job_description,
        cv_content=cv_content,
        interview_feedback=interview_feedback
    )
    final_result_file = save_results(
        final_result,
        f"final_result_{timestamp}.json"
    )
    print(f"Final result saved to: {final_result_file}")

    report_file = os.path.join("outputs", f"complete_report_{timestamp}.json")
    generate_structured_report(result, final_result, report_file)
    print(f"Complete report saved to: {report_file}")
