import logging
from typing import Any
import json
from functools import wraps
import traceback


class Colors:
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    RESET = '\033[0m'

class ColoredFormatter(logging.Formatter):
    """Custom formatter that adds colors to log messages"""
    
    def format(self, record):
        original_msg = record.msg
        
        if "Starting" in str(record.msg):
            record.msg = f"{Colors.BLUE}{record.msg}{Colors.RESET}"
        elif "Completed" in str(record.msg):
            record.msg = f"{Colors.GREEN}{record.msg}{Colors.RESET}"
        elif "Transition decision" in str(record.msg):
            record.msg = f"{Colors.YELLOW}{record.msg}{Colors.RESET}"
        elif "Error" in str(record.msg):
            record.msg = f"{Colors.RED}{record.msg}{Colors.RESET}"
            
        # Format the message
        result = super().format(record)
        
        # Restore the original message for other handlers
        record.msg = original_msg
        return result

def setup_logger(name: str = "hr_workflow"):
    logger = logging.getLogger(name)
    
    # Only add handlers if they haven't been added already
    if not logger.handlers:
        logger.setLevel(logging.INFO)
        
        # Console Handler with colors
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        colored_formatter = ColoredFormatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        console_handler.setFormatter(colored_formatter)
        
        # File Handler
        file_handler = logging.FileHandler('hr_workflow.log')
        file_handler.setLevel(logging.DEBUG)
        file_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s'
        )
        file_handler.setFormatter(file_formatter)
        
        logger.addHandler(console_handler)
        logger.addHandler(file_handler)
    
    return logger

# Helper function to safely serialize state for logging
def serialize_state(state: Any) -> str:
    try:
        if hasattr(state, '__dict__'):
            return json.dumps(state.__dict__, indent=2)
        return str(state)
    except Exception:
        return str(state)

# Decorator for node functions
def log_node_execution(node_name: str):
    logger = setup_logger()
    
    def decorator(func):
        @wraps(func)
        def wrapper(state, *args, **kwargs):
            logger.info(f"Starting {node_name} execution")
            logger.debug(f"Input state: {serialize_state(state)}")
            
            try:
                result = func(state, *args, **kwargs)
                logger.info(f"Completed {node_name} execution")
                logger.debug(f"Output state: {serialize_state(result)}")
                return result
            except Exception as e:
                logger.error(f"Error in {node_name}: {str(e)}")
                logger.error(f"Traceback: {traceback.format_exc()}")
                raise
        
        return wrapper
    return decorator

# Decorator for the conditional router
def log_transition(func):
    logger = setup_logger()
    
    @wraps(func)
    def wrapper(state, *args, **kwargs):
        logger.info("Evaluating workflow transition")
        logger.debug(f"Current state: {serialize_state(state)}")
        
        result = func(state, *args, **kwargs)
        logger.info(f"Transition decision: {result}")
        return result
    
    return wrapper