from core.state import AgentState
from agents.profile_analyzer import ProfileAnalyzerAgent
from agents.interviewer import InterviewerAgent
from agents.hr_coordinator import HRCoordinatorAgent
from utils.json_helpers import ensure_json
from core.config import create_llm
from utils.logging_utils import log_node_execution, log_transition, setup_logger
import json

state_logger = setup_logger("agent_state_tracker")

@log_node_execution("profile_analysis")
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

@log_node_execution("interview_preparation")
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

@log_node_execution("results_synthesis")
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


@log_transition
def should_continue(state: AgentState) -> str:
    # Log the complete state
    state_logger.info(f"\n{'='*50}")
    state_logger.info("Current AgentState:")
    
    # Log basic attributes
    state_logger.info(f"Current Step: {state.current_step}")
    state_logger.info(f"Error State: {state.error if state.error else 'No error'}")
    
    # Log job description and CV content (truncated if too long)
    max_length = 50
    state_logger.info(f"\nJob Description: {state.job_description[:max_length]}...")
    state_logger.info(f"\nCV Content: {state.cv_content[:max_length]}...")
    
    # Log JSON
    if state.profile_analysis:
        try:
            analysis = json.loads(state.profile_analysis)
            state_logger.info(f"\nProfile Analysis:\n{json.dumps(analysis, indent=2, ensure_ascii=False)}")
        except json.JSONDecodeError:
            state_logger.info(f"\nProfile Analysis (raw):\n{state.profile_analysis}")
    
    if state.interview_plan:
        try:
            plan = json.loads(state.interview_plan)
            state_logger.info(f"\nInterview Plan:\n{json.dumps(plan, indent=2, ensure_ascii=False)}")
        except json.JSONDecodeError:
            state_logger.info(f"\nInterview Plan (raw):\n{state.interview_plan}")
    
    if state.interview_feedback:
        try:
            feedback = json.loads(state.interview_feedback)
            state_logger.info(f"\nInterview Feedback:\n{json.dumps(feedback, indent=2, ensure_ascii=False)}")
        except json.JSONDecodeError:
            state_logger.info(f"\nInterview Feedback (raw):\n{state.interview_feedback}")
    
    if state.final_recommendation:
        try:
            recommendation = json.loads(state.final_recommendation)
            state_logger.info(f"\nFinal Recommendation:\n{json.dumps(recommendation, indent=2, ensure_ascii=False)}")
        except json.JSONDecodeError:
            state_logger.info(f"\nFinal Recommendation (raw):\n{state.final_recommendation}")
    
    # Log complete state as dictionary for debugging
    state_logger.debug(f"\nComplete State Dictionary:\n{json.dumps(state.to_dict(), indent=2, ensure_ascii=False)}")
    
    state_logger.info(f"{'='*50}\n")
    
    # Conditional logic
    if state.error:
        return "error"
    
    if state.current_step == "profile_analyzed":
        return "prepare_interview"
    elif state.current_step == "interview_planned":
        if state.interview_feedback:
            return "synthesize"
        else:
            return "await_feedback"
    return "end"