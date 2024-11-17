import os
import sys
import json
from datetime import datetime
import logging

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import process_candidate, save_results

# Setup logging
def setup_test_logger():
    logger = logging.getLogger('test_cases')
    logger.setLevel(logging.DEBUG)
    
    # Create logs directory if it doesn't exist
    os.makedirs("logs", exist_ok=True)
    
    # File handler
    fh = logging.FileHandler(f'logs/test_cases_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log')
    fh.setLevel(logging.DEBUG)
    
    # Console handler
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    
    # Format
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)
    
    logger.addHandler(fh)
    logger.addHandler(ch)
    
    return logger

logger = setup_test_logger()

def log_state(result: dict, test_name: str):
    """Log the state information from the result"""
    logger.info(f"\n{'='*50}")
    logger.info(f"Test Case: {test_name}")
    logger.info(f"Current Step: {result.get('status', 'N/A')}")
    logger.info(f"Error: {result.get('error', 'None')}")
    
    # Log detailed state information
    logger.debug("Profile Analysis:")
    try:
        if result.get('profile_analysis'):
            analysis = json.loads(result['profile_analysis'])
            logger.debug(json.dumps(analysis, indent=2))
    except Exception as e:
        logger.debug(f"Could not parse profile analysis: {e}")
    
    logger.debug("Interview Plan:")
    try:
        if result.get('interview_plan'):
            plan = json.loads(result['interview_plan'])
            logger.debug(json.dumps(plan, indent=2))
    except Exception as e:
        logger.debug(f"Could not parse interview plan: {e}")
    
    logger.debug("Final Recommendation:")
    try:
        if result.get('final_recommendation'):
            recommendation = json.loads(result['final_recommendation'])
            logger.debug(json.dumps(recommendation, indent=2))
    except Exception as e:
        logger.debug(f"Could not parse final recommendation: {e}")
    
    logger.info(f"{'='*50}\n")

def test_empty_cv():
    """Test case for empty CV content"""
    logger.info("\nTesting empty CV case...")
    
    job_description = """
    Senior Software Engineer
    
    Responsabilités:
    - Développement d'applications Python complexes
    - Leadership technique d'équipe
    """
    
    cv_content = ""
    
    result = process_candidate(
        job_description=job_description,
        cv_content=cv_content
    )
    log_state(result, "Empty CV")
    return result

def test_malformed_feedback():
    """Test case for malformed interview feedback"""
    logger.info("\nTesting malformed feedback case...")
    job_description = """
    Senior Software Engineer
    
    Responsabilités:
    - Développement d'applications Python complexes
    """
    
    cv_content = """
    Jean Dupont
    Ingénieur Logiciel Senior
    """
    
    interview_feedback = """
    {
        "technical_performance": "Excellent",
        "communication_skills": "Très bon",
        MALFORMED_JSON  # Error ry zareo a
    """
    
    result = process_candidate(
        job_description=job_description,
        cv_content=cv_content,
        interview_feedback=interview_feedback
    )
    log_state(result, "Malformed Feedback")
    return result

def test_invalid_cv_content():
    """Test case for invalid CV content type"""
    logger.info("\nTesting invalid CV content case...")
    job_description = "Senior Software Engineer"
    cv_content = {"this": "should", "be": "text", "not": "dict"}
    
    result = process_candidate(
        job_description=job_description,
        cv_content=cv_content
    )
    log_state(result, "Invalid CV Content")
    return result

def run_all_tests():
    """Run all error test cases and save results"""
    logger.info("Starting error test cases...")
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Create a test results directory
    test_output_dir = os.path.join("outputs", "test_results")
    os.makedirs(test_output_dir, exist_ok=True)
    
    try:
        # Run empty CV test
        empty_cv_result = test_empty_cv()
        save_results(
            empty_cv_result,
            os.path.join("test_results", f"error_empty_cv_{timestamp}.json")
        )
        
        # Run malformed feedback test
        malformed_feedback_result = test_malformed_feedback()
        save_results(
            malformed_feedback_result,
            os.path.join("test_results", f"error_malformed_feedback_{timestamp}.json")
        )
        
        # Run invalid CV content test
        invalid_cv_result = test_invalid_cv_content()
        save_results(
            invalid_cv_result,
            os.path.join("test_results", f"error_invalid_cv_{timestamp}.json")
        )
        
        logger.info("\nAll test results have been saved in the outputs/test_results directory")
    except Exception as e:
        logger.error(f"Error during test execution: {str(e)}")
        raise

if __name__ == "__main__":
    run_all_tests()