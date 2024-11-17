from langgraph.graph import Graph, StateGraph, END
from core.state import AgentState
from workflow.nodes import (
    analyze_profile,
    prepare_interview,
    synthesize_results,
    should_continue
)
from utils.logging_utils import setup_logger

logger = setup_logger("hr_workflow.graph")

def create_hr_workflow() -> Graph:
    logger.info("Creating HR workflow graph")
    
    workflow = StateGraph(AgentState)
    
    # Add nodes
    logger.debug("Adding workflow nodes")
    workflow.add_node("analyze_profile", analyze_profile)
    workflow.add_node("prepare_interview", prepare_interview)
    workflow.add_node("synthesize", synthesize_results)
    
    # Define the edges
    logger.debug("Configuring workflow transitions")
    workflow.add_conditional_edges(
        "analyze_profile",
        should_continue,
        {
            "prepare_interview": "prepare_interview",
            "error": END,
            "end": END
        }
    )
    
    workflow.add_conditional_edges(
        "prepare_interview",
        should_continue,
        {
            "synthesize": "synthesize",
            "await_feedback": END,
            "error": END,
            "end": END
        }
    )
    
    workflow.add_conditional_edges(
        "synthesize",
        should_continue,
        {
            "end": END,
            "error": END
        }
    )
    
    workflow.set_entry_point("analyze_profile")
    
    logger.info("HR workflow graph created successfully")
    return workflow.compile()