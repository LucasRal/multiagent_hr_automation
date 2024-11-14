from core.state import AgentState
from agents.profile_analyzer import ProfileAnalyzerAgent
from agents.interviewer import InterviewerAgent
from agents.hr_coordinator import HRCoordinatorAgent
from utils.json_helpers import ensure_json
from core.config import create_llm
import json

def analyze_profile(state: AgentState) -> AgentState:
    try:
        llm = create_llm()
        profile_analyzer = ProfileAnalyzerAgent(llm)
        analysis = profile_analyzer.analyze(
            state.job_description,
            state.cv_content
        )
        analysis_dict = ensure_json(analysis)
        
        return state.update(
            profile_analysis=json.dumps(analysis_dict),
            current_step="profile_analyzed"
        )
    except Exception as e:
        return state.update(error=str(e))


def prepare_interview(state: AgentState) -> AgentState:
    try:
        llm = create_llm()
        interviewer = InterviewerAgent(llm)
        interview_plan = interviewer.prepare_interview(
            state.profile_analysis,
            state.job_description
        )
        plan_dict = ensure_json(interview_plan)
        
        return AgentState(
            job_description=state.job_description,
            cv_content=state.cv_content,
            profile_analysis=state.profile_analysis,
            interview_plan=json.dumps(plan_dict),
            interview_feedback=state.interview_feedback,
            final_recommendation=state.final_recommendation,
            current_step="interview_planned",
            error=None
        )
    except Exception as e:
        return AgentState(
            job_description=state.job_description,
            cv_content=state.cv_content,
            profile_analysis=state.profile_analysis,
            interview_plan=state.interview_plan,
            interview_feedback=state.interview_feedback,
            final_recommendation=state.final_recommendation,
            current_step=state.current_step,
            error=str(e)
        )

def synthesize_results(state: AgentState) -> AgentState:
    try:
        llm = create_llm()
        coordinator = HRCoordinatorAgent(llm)
        recommendation = coordinator.synthesize(
            state.profile_analysis,
            state.interview_plan,
            state.interview_feedback
        )
        recommendation_dict = ensure_json(recommendation)
        
        return AgentState(
            job_description=state.job_description,
            cv_content=state.cv_content,
            profile_analysis=state.profile_analysis,
            interview_plan=state.interview_plan,
            interview_feedback=state.interview_feedback,
            final_recommendation=json.dumps(recommendation_dict),
            current_step="completed",
            error=None
        )
    except Exception as e:
        return AgentState(
            job_description=state.job_description,
            cv_content=state.cv_content,
            profile_analysis=state.profile_analysis,
            interview_plan=state.interview_plan,
            interview_feedback=state.interview_feedback,
            final_recommendation=state.final_recommendation,
            current_step=state.current_step,
            error=str(e)
        )

def should_continue(state: AgentState) -> str:
    if state.error:  # Use dot notation
        return "error"
    
    if state.current_step == "profile_analyzed":
        return "prepare_interview"
    elif state.current_step == "interview_planned":
        if state.interview_feedback:
            return "synthesize"
        else:
            return "await_feedback"
    return "end"
